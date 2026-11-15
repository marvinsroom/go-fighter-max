"""Register generated animation islands and measured body anchors for packing."""
from pathlib import Path
from PIL import Image
from scipy import ndimage
import numpy as np,json
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/jinwoo/art/greatsword'
# Fractions are measurements on the complete sheet, not individual auto-fits.
# Body heights exclude raised swords; foot anchors exclude low sword tips.
measurements={
 'stance':(.252,[290,760,260,750,280,750,275,780],[414,414,728,704,1109,1108,1516,1521],(1024,1536)),
 'movement':(.225,[340,803,350,820,345,810,360,825],[376,376,756,757,1134,1136,1509,1513],(1024,1536)),
 'light':(.252,[290,810,300,795,280,790,300,810],[403,396,755,755,1109,1129,1481,1516],(1024,1536)),
 'heavy':(.242,[285,780,290,800,250,780,280,775],[394,394,791,790,1099,1075,1496,1505],(1024,1536)),
 'aerial':(.438,[220,600,950,1360,215,580,955,1370],[507,513,500,500,943,962,971,989],(1536,1024)),
 'reactions':(.456,[185,575,965,1340,190,575,955,1350],[502,500,500,430,932,962,975,1005],(1536,1024)),
 'super':(.401,[205,575,990,1390,150,535,970,1370],[485,479,495,498,936,905,950,966],(1536,1024)),
 'finisher':(.481,[200,550,1000,1460,325,690,1150,1610],[444,443,430,431,863,860,865,873],(1774,887)),
}
registration={'weapon':"Demon King's Longsword",'sheets':{}}
for name,(height,xs,ys,reference_size) in measurements.items():
 path=S/'animations'/f'{name}.png'
 with Image.open(path) as im:
  pixels=np.array(im);w,h=im.size
 assert pixels.shape[2]==4 and pixels[:,:,3].min()==0,path
 threshold=240 if name=='super' else 16
 labels,count=ndimage.label(pixels[:,:,3]>threshold);areas=np.bincount(labels.ravel());objects=ndimage.find_objects(labels)
 ids=sorted(range(1,count+1),key=lambda i:areas[i],reverse=True)[:8]
 assert min(areas[i] for i in ids)>10000,(name,'Missing character islands')
 columns=4 if w>h else 2;rows=8//columns
 ids.sort(key=lambda i:objects[i-1][0].start+objects[i-1][0].stop)
 ids=[i for start in range(0,8,columns) for i in sorted(ids[start:start+columns],key=lambda i:objects[i-1][1].start)]
 components=[[i] for i in ids]
 for i in range(1,count+1):
  if i in ids or areas[i]<3000:continue
  sy,sx=objects[i-1];col=min(columns-1,int((sx.start+sx.stop)*.5/w*columns));row=min(rows-1,int((sy.start+sy.stop)*.5/h*rows))
  components[row*columns+col].append(i)
 frames=[]
 for i,parts in enumerate(components):
  slices=[objects[part-1] for part in parts]
  x1=min(sx.start for sy,sx in slices);y1=min(sy.start for sy,sx in slices);x2=max(sx.stop for sy,sx in slices);y2=max(sy.stop for sy,sx in slices)
  frames.append({'rect':[x1,y1,x2,y2],'components':parts,'axis':[round(xs[i]*w/reference_size[0])-x1,round(ys[i]*h/reference_size[1])-y1]})
 registration['sheets'][name]={'file':f'animations/{name}.png','alpha_min':threshold,'body_height':height*h,'frames':frames}
 print(name,'8 frames',w,h,'body height',height*h)
(S/'registration.json').write_text(json.dumps(registration,indent=2))
