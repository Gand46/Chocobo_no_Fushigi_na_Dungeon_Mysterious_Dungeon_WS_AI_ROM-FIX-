local p={frames=300,capture_every=300,moves={}};local rows={};local seen={}
p.setup=function()
 emu.addMemoryCallback(function(a,v)
  local s=emu.getState();local key=string.format('%04X:%04X',s['cpu.cs'],s['cpu.ip']);if seen[key] then return end;seen[key]=true
  if #rows>50 then return end;local t={key,string.format('%04X,%04X',a,v)}
  for _,r in ipairs({'ax','bx','cx','dx','si','di','ds','es'})do t[#t+1]=string.format('%04X',s['cpu.'..r])end
  for i=0,3 do t[#t+1]=string.format('%02X',s['cart.selectedBanks'..i] or 0)end
  rows[#rows+1]=table.concat(t,',')
 end,emu.callbackType.write,0x2000,0x3fff,emu.cpuType.ws)
end
p.tick=function(f,save,memory)if f==p.frames then save('writes.csv',table.concat(rows,'\n'))end end
return p
