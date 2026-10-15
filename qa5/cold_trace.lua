local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/../qa3/cold_verified.lua'))();local old=p.tick
p.setup=function()
 local seen={}
 emu.addMemoryCallback(function(a,v)
 local s=emu.getState();local key=string.format('%04X:%04X:%05X',s['cpu.cs'],s['cpu.ip'],a)
 if seen[key] then return end;seen[key]=true
 local h=assert(io.open(os.getenv('QA_OUT')..'/save_marker_access.txt','a'));h:write(string.format('%s value=%04X ds=%04X es=%04X si=%04X di=%04X\n',key,v,s['cpu.ds'],s['cpu.es'],s['cpu.si'],s['cpu.di']));h:close()
 end,emu.callbackType.write,0x175ac,0x175b5,emu.cpuType.ws)
 for _,pc in ipairs({0x903b8,0x903f9,0x90333,0x8c813,0x9038c})do emu.addMemoryCallback(function(a,v)
 local s=emu.getState();local h=assert(io.open(os.getenv('QA_OUT')..'/calls.txt','a'));h:write(string.format('cs=%04X ip=%04X valid=%02X flags=%02X ss=%04X sp=%04X\n',s['cpu.cs'],s['cpu.ip'],emu.read(0x75b4,emu.memType.wsCartRam,false),emu.read(0x7301,emu.memType.wsCartRam,false),s['cpu.ss'],s['cpu.sp']));h:close()
 end,emu.callbackType.exec,pc,pc,emu.cpuType.ws)end
end
p.tick=function(f,save,memory)
 if old then old(f,save,memory)end
 if f==1 or f==1000 or f==3200 then save('sram_f'..f..'.bin',memory(emu.memType.wsCartRam))end
end
return p
