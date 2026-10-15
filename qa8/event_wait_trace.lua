local p={frames=180,capture_every=180,moves={}};local rows={};local count=0
p.setup=function()
 emu.addMemoryCallback(function(a,v)
  if count>=64 then return end;count=count+1;local s=emu.getState();local t={string.format('%06X,%02X',a,v)}
  for _,r in ipairs({'cs','ip','ax','bx','cx','dx','si','di','ds','es','sp'})do t[#t+1]=string.format('%04X',s['cpu.'..r])end
  rows[#rows+1]=table.concat(t,',')
 end,emu.callbackType.read,0x15800,0x15b10,emu.cpuType.ws,emu.memType.wsPrgRom)
end
p.tick=function(f,save,memory)if f==p.frames then save('script_reads.csv',table.concat(rows,'\n'))end end
return p
