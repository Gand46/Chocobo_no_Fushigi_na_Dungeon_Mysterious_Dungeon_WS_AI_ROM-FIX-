"""Native English 16x16 digraph map, verified against HF13 font atlas.
No font replacement. Each emitted word occupies one 16-pixel story cell.
"""
from functools import lru_cache
import string
MAP={}
def put(t,g):MAP.setdefault(t,[]).append(g)
for ch,base in [('a',1),('b',0x21),('c',0x41),('d',0x61),('e',0x81),('g',0xf7),('h',0x117),('i',0x137),('j',0x157),('k',0x177),('l',0x197),('m',0x1b7),('n',0x1d7),('o',0x1f7),('p',0x217),('r',0x238),('s',0x258),('t',0x278),('u',0x298),('v',0x2b8),('w',0x2d8)]:
 for i,z in enumerate(' '+string.ascii_lowercase+".,'!?"):
  g=base+i
  if g in [0x7a,0x7b,0x81,0x96,0x137,0x143,0x2c9]:continue
  put(ch+z,g)
put('f ',0xa1);put('fa',0xa2)
for i,z in enumerate(string.ascii_lowercase[1:]+".,'!?"):put('f'+z,0xd9+i)
for t,g in [('xa',0x2f9),('xb',0x2fa),('xc',0x2fb),('xd',0x2fc),('xe',0x2fd),('xh',0x300),('xi',0x301),('xo',0x307),('xp',0x308),('xx',0x313),('xy',0x314),('xz',0x315),('ya',0x319),('yb',0x31a),('yc',0x31b),('yd',0x31c),('ye',0x31d),('yf',0x31e),('yk',0x324),('yl',0x325),('yp',0x32a),('yq',0x32b),('ys',0x32d),('yu',0x32f),('yw',0x330),('za',0x339),('zb',0x33a),('zc',0x33b),('zd',0x33c),('ze',0x33d),('zi',0x341),('zw',0x350),('zx',0x351),('zy',0x352),('zz',0x353),('il',0x7a),('dy',0x143)]:put(t,g)
for ch,g in zip(string.ascii_lowercase,[1,0xb8,0xb9,0xba,0xbb,0xbc,0xbd,*range(0x358,0x36b)]):put(ch,g)
for i,ch in enumerate(string.ascii_uppercase):put(ch,0xbf+i)
for i,ch in enumerate(string.digits):put(ch,0xa3+i)
for ch,g in [(' ',0),('.',0xb7),(',',0xb5),('!',0xad),('?',0xae),('-',0xaf),('+',0xb0),('(',0xb2),(')',0xb3),("'",0x154)]:
 if ch!="'":put(ch,g) # apostrophe only in verified digraphs, not an invented single.
# Word-final left-side glyphs: legacy B8..BD/358..36A are right-side letters.
for ch,g in [('a',1),('b',0x21),('c',0x41),('d',0x61),('e',0x302),('f',0xa1),('g',0xf7),('h',0x117),('i',0x2c9),('j',0x157),('k',0x177),('l',0x197),('m',0x1b7),('n',0x1d7),('o',0x1f7),('p',0x217),('r',0x238),('s',0x258),('t',0x278),('u',0x298),('v',0x2b8),('w',0x2d8),('y',0x318)]:
 MAP[ch]=[g]
 MAP[ch+' ']=[g]
RIGHT_SINGLE=dict(zip(string.ascii_lowercase,[0xb6,0xb8,0xb9,0xba,0xbb,0xbc,0xbd,*range(0x358,0x36b)]))
# Correct the irregular y row; unavailable yo is rendered with a right-side y.
for token in list(MAP):
 if len(token)==2 and token[0]=='y' and token[1]!=' ':del MAP[token]
for token,g in [('ya',0x319),('yb',0x31a),('yc',0x31b),('yd',0x31c),('ye',0x31d),('yf',0x31e),('yk',0x323),('yl',0x324),('yn',0x326),('yp',0x328),('yr',0x32a),('ys',0x32b),('yt',0x32c),('yu',0x32d),('yv',0x32e),('yw',0x32f),('yx',0x330)]:MAP[token]=[g]
@lru_cache(None)
def _encode(s):
 if not s:return (0,())
 choices=[]
 for token,gs in MAP.items():
  if s.startswith(token):
   rest=s[len(token):];tail=_encode(rest)
   if tail is not None:
    penalty=int(len(token)==1 and token.islower() and bool(rest) and (rest[0].islower() or rest[0]=="'"))
    for g in ([RIGHT_SINGLE[token]] if penalty else gs):choices.append((penalty+tail[0],(g,)+tail[1]))
 return min(choices,key=lambda z:(z[0],len(z[1]),z[1])) if choices else None
def encode(s):
 v=_encode(s)
 return v[1] if v is not None else None

def line(s):
 v=encode(s)
 if v is None:raise ValueError('Unencodable '+repr(s))
 if len(v)>13:raise ValueError(f'Over13 cells ({len(v)}): {s}')
 return list(v)
def pages(pages):
 out=[]
 for j,p in enumerate(pages):
  for i,s in enumerate(p):
   if i:out.append(0xfffe)
   out.extend(line(s))
  out.append(0xfff2)
  if j+1<len(pages):out.append(0xfffd)
 return out+[0xffff]
