local p={frames=2200,capture_every=60,moves={{20,75,'up'},{160,164,'a'},{450,454,'a'},{800,804,'a'},{1100,1104,'b'},{1300,1304,'down'},{1500,1504,'a'},{1800,1804,'a'}}}
p.setup=function()local sr=emu.memType.wsCartRam;emu.write16(0x7309,emu.read16(0x7309,sr)|0x100,sr)end
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))();p.tick=function(f,save,memory)o.tick(f,save,memory);if f==p.frames then o.finish(save)end end;return p
