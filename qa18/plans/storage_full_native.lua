local p={frames=1200,capture_every=30,moves={{20,50,'up'},{180,184,'down'},{260,264,'down'},{340,344,'down'},{420,424,'down'},{500,504,'down'},{580,584,'down'},{660,664,'down'},{740,744,'down'},{820,824,'down'}}}
local changed=false
emu.addMemoryCallback(function()local sr=emu.memType.wsCartRam;if not changed and emu.getState()['cpu.cs']==0x4000 and emu.read(0x649b,sr)==0xe1 and emu.read16(0x64a1,sr)==0x1da2 then emu.write(0x649b,0xe0,sr);emu.write16(0x64a1,0x11bb,sr);changed=true end end,emu.callbackType.exec,0x4d160,0x4d160,emu.cpuType.ws)
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))();p.tick=function(f,save,memory)o.tick(f,save,memory);if f==p.frames then save('injection.txt',tostring(changed));o.finish(save)end end;return p
