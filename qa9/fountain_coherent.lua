local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/ending_flag_trace.lua'))();local old=p.setup
p.setup=function()
 old();local sr=emu.memType.wsCartRam;local full=os.getenv('FOUNTAIN_FULL')=='1'
 emu.write16(0x7313,emu.read16(0x7313,sr,false)|(full and 0x03f0 or 0x0090),sr)
 emu.write(0x7514,full and 45 or 15,sr);emu.write(0x7515,full and 15 or 5,sr)
end
return p
