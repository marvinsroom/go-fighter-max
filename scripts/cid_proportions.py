"""Fixed skeleton scales for Cid, independent of animated hood folds."""
import statistics


def calibrate(art):
    def height(key):
        m=art[key];return m['bounds'][3]-m['bounds'][1]
    idle=55/height('movement-a:0')
    walk=55/statistics.median(height(f'movement-a:{i}') for i in range(4,12))
    airborne=55/height('movement-b:2')
    combat=55/height('combat:2')
    for key,m in art.items():
        sheet,index=key.split(':');index=int(index)
        if sheet=='movement-a':scale=idle if index<4 else walk
        elif sheet=='movement-b':scale=idle if index<2 else airborne
        elif sheet=='combat':scale=combat
        elif sheet=='cinematic':
            # These are upright reference poses, not crouch/attack phases.
            scale=55/height(key) if 4<=index<=8 else .17
        else:continue
        m['previous_scale']=m['scale'];m['scale']=scale
        m['logical_head_size']=m['head_length']*scale
        m['calibration']='Fixed sequence scale; upright cinematic references share 55-unit standing height'
    return dict(revision=6,idle=idle,walk=walk,airborne=airborne,combat=combat,
                standing_height=55,method='Fixed sequence skeleton scales; hood folds do not resize an actor; only upright cinematic references fitted to standing height')
