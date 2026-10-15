-- Exact D2 pre-boss rescue, starting from the recorded dialogue checkpoint.
-- No memory writes and no script-pointer redirection in this plan.
local sr=emu.memType.wsCartRam;local frame=0;local rows={};local flags={};local capture=nil
local p={frames=4200,capture_every=30,moves={{50,4100,'a',90,4}}}
p.setup=function()
 emu.addMemoryCallback(function()
  local bank=emu.read(0x649b,sr,false);local ptr=emu.read16(0x64a1,sr,false)-1
  if bank==0xe0 and ptr>=0x9900 and ptr<0xa000 then
   rows[#rows+1]=string.format('%d,%02X:%04X,%02X',frame,bank,ptr,emu.getState()['cpu.ax']%256)
   if ptr==0x9a1c or ptr==0x9a6f or ptr==0x9ae4 or ptr==0x9b19 or ptr==0x9c11 or ptr==0x9d07 or ptr==0x9e44 then capture=string.format('event_%04X',ptr)end
  end
 end,emu.callbackType.exec,0x4d18a,0x4d18a,emu.cpuType.ws)
 emu.addMemoryCallback(function(a,v)
  local s=emu.getState();flags[#flags+1]=string.format('%d,%05X,%02X,%04X:%04X',frame,a,v,s['cpu.cs'],s['cpu.ip'])
 end,emu.callbackType.write,0x17309,0x17328,emu.cpuType.ws)
end
p.tick=function(f,save,memory)
 frame=f
 if capture then
  save(capture..'.png',emu.takeScreenshot());save(capture..'_sram.bin',memory(sr))
  local key=capture;local cb;cb=emu.addMemoryCallback(function() emu.removeMemoryCallback(cb,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws);save(key..'.mss',emu.createSavestate())end,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws);capture=nil
 end
 if f==p.frames then save('opcodes.csv','frame,script,opcode\n'..table.concat(rows,'\n'));save('flags.csv','frame,address,value,pc\n'..table.concat(flags,'\n'))end
end
return p
