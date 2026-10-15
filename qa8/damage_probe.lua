local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/lafoss_detailed.lua'))();local old=p.setup;local oldtick=p.tick;local rows={};local sr=emu.memType.wsCartRam
p.setup=function()
 old()
 for _,pc in ipairs({0xe9c0a,0x4ca16,0x4ca65,0x4cab9,0x4ca3d,0xe9c62})do
  emu.addMemoryCallback(function()
   if #rows>60 then return end;local s=emu.getState();rows[#rows+1]=string.format('%05X,dx=%04X,si=%04X,flags=%04X,damage=%d,defense=%d',pc,s['cpu.dx'],s['cpu.si'],emu.read16(0x62f,sr,false),emu.read16(0x4c67,sr,false),emu.read16(0x5b22+s['cpu.si']*2,sr,false))
  end,emu.callbackType.exec,pc,pc,emu.cpuType.ws)
 end
end
p.tick=function(f,save,memory)oldtick(f,save,memory);if f==p.frames then save('damage.txt',table.concat(rows,'\n'))end end
return p
