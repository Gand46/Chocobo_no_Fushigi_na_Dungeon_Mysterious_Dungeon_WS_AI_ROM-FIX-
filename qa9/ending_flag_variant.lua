local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/ending_flag_trace.lua'))();local old=p.setup
p.setup=function()
 old();local a=tonumber(os.getenv('FLAG_ADDR')) or 0x7311;local mask=tonumber(os.getenv('FLAG_MASK')) or 0x2000;local sr=emu.memType.wsCartRam
 emu.write16(a,emu.read16(a,sr,false)|mask,sr)
end
return p
