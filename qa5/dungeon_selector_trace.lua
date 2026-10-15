local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/cold_trace.lua'))();local old=p.setup
p.setup=function()
old();local n=0
emu.addMemoryCallback(function(a,v)
 n=n+1;if n>12 then return end
 local s=emu.getState();local h=assert(io.open(os.getenv('QA_OUT')..'/dungeon_selector.txt','a'));h:write(string.format('value=%02X pc=%04X:%04X ds=%04X si=%04X di=%04X flags=%04X/%04X\n',v,s['cpu.cs'],s['cpu.ip'],s['cpu.ds'],s['cpu.si'],s['cpu.di'],emu.read16(0x730a,emu.memType.wsCartRam,false),emu.read16(0x730c,emu.memType.wsCartRam,false)));h:close()
end,emu.callbackType.write,0x17301,0x17301,emu.cpuType.ws)
end
return p
