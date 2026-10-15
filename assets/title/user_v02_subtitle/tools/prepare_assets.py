"""Compile authored masters to native pixel assets. No image generation API required."""
from pathlib import Path
import json
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAL = np.array([[36,36,0],[146,146,170],[182,182,170],[219,219,170]],dtype=np.int32)

def indices(im):
    a = np.array(im.convert('RGB')).astype(np.int32)
    return np.argmin(((a[:,:,None,:]-PAL)**2).sum(axis=3),axis=2).astype('uint8')

def indexed(a):
    im=Image.fromarray(a.astype('uint8'), 'P')
    im.putpalette(PAL.astype('uint8').ravel().tolist()+[0]*756)
    return im

def main():
    a=ROOT/'assets'; a.mkdir(exist_ok=True)
    logo=Image.open(ROOT/'authoring/wordmark_master.png').convert('RGBA')
    y,x=np.where(np.array(logo.getchannel('A'))>127)
    box=[int(x.min()),int(y.min()),int(x.max())+1,int(y.max())+1]
    logo=logo.crop(box).resize((156,42),Image.Resampling.NEAREST)
    li=indices(logo); alpha=np.array(logo.getchannel('A'))>127
    # Opaque four-color pixels plus a separate binary transparency mask.
    indexed(li).save(a/'wordmark_indices.png',bits=2)
    Image.fromarray((alpha*255).astype('uint8')).save(a/'wordmark_mask.png')
    rgba=np.dstack((PAL[li].astype('uint8'),(alpha*255).astype('uint8')))
    Image.fromarray(rgba,'RGBA').save(a/'wordmark_native.png')
    bg=Image.open(ROOT/'authoring/backplate_master.png').resize((224,144),Image.Resampling.NEAREST)
    indexed(indices(bg)).save(a/'backplate_native.png',bits=2)
    sub=Image.open(ROOT/'authoring/subtitle_master.png').crop((453,817,1116,899)).resize((94,12),Image.Resampling.NEAREST)
    indexed(indices(sub)).save(a/'subtitle_native.png',bits=2)
    config={'size':[224,144], 'palette_rgb':PAL.tolist(), 'palette_semantics':'display colors sampled from GIF, not verified hardware palette registers',
      'wordmark_xy':[34,64], 'wordmark_size':[156,42], 'subtitle_xy':[65,109],
      'backplate_rows':[56,104], 'clear_rows':[104,121], 'wordmark_master_crop':box,
      'subtitle_master_crop':[453,817,1116,899], 'sampling':'nearest neighbor',
      'transparency':'separate 1-bit mask, alpha threshold 128', 'version':'0.1-ART-REVIEW'}
    (a/'layout.json').write_text(json.dumps(config,indent=2)+'\n')
    print('Prepared editable native assets.')

if __name__=='__main__': main()
