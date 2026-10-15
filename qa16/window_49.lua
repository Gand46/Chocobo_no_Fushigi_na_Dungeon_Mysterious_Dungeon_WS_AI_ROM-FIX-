local p={frames=420,capture_every=60,moves={{60,64,'right2'}}}
local changed=false
emu.addMemoryCallback(function()local sr=emu.memType.wsCartRam;if not changed and emu.getState()['cpu.cs']==0x3000 and emu.read(0x641a,sr)==3 then emu.write(0x641a,49,sr);changed=true end end,emu.callbackType.exec,0x342be,0x342be,emu.cpuType.ws)
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))();p.tick=function(f,save,memory)o.tick(f,save,memory);if f==p.frames then save('injection.txt',tostring(changed));o.finish(save)end end;return p
