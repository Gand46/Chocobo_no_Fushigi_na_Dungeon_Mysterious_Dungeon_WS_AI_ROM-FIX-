local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/whistle_dump.lua'))();local old=p.setup;p.setup=function()
 old();local count=0
 emu.addMemoryCallback(function(a,v)
 if a==0x3800 or a==0x3a40 or a==0x3a50 then
 count=count+1;if count<20 then local s=emu.getState();local h=assert(io.open(os.getenv('QA_OUT')..'/writes.txt','a'));h:write(string.format('addr=%04X val=%04X cs=%04X ip=%04X ds=%04X si=%04X es=%04X di=%04X cx=%04X bank2=%02X bank3=%02X\n',a,v,s['cpu.cs'],s['cpu.ip'],s['cpu.ds'],s['cpu.si'],s['cpu.es'],s['cpu.di'],s['cpu.cx'],s['cart.selectedBanks2'],s['cart.selectedBanks3']));h:close() end
 end
 end,emu.callbackType.write,0x3800,0x3a5f,emu.cpuType.ws)
end
return p
