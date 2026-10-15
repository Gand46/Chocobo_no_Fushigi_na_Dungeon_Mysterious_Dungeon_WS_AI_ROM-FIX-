local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/../qa3/lafoss_use.lua'))();local old=p.setup
p.setup=function()
 old();local h=assert(io.open(os.getenv('SAVE_FIXTURE'),'rb'));local data=h:read('*a');h:close()
 for a=0x75ac,0x7f89 do emu.write(a,string.byte(data,a+1),emu.memType.wsCartRam)end
 local out=assert(io.open(os.getenv('QA_OUT')..'/protected_save_writes.txt','w'));out:write('method=SYNTHETIC_EXISTING_NATIVE_SAVE_BLOCK; watch=175AC..17F89\n');out:flush();local n=0
 emu.addMemoryCallback(function(a,v)
 n=n+1;if n<=50 then local s=emu.getState();out:write(string.format('%05X=%04X pc=%04X:%04X\n',a,v,s['cpu.cs'],s['cpu.ip']));out:flush()end
 end,emu.callbackType.write,0x175ac,0x17f89,emu.cpuType.ws)
end
return p
