local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/../qa3/lafoss_use.lua'))();local old=p.setup;local frame=0;local counts={};local rows={};local sr=emu.memType.wsCartRam
p.setup=function()
 old();emu.write(0x6ca0,tonumber(os.getenv('ITEM_ID')) or 255,sr)
 for _,address in ipairs({0x4226c,0x4228c,0x9cc73,0x9cc99,0x9db89,0xe9a10,0x54392})do
  emu.addMemoryCallback(function()
   counts[address]=(counts[address] or 0)+1
   if counts[address]>80 then return end
   local s=emu.getState();local t={string.format('%d,%05X',frame,address)}
   for _,r in ipairs({'ax','bx','cx','dx','si','di','bp','ds','es','sp'})do t[#t+1]=string.format('%04X',s['cpu.'..r])end
   for _,a in ipairs({0x399,0x600,0x601,0x6a70,0x6b14,0x6b0d,0x6b0e})do t[#t+1]=string.format('%02X',emu.read(a,sr,false))end
   rows[#rows+1]=table.concat(t,',')
  end,emu.callbackType.exec,address,address,emu.cpuType.ws)
 end
end
local tick=p.tick
p.tick=function(f,save,memory)
 frame=f;if tick then tick(f,save,memory)end
 if f==p.frames then save('effect_trace.csv','frame,pc,ax,bx,cx,dx,si,di,bp,ds,es,sp,phase,item600,item601,item6a70,item6b14,flag6b0d,flag6b0e\n'..table.concat(rows,'\n'))end
end
return p
