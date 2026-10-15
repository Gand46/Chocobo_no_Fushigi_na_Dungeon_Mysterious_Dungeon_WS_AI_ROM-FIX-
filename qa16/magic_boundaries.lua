local p={frames=1400,capture_every=60,moves={{60,64,'right2'},{130,134,'down'},{200,204,'down'},{270,274,'down'},{340,344,'down'},{410,414,'a'},{700,704,'down'},{800,804,'down'},{900,904,'down'},{1000,1004,'down'},{1200,1204,'b'}}}
p.setup=function()local sr=emu.memType.wsCartRam;for i=0,6 do emu.write(0x6c8c+i,99,sr);emu.write(0x6c85+i,255,sr);emu.write(0x6c93+i,255,sr)end end
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))();p.tick=function(f,save,memory)o.tick(f,save,memory);if f==p.frames then o.finish(save)end end;return p
