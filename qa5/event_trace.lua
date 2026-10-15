local rows={};local counts={};local frame=0
return {frames=1200,capture_every=200,moves={{120,1100,'a',60,3}},setup=function()
 local n=0;local cb
 cb=emu.addMemoryCallback(function(a,v)
  if a>=0xf0000 then return end
  local s=emu.getState();local key=string.format('%04X:%04X',s['cpu.cs'],s['cpu.ip']);counts[key]=(counts[key] or 0)+1
  if n<512 then n=n+1;rows[#rows+1]=string.format('%s ax=%04X bx=%04X cx=%04X dx=%04X si=%04X di=%04X bp=%04X ds=%04X es=%04X sp=%04X',key,s['cpu.ax'],s['cpu.bx'],s['cpu.cx'],s['cpu.dx'],s['cpu.si'],s['cpu.di'],s['cpu.bp'],s['cpu.ds'],s['cpu.es'],s['cpu.sp']) end
 if n==512 then emu.removeMemoryCallback(cb,emu.callbackType.exec,0,0xeffff,emu.cpuType.ws);local h=assert(io.open(os.getenv('QA_OUT')..'/trace_immediate.txt','w'));h:write(table.concat(rows,'\n'));h:close() end
 end,emu.callbackType.exec,0,0xeffff,emu.cpuType.ws)
end,tick=function(f,save,memory)
 if f==30 then save('trace.txt',table.concat(rows,'\n'));local c={};for k,v in pairs(counts)do c[#c+1]=string.format('%s %d',k,v)end;table.sort(c);save('counts.txt',table.concat(c,'\n'));local s=emu.getState();local t={};for k,v in pairs(s)do t[#t+1]=k..'='..tostring(v)end;table.sort(t);save('state.txt',table.concat(t,'\n')) end
end}
