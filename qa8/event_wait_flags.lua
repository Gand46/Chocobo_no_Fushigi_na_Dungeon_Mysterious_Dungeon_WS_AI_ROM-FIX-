local p={frames=180,capture_every=180,moves={}};local rows={};local seen={};local sr=emu.memType.wsCartRam
p.setup=function()
 emu.addMemoryCallback(function(a,v)
  local s=emu.getState();local key=string.format('%04X:%04X',s['cpu.cs'],s['cpu.ip']);if seen[key]then return end;seen[key]=true
  if #rows>40 then return end;rows[#rows+1]=string.format('%s,a=%05X,v=%04X,ax=%04X,bx=%04X,cx=%04X,dx=%04X,si=%04X,di=%04X,ds=%04X,es=%04X',key,a,v,s['cpu.ax'],s['cpu.bx'],s['cpu.cx'],s['cpu.dx'],s['cpu.si'],s['cpu.di'],s['cpu.ds'],s['cpu.es'])
 end,emu.callbackType.read,0x17335,0x17336,emu.cpuType.ws)
end
p.tick=function(f,save,memory)if f==p.frames then save('flag_reads.txt',table.concat(rows,'\n'));save('flags.bin',memory(sr):sub(0x7301,0x7380))end end
return p
