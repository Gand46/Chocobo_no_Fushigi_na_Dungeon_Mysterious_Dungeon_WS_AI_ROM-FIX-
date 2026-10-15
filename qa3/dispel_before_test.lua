return {frames=3800,capture_every=60,setup=function()
 for i,v in ipairs({1,157,0,0,1}) do emu.write(0x6c9f+i-1,v,emu.memType.wsCartRam) end
 for i,v in ipairs({1,89,0,0,0}) do emu.write(0x6ca4+i-1,v,emu.memType.wsCartRam) end
 end,tick=function(f,save,memory) if f==2100 then  end end,
 moves={{60,64,'right2'},{300,304,'a'},{430,434,'a'},{490,494,'a'},{700,704,'b'},{780,784,'b'},{850,854,'b'},
 {2400,2404,'right2'},{2520,2524,'a'},{2640,2644,'down'},{2760,2764,'a'},{2850,2854,'a'},{3000,3004,'b'},{3080,3084,'b'},{3160,3164,'b'}}}