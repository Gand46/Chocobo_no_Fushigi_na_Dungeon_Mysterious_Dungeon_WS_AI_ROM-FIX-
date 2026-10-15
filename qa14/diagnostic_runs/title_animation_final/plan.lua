local p={frames=1400,capture_every=0x7fffffff,moves={}};local rows={}
p.tick=function(f,save,memory)
 if f>=300 and f<=1300 then
  save(string.format('anim%05d.png',f),emu.takeScreenshot())
  local a={};for y=2,7 do for x=11,16 do local v=emu.read16(0x1000+(y*32+x)*2,emu.memType.wsWorkRam,false);a[#a+1]=string.format('%04X',v)end end
  rows[#rows+1]=f..','..table.concat(a,';')
 end
 if f==p.frames then save('animation_map.csv','frame,cells\n'..table.concat(rows,'\n')) end
end
return p
