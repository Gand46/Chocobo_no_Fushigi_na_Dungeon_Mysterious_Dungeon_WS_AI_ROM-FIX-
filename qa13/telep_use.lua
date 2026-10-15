local p={frames=2200,capture_every=110,moves={{60,64,'right2'},{300,304,'a'},{430,434,'a'},{550,554,'a'},{850,2150,'a',90,4}}}
p.setup=function()for i,v in ipairs({1,0x0b,0,0,0})do emu.write(0x6c9f+i-1,v,emu.memType.wsCartRam)end end
return p
