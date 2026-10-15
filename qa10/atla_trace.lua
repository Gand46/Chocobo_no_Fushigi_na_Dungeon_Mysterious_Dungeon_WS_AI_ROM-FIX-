local sr=emu.memType.wsCartRam;local frame=0;local rows={};local flags={};local seen={}
local p={frames=10000,capture_every=60,moves={{60,130,'up'},{240,9900,'a',180,4}}}
p.setup=function()
 emu.write16(0x5a32,1,sr);emu.write16(0x6c7e,500,sr);emu.write16(0x6c80,500,sr)
 emu.addMemoryCallback(function()
  local bank=emu.read(0x649b,sr,false);local ptr=emu.read16(0x64a1,sr,false)-1
  local key=string.format('%02X:%04X',bank,ptr)
  if #rows<20000 then rows[#rows+1]=string.format('%d,%s,%02X',frame,key,emu.getState()['cpu.ax']%256)end
 end,emu.callbackType.exec,0x4d18a,0x4d18a,emu.cpuType.ws)
 emu.addMemoryCallback(function(a,v)
  local s=emu.getState();flags[#flags+1]=string.format('%d,%05X,%02X,%04X:%04X',frame,a,v,s['cpu.cs'],s['cpu.ip'])
 end,emu.callbackType.write,0x17309,0x17328,emu.cpuType.ws)
end
p.tick=function(f,save,memory)
 frame=f;if f%60==0 then emu.write16(0x6c7e,500,sr)end
 if f==p.frames then save('opcodes.csv','frame,script,opcode\n'..table.concat(rows,'\n'));save('flags.csv','frame,address,value,pc\n'..table.concat(flags,'\n'))end
end
return p
