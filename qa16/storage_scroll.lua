local p={frames=1500,capture_every=60,moves={{60,64,'right2'},{420,424,'down'},{540,544,'down'},{660,664,'down'},{780,784,'down'},{900,904,'down'},{1020,1024,'down'},{1140,1144,'down'},{1260,1264,'down'}}}
local changed=false
emu.addMemoryCallback(function()local sr=emu.memType.wsCartRam;if not changed and emu.getState()['cpu.cs']==0x3000 and emu.read(0x641a,sr)==3 then emu.write(0x641a,32,sr);changed=true end end,emu.callbackType.exec,0x342be,0x342be,emu.cpuType.ws)
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))();p.tick=function(f,save,memory)o.tick(f,save,memory);if f==p.frames then save('injection.txt',tostring(changed));o.finish(save)end end;return p
