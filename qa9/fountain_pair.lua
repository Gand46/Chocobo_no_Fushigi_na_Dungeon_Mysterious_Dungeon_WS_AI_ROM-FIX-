local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/ending_flag_trace.lua'))();local old=p.setup
p.setup=function()
 old();local sr=emu.memType.wsCartRam
 emu.write16(0x7311,emu.read16(0x7311,sr,false)|0x2000,sr)
 emu.write16(0x730b,emu.read16(0x730b,sr,false)|0x0004,sr)
end
return p
