-- Synthetic entry to native staircase menu E0:1950 (script 0A).
-- No edit of live payload or stored payload; choices, save and transition are native.
local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/save_native_trace.lua'))()
local old=p.setup;p.frames=1800;p.moves={{300,304,'down'},{400,404,'a'},{700,1600,'a',100,4}}
p.setup=function()
 local sr=emu.memType.wsCartRam
 emu.write(0x1fae,0x0a,sr);emu.write(0x1fb0,0xff,sr);emu.write16(0x1fb3,0,sr)
 emu.write(0x649b,0xe0,sr);emu.write16(0x64a1,0x1950,sr);emu.write(0x649c,0,sr);emu.write(0x649f,0x80,sr);emu.write(0x64a0,0,sr)
 old()
 local function dump(name)local t={};for i=0,32767 do t[#t+1]=string.char(emu.read(i,sr,false))end;local h=assert(io.open(os.getenv('QA_OUT')..'/'..name,'wb'));h:write(table.concat(t));h:close()end
 emu.addMemoryCallback(function()dump('before_copy.sav')end,emu.callbackType.exec,0x90373,0x90373,emu.cpuType.ws)
 emu.addMemoryCallback(function()dump('after_copy.sav')end,emu.callbackType.exec,0x9037f,0x9037f,emu.cpuType.ws)
end
return p
