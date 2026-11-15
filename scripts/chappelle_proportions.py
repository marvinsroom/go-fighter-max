"""Reviewed pose landmarks and pivots; never fit a bent pose to standing height.

Coordinates refer to the unmodified packed PNGs. Crown/chin vectors follow the
head's tilt. A bounded correction retains drawn perspective without enlarging a
foreshortened face into an oversized whole body. Pelvis anchors ignore canvas
padding; ground anchors ignore neighboring-sheet fragments.
"""
import math,struct

LANDMARKS={
 'Prince':{
  'idle':((256,28),(272,100),245,417),
  'walk_a':((287,32),(304,101),268,415),
  'walk_b':((251,34),(271,103),236,416),
  'palm':((229,37),(251,99),230,416),
  'kick':((178,43),(204,101),217,416),
  'special':((146,64),(175,119),183,419),
  'crouch':((245,84),(269,144),226,349),
  'hurt':((132,18),(170,74),221,350),
  'down':((39,68),(89,95),226,169)},
 'Rick James':{
  'idle':((242,20),(266,83),233,411),
  'walk_a':((268,16),(290,78),265,409),
  'walk_b':((241,20),(263,81),240,411),
  'palm':((215,38),(242,94),211,423),
  'kick':((207,28),(236,87),245,413),
  'special':((193,66),(222,117),243,422),
  'crouch':((218,110),(245,170),227,362),
  'hurt':((123,38),(159,90),260,373),
  'down':((41,278),(89,280),239,370)},
 'Tyrone Biggums':{
  'idle':((231,35),(251,103),219,402),
  'walk_a':((253,36),(279,104),252,399),
  'walk_b':((271,34),(291,104),259,400),
  'palm':((242,70),(270,128),221,406),
  'kick':((239,70),(267,127),240,399),
  'special':((251,89),(280,142),240,411),
  'crouch':((244,109),(272,166),230,379),
  'hurt':((127,35),(172,87),231,383),
  'down':((43,307),(87,304),225,396)},
 'Negan':{
  'idle':((226,12),(249,67),224,411),
  'walk_a':((269,12),(294,66),260,412),
  'walk_b':((269,15),(298,70),270,412),
  'palm':((173,35),(197,94),192,402),
  'kick':((204,15),(233,69),219,392),
  'special':((132,96),(159,148),205,442),
  'crouch':((228,110),(251,174),205,375),
  'hurt':((86,21),(123,73),190,362),
  'down':((24,135),(88,126),230,183)},
}


def calibrate(assets,prefix,label):
    poses=LANDMARKS[label]
    reference=math.dist(*poses['idle'][:2])
    base=assets.meta[prefix+'idle']['scale']
    for key,(crown,chin,x,ground) in poses.items():
        m=assets.meta[prefix+key]
        m['previous_scale']=m['scale'];m['previous_axis']=list(m['axis'])
        units=math.dist(crown,chin)
        m['scale']=base*max(.9,min(1.12,reference/units))
        m['axis']=[x,ground]
        m['calibration']={'crown':list(crown),'chin':list(chin),'head_units':units,'reference_head_units':reference}
        index=next(i for i,h in enumerate(assets.headers) if struct.unpack_from('<HH',h)==(m['group'],m['number']))
        fields=list(struct.unpack('<HHHHhhHBBIIHH',assets.headers[index]));fields[4:6]=[x,ground]
        assets.headers[index]=struct.pack('<HHHHhhHBBIIHH',*fields)
    return {'reference':'idle','standing_height':365,'method':'Head landmarks, pelvis and reviewed foot anchors',
            'minimum_scale_ratio':.9,'maximum_scale_ratio':1.12}
