local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/../qa3/whistle_use.lua'))();p.frames=2400
local old=p.tick
p.tick=function(f,save,memory)
 old(f,save,memory)
 if f==720 then save('wram_animation.bin',memory(emu.memType.wsWorkRam));save('sram_animation.bin',memory(emu.memType.wsCartRam)) end
end
return p
