local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/damage_probe.lua'))()
local old=p.setup
p.setup=function()
 old()
 emu.write16(0x5b24,tonumber(os.getenv('ENEMY_DEFENSE')) or 0,emu.memType.wsCartRam)
end
return p
