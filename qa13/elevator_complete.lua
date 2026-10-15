local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/elevator_probe.lua'))()
local setup=p.setup;local tick=p.tick
p.frames=3600;p.capture_every=200
p.setup=function()setup();emu.write(0x6b0e,1,emu.memType.wsCartRam)end
p.moves={{500,1100,'a',100,4},{1800,3400,'a',100,4}}
return p
