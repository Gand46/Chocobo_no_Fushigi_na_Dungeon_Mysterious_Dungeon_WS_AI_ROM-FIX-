-- Native preset/monster-selector fixture; initializer and consumer preserved.
local p={frames=600,capture_every=60,moves={{60,64,'right2'},{180,184,'down'},{250,254,'down'},{320,324,'down'},{390,394,'down'},{460,464,'down'}}}
local changed=false
local scroll=false
p.setup=function()
 emu.addMemoryCallback(function()
  local sr=emu.memType.wsCartRam
  if not changed and emu.getState()['cpu.cs']==0x3000 and emu.read(0x641a,sr)==3 then
   emu.write(0x641a,0x81,sr);emu.write(0x2000,63,sr);emu.write(0x2001,0,sr);changed=true
  end
 end,emu.callbackType.exec,0x342be,0x342be,emu.cpuType.ws)
 emu.addMemoryCallback(function() if emu.getState()['cpu.cs']==0x3000 then emu.write(0x64c4,1,emu.memType.wsCartRam);scroll=true end end,emu.callbackType.exec,0x36526,0x36526,emu.cpuType.ws)
 
end
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))()
p.tick=function(f,save,memory)o.tick(f,save,memory);if f==p.frames then save('injection.txt',tostring(changed));save('scroll_fixture.txt',tostring(scroll));o.finish(save)end end
return p
