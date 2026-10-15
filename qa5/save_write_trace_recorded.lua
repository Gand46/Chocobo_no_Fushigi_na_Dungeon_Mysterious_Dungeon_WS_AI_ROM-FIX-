local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/../qa3/save_yes_trace.lua'))();local old=p.tick;local rows={};local seen={}
p.setup=function()
 emu.addMemoryCallback(function(a,v)
 local s=emu.getState();local key=string.format('%04X:%04X',s['cpu.cs'],s['cpu.ip']);local z=seen[key] or {count=0,min=a,max=a};seen[key]=z;z.count=z.count+1;z.min=math.min(z.min,a);z.max=math.max(z.max,a)
 if z.count<=2 then local h=assert(io.open(os.getenv('QA_OUT')..'/writes.txt','a'));h:write(string.format('%s a=%05X value=%04X ax=%04X bx=%04X cx=%04X dx=%04X si=%04X di=%04X ds=%04X es=%04X\n',key,a,v,s['cpu.ax'],s['cpu.bx'],s['cpu.cx'],s['cpu.dx'],s['cpu.si'],s['cpu.di'],s['cpu.ds'],s['cpu.es']));h:close() end
 end,emu.callbackType.write,0x17500,0x17fff,emu.cpuType.ws)
end
p.tick=function(f,save,memory)
 old(f,save,memory)
 if f==250 then local t={};for k,v in pairs(seen)do t[#t+1]=string.format('%s count=%d min=%05X max=%05X',k,v.count,v.min,v.max)end;table.sort(t);save('write_summary.txt',table.concat(t,'\n'))end
end
return p
