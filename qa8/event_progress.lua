local p={frames=3600,capture_every=600,moves={{50,3500,'a',90,4}}};local rows={};local seen={};local frame=0;local sr=emu.memType.wsCartRam
p.tick=function(f,save,memory)
 frame=f
 if f%60==0 then
  local bank=emu.read(0x649b,sr,false);local ptr=emu.read16(0x64a1,sr,false);local key=string.format('%02X:%04X',bank,ptr)
  if not seen[key] then seen[key]=true;rows[#rows+1]=string.format('%d,%s,%s',f,key,(memory(sr):sub(0x730a,0x7315):gsub('.',function(c)return string.format('%02X',c:byte())end)))end
 end
 if f==p.frames then save('script_states.csv','frame,script,flags\n'..table.concat(rows,'\n'))end
end
return p
