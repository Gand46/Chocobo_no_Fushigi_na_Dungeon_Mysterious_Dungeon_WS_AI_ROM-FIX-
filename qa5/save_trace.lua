local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/../qa3/cold_verified.lua'))();local frame=0;local stats={};local first={}
p.setup=function()
 for _,ty in ipairs({'read','write'}) do
 emu.addMemoryCallback(function(a,v)
  local s=emu.getState();local key=string.format('%s,%04X:%04X',ty,s['cpu.cs'],s['cpu.ip']);local z=stats[key]
  if not z then z={n=0,lo=a,hi=a,first=frame,last=frame};stats[key]=z end;z.n=z.n+1;z.lo=math.min(z.lo,a);z.hi=math.max(z.hi,a);z.last=frame
  if ty=='write' and a<0x10020 and #first<80 then first[#first+1]=string.format('%d,%s,%05X,%04X',frame,key,a,v) end
 end,emu.callbackType[ty],0x10000,0x14fff,emu.cpuType.ws)
 end
end
p.tick=function(f,save,memory)
 frame=f
 if f==1 or f==100 or f==1000 or f==2900 or f==3000 or f==4300 then save('sram_f'..f..'.bin',memory(emu.memType.wsCartRam)) end
 if f==p.frames then
 local rows={'type,pc,count,low,high,first_frame,last_frame'};for k,z in pairs(stats) do rows[#rows+1]=string.format('%s,%d,%05X,%05X,%d,%d',k,z.n,z.lo,z.hi,z.first,z.last) end;table.sort(rows);save('memory_access.csv',table.concat(rows,'\n'));save('header_writes.csv',table.concat(first,'\n'))
 end
end
return p
