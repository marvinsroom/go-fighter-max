"""Local-only landmark analysis and smooth 3D deformation; no network calls."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
import mediapipe as mp
from scipy.interpolate import RBFInterpolator

root=Path(__file__).resolve().parents[1]
out=root/'characters/will/local-head-fit-v1'
model=root/'tooling/local-face-models/face_landmarker.task'
options=mp.tasks.vision.FaceLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path=str(model)),num_faces=1,
    min_face_detection_confidence=.35,min_face_presence_confidence=.35)
paths={'source':out/'source-front.png',
       'reference':root/'characters/will/reference-reconstruction/will-head-input-v1.png'}
landmarks={}
with mp.tasks.vision.FaceLandmarker.create_from_options(options) as detector:
    for name,path in paths.items():
        image=np.array(Image.open(path).convert('RGB'))
        result=detector.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=image))
        if len(result.face_landmarks)!=1:
            raise RuntimeError('Expected one detectable face in '+name)
        landmarks[name]={'width':image.shape[1],'height':image.shape[0],
                         'points':[[p.x,p.y,p.z] for p in result.face_landmarks[0]]}
(out/'landmarks.json').write_text(json.dumps(landmarks,indent=2))
geometry=json.loads((out/'source-geometry.json').read_text())
vertices=np.asarray(geometry['vertices'])
triangles=[]
for polygon in geometry['polygons']:
    for i in range(1,len(polygon)-1):
        triangles.append([polygon[0],polygon[i],polygon[i+1]])
tri=vertices[np.asarray(triangles)]
a=tri[:,0][:,[0,2]];b=tri[:,1][:,[0,2]];c=tri[:,2][:,[0,2]]
v0=b-a;v1=c-a
det=v0[:,0]*v1[:,1]-v0[:,1]*v1[:,0]
valid=np.abs(det)>1e-12
den=np.where(valid,det,1)
source=np.asarray(landmarks['source']['points'])
ref=np.asarray(landmarks['reference']['points'])
source_xz=np.column_stack(((source[:,0]-.5)*geometry['ortho_scale'],
                          geometry['camera_z']+(.5-source[:,1])*geometry['ortho_scale']))
skin=np.asarray(geometry['skin_indices'])
front=skin[vertices[skin,1]<-.025*geometry['scale']]

def raycast(point):
    v2=point-a
    u=(v2[:,0]*v1[:,1]-v2[:,1]*v1[:,0])/den
    v=(v0[:,0]*v2[:,1]-v0[:,1]*v2[:,0])/den
    inside=valid&(u>=-.001)&(v>=-.001)&(u+v<=1.001)
    ids=np.flatnonzero(inside)
    if not len(ids):
        nearest=front[np.argmin(np.sum((vertices[front][:,[0,2]]-point)**2,axis=1))]
        return vertices[nearest].copy()
    ys=tri[ids,0,1]+u[ids]*(tri[ids,1,1]-tri[ids,0,1])+v[ids]*(tri[ids,2,1]-tri[ids,0,1])
    index=ids[np.argmin(ys)]
    return np.array([point[0],ys.min(),point[1]])

source3d=np.asarray([raycast(p) for p in source_xz[:468]])
width=landmarks['reference']['width'];height=landmarks['reference']['height']
ref_pixels=np.column_stack((ref[:,0]*width,ref[:,1]*height))
left=[33,133];right=[362,263]
source_left=source3d[left].mean(axis=0);source_right=source3d[right].mean(axis=0)
ref_left=ref_pixels[left].mean(axis=0);ref_right=ref_pixels[right].mean(axis=0)
ref_mid=(ref_left+ref_right)/2;source_mid=(source_left+source_right)/2
pixel_scale=np.linalg.norm(source_left[[0,2]]-source_right[[0,2]])/np.linalg.norm(ref_left-ref_right)*.97
reference_depth_origin=ref[[33,133,362,263],2].mean()
target3d=source3d.copy()
target3d[:,0]=source_mid[0]+(ref_pixels[:468,0]-ref_mid[0])*pixel_scale
target3d[:,2]=source_mid[2]-(ref_pixels[:468,1]-ref_mid[1])*pixel_scale
depth=source_mid[1]+(ref[:468,2]-reference_depth_origin)*width*pixel_scale
target3d[:,1]=source3d[:,1]+np.clip((depth-source3d[:,1])*.45,-.015,.015)
# Use a broad, evenly distributed sample plus the feature boundaries. Dense,
# almost coincident eye/lip vertices otherwise make the interpolant unstable.
features=[10,152,234,454,127,356,93,323,132,361,172,397,136,365,150,379,
          149,378,148,377,176,400,58,288,67,297,109,338,103,332,
          33,133,159,145,158,153,160,144,263,362,386,374,385,380,387,373,
          70,63,105,66,107,336,296,334,293,300,
          1,2,4,5,6,19,94,97,326,98,327,64,294,168,195,
          61,291,0,17,13,14,37,267,39,269,40,270,91,321,84,314,87,317]
control=source3d[features];deltas=target3d[features]-control
# Freeze rear skull and neck so facial changes do not move the body.
s=geometry['scale']
anchors=[]
for z in [1.25,1.29,1.37,1.47,1.53]:
    for x in [-.10,-.05,0,.05,.10]:anchors.append([x*s,.035*s,z*s])
for x in [-.09,-.045,0,.045,.09]:
    for y in [-.10,-.04,.02]:anchors.append([x*s,y*s,1.255*s])
control=np.vstack((control,anchors));deltas=np.vstack((deltas,np.zeros((len(anchors),3))))
# Round tiny duplicate ray hits to avoid singular source controls.
_,unique=np.unique(np.round(control,6),axis=0,return_index=True)
control=control[unique];deltas=deltas[unique]
fit=RBFInterpolator(control,deltas,kernel='thin_plate_spline',smoothing=2e-6)
candidate=fit(vertices)
fade=np.clip((vertices[:,2]-1.255*s)/(.05*s),0,1)
fade*=np.clip((.045*s-vertices[:,1])/(.04*s),0,1)
fade*=np.clip((1.555*s-vertices[:,2])/(.045*s),0,1)
candidate*=fade[:,None]
# Bound the first fit to 3cm per vertex; report rather than silently trust it.
length=np.linalg.norm(candidate,axis=1)
candidate*=np.minimum(1,.03/np.maximum(length,1e-12))[:,None]
new=vertices+candidate
aux={}
for name,points in geometry.get('accessories',{}).items():
    points=np.asarray(points)
    change=fit(points)
    fade_aux=np.clip((points[:,2]-1.255*s)/(.05*s),0,1)*np.clip((.045*s-points[:,1])/(.04*s),0,1)
    fade_aux*=np.clip((1.555*s-points[:,2])/(.045*s),0,1)
    change*=fade_aux[:,None]
    length_aux=np.linalg.norm(change,axis=1)
    change*=np.minimum(1,.03/np.maximum(length_aux,1e-12))[:,None]
    aux[name]=(points+change).tolist()
result={'vertices':new.tolist(),'displacements':candidate.tolist(),'accessories':aux,
        'projection':{'reference_width':width,'reference_height':height,
                      'reference_eye_mid':ref_mid.tolist(),'world_eye_mid':source_mid.tolist(),
                      'meters_per_pixel':float(pixel_scale)},
        'fit_report':{'local_processing':True,'landmarks_detected':len(source),
                      'control_points':len(control),'max_displacement_m':float(np.linalg.norm(candidate,axis=1).max()),
                      'method':'Image landmarks fitted to full MPFB head with a smooth RBF deformation; image depth is approximate'}}
(out/'fitted-head.json').write_text(json.dumps(result))
print('LOCAL_HEAD_FIT_READY',json.dumps(result['fit_report']),flush=True)
