-- Causal control on JP: same post-Telep state and native elevator caller.
-- The only extra intervention is replacing the cached digits 99 with target 30.
local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/elevator_causal_trace.lua'))()
local old=p.setup
p.setup=function()
 old();local sr=emu.memType.wsCartRam
 for i,v in ipairs({0,3,0,0,0})do emu.write(0x7539+i,v,sr)end
end
return p
