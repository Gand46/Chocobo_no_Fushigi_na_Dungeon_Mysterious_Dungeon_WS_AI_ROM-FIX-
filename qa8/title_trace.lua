local p={frames=1000,capture_every=200,moves={}};local rows={};local frame=0
p.setup=function()
 for _,pc in ipairs({0x5e1bb,0x5e232})do
  emu.addMemoryCallback(function()
   if #rows>150 then return end
   local s=emu.getState();local t={string.format('%d,%05X',frame,pc)}
   for _,r in ipairs({'ax','bx','cx','dx','si','di','ds','es','sp'})do t[#t+1]=string.format('%04X',s['cpu.'..r])end
   rows[#rows+1]=table.concat(t,',')
  end,emu.callbackType.exec,pc,pc,emu.cpuType.ws)
 end
end
p.tick=function(f,save,memory)frame=f;if f==p.frames then save('resources.csv','frame,pc,ax,bx,cx,dx,si,di,ds,es,sp\n'..table.concat(rows,'\n'))end end
return p
