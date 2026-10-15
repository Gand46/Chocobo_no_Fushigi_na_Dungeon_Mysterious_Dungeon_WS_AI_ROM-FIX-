-- POINTER_INJECTION: replace only the selector of the next native message.
-- No fabricated text, pixels, control stream, geometry or ROM modifications.
local p={frames=1050,capture_every=15,moves={{50,54,'a'},{430,434,'a'},{700,704,'a'},{950,954,'a'}}}
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))()
p.setup=function()
 local cb;cb=emu.addMemoryCallback(function()
  if emu.getState()['cpu.cs']~=0x5000 then return end
  emu.removeMemoryCallback(cb,emu.callbackType.exec,0x50e77,0x50e77,emu.cpuType.ws)
  emu.write(0x648f,0,emu.memType.wsCartRam);emu.write(0x648e,254,emu.memType.wsCartRam)
  emu.write(0x64cb,217,emu.memType.wsCartRam);emu.write16(0x67c6,0,emu.memType.wsCartRam)
 end,emu.callbackType.exec,0x50e77,0x50e77,emu.cpuType.ws)
end
p.tick=function(f,save,memory)o.tick(f,save,memory);if f==p.frames then o.finish(save)end end
return p
