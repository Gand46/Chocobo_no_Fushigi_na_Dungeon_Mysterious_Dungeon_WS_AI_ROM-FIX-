local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/../qa8/ending_progress.lua'))();local old=p.tick;local rows={};local seen={};local frame=0
p.setup=function()
 emu.addMemoryCallback(function()
  local s=emu.getState();local a=s['cpu.bx'];local mask=s['cpu.dx'];local v=emu.read16(a,emu.memType.wsCartRam,false);local bank=emu.read(0x649b,emu.memType.wsCartRam,false);local ptr=emu.read16(0x64a1,emu.memType.wsCartRam,false);local key=string.format('%02X:%04X/%04X/%04X/%04X',bank,ptr,a,mask,v)
  if seen[key] or #rows>=1000 then return end;seen[key]=true;rows[#rows+1]=string.format('%d,%s',frame,key)
 end,emu.callbackType.exec,0x4007d,0x4007d,emu.cpuType.ws)
end
p.tick=function(f,save,memory)frame=f;old(f,save,memory);if f==p.frames then save('flag_tests.txt',table.concat(rows,'\n'))end end
return p
