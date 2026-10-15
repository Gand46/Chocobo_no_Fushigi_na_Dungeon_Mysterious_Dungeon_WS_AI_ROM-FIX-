-- Inputs only after a synthetic entry; trace persistent writes and actual coordinates.
local p={frames=1800,capture_every=120,moves={}}
local dirs={'left','up','right','down'}
for i=0,13 do p.moves[#p.moves+1]={60+i*120,90+i*120,dirs[i%4+1]} end
local frame=0;local writes={};local steps={};local sr=emu.memType.wsCartRam
p.setup=function()
 emu.addMemoryCallback(function(a,v)
  local s=emu.getState();writes[#writes+1]=string.format('%d,%05X,%02X,%04X:%04X',frame,a,v,s['cpu.cs'],s['cpu.ip'])
 end,emu.callbackType.write,0x175ac,0x17f8f,emu.cpuType.ws)
end
p.tick=function(f,save,memory)
 frame=f
 if f%30==0 then steps[#steps+1]=string.format('%d,%d,%d,%d,%d,%04X',f,emu.read(0x4ac7,sr,false),emu.read(0x4ac8,sr,false),emu.read16(0x7303,sr,false),emu.read16(0x6c7e,sr,false),emu.read16(0x7335,sr,false))end
 if f==p.frames then save('persistent_writes.csv','frame,address,value,pc\n'..table.concat(writes,'\n'));save('steps.csv','frame,x,y,floor,hp,event\n'..table.concat(steps,'\n'))end
end
return p
