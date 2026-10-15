local n=0;local cb;local rows={'n,cs,ip,ss,sp,ax,bx,cx,dx,si,di'}
return {frames=120,capture_every=60,setup=function()
 cb=emu.addMemoryCallback(function()
  n=n+1;local s=emu.getState();rows[#rows+1]=string.format('%d,%04X,%04X,%04X,%04X,%04X,%04X,%04X,%04X,%04X,%04X',n,s['cpu.cs'],s['cpu.ip'],s['cpu.ss'],s['cpu.sp'],s['cpu.ax'],s['cpu.bx'],s['cpu.cx'],s['cpu.dx'],s['cpu.si'],s['cpu.di'])
  if n==2048 then emu.removeMemoryCallback(cb,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws) end
 end,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws)
end,tick=function(f,save,memory)
 if f==60 then local t={};for k,v in pairs(emu.getState()) do t[#t+1]=k..'='..tostring(v) end;table.sort(t);save('state.txt',table.concat(t,'\n'));save('trace.csv',table.concat(rows,'\n')) end
end}
