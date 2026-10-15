local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/elevator_caller.lua'))()
local old=p.setup;local tick=p.tick;local frame=0;local writes={}
p.setup=function()
 old()
 emu.addMemoryCallback(function(a,v)
  local s=emu.getState();writes[#writes+1]=string.format('%d,%05X,%02X,%04X:%04X',frame,a,v,s['cpu.cs'],s['cpu.ip'])
 end,emu.callbackType.write,0x175ac,0x17f8f,emu.cpuType.ws)
end
p.tick=function(f,save,memory)
 frame=f;tick(f,save,memory)
 if f==p.frames then save('persistent_writes.csv','frame,address,value,pc\n'..table.concat(writes,'\n'))end
end
return p
