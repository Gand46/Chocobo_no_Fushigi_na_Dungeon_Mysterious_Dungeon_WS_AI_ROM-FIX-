local p={frames=60,capture_every=60,moves={}};local counts={};local first={};local n=0;local cb
p.setup=function()
 cb=emu.addMemoryCallback(function()
  local s=emu.getState();local pc=s['cpu.cs']*16+s['cpu.ip'];n=n+1;counts[pc]=(counts[pc] or 0)+1
  if #first<100 then first[#first+1]=string.format('%05X,ax=%04X,bx=%04X,cx=%04X,dx=%04X,si=%04X,di=%04X,ds=%04X,es=%04X,sp=%04X',pc,s['cpu.ax'],s['cpu.bx'],s['cpu.cx'],s['cpu.dx'],s['cpu.si'],s['cpu.di'],s['cpu.ds'],s['cpu.es'],s['cpu.sp'])end
  if n==150000 then emu.removeMemoryCallback(cb,emu.callbackType.exec,0,0xeffff,emu.cpuType.ws)end
 end,emu.callbackType.exec,0,0xeffff,emu.cpuType.ws)
end
p.tick=function(f,save,memory)
 if f==60 then local rows={};for pc,c in pairs(counts)do rows[#rows+1]={pc=pc,c=c}end;table.sort(rows,function(a,b)return a.c>b.c end);local t={};for i=1,math.min(100,#rows)do t[#t+1]=string.format('%05X,%d',rows[i].pc,rows[i].c)end;save('counts.csv',table.concat(t,'\n'));save('first.txt',table.concat(first,'\n'))end
end
return p
