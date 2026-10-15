local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/lafoss_use.lua'))();local old=p.setup
p.setup=function()
 old();local n=0
 emu.addMemoryCallback(function()
  local s=emu.getState();if s['cpu.dx']==0xffff and n<8 then
   n=n+1;local h=assert(io.open(os.getenv('QA_OUT')..'/invalid_descriptor.txt','a'));h:write(string.format('cs=%04X ip=%04X ax=%04X cx=%04X dx=%04X di=%04X es=%04X sp=%04X\n',s['cpu.cs'],s['cpu.ip'],s['cpu.ax'],s['cpu.cx'],s['cpu.dx'],s['cpu.di'],s['cpu.es'],s['cpu.sp']));h:close()
  end
 end,emu.callbackType.exec,0x543a1,0x543a1,emu.cpuType.ws)
end
return p
