local p=assert(loadfile(os.getenv('TAIL_PLAN')))();local old=p.setup;local rows={}
p.setup=function()
 if old then old()end
 for _,ty in ipairs({'read','write'})do
  emu.addMemoryCallback(function(a,v)
   if #rows<100 then local s=emu.getState();rows[#rows+1]=string.format('%s,%04X:%04X,%05X,%04X',ty,s['cpu.cs'],s['cpu.ip'],a,v)end
  end,emu.callbackType[ty],0x17f8a,0x17f8f,emu.cpuType.ws)
 end
end
local tick=p.tick
p.tick=function(f,save,memory)
 if tick then tick(f,save,memory)end
 if f==p.frames then save('tail_access.csv','type,pc,address,value\n'..table.concat(rows,'\n'))end
end
return p
