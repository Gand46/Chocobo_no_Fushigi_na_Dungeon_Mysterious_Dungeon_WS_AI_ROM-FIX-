return {frames=1800,capture_every=120,setup=function()
 for i,v in ipairs({1,157,0,0,1}) do emu.write(0x6c9f+i-1,v,emu.memType.wsCartRam) end
 
 end,tick=function(f,save,memory) if f==900 then for i,v in ipairs({1,89,0,0,0}) do emu.write(0x6ca4+i-1,v,emu.memType.wsCartRam) end end end,
 moves={{60,64,'right2'},{300,304,'a'},{430,434,'a'},{490,494,'a'},{700,704,'b'},{780,784,'b'},{850,854,'b'},
 {1000,1004,'right2'},{1120,1124,'a'},{1240,1244,'down'},{1360,1364,'a'},{1450,1454,'a'},{1600,1604,'b'},{1680,1684,'b'},{1760,1764,'b'}}}