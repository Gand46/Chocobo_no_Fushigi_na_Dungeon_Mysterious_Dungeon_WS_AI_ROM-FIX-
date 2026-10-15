local p={frames=7200,capture_every=60,moves={{50,7100,'a',60,4}}}
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))();local f=0;local writers={}
local cb=emu.addMemoryCallback(function(a,v)
 if f<1 then return end
 local s=emu.getState();local k=string.format('%04X:%04X',s['cpu.cs'],s['cpu.ip'])
 local w=writers[k];if not w then w={first=f,last=f,count=0,min=a,max=a};writers[k]=w end
 w.last=f;w.count=w.count+1;w.min=math.min(w.min,a);w.max=math.max(w.max,a)
end,emu.callbackType.write,0x2000,0x3fff,emu.cpuType.ws)
p.tick=function(frame,save,memory)
 f=frame;o.tick(f,save,memory)
 if f==4250 then emu.removeMemoryCallback(cb,emu.callbackType.write,0x2000,0x3fff,emu.cpuType.ws)end
 if f==p.frames then
  local lines={'pc,first_frame,last_frame,writes,min_address,max_address'}
  for k,v in pairs(writers)do lines[#lines+1]=string.format('%s,%d,%d,%d,%04X,%04X',k,v.first,v.last,v.count,v.min,v.max)end
  table.sort(lines);save('credits_writers.csv',table.concat(lines,'\n'));o.finish(save)
 end
end
return p
