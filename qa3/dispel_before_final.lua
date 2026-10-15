return {frames=4400,capture_every=60,setup=function()
 for i,v in ipairs({1,157,0,0,1,1,89,0,0,0}) do emu.write(0x6c9f+i-1,v,emu.memType.wsCartRam) end
end,tick=function(f,save,memory) if f==1500 or f==3000 or f==4300 then save('sram_f'..f..'.bin',memory(emu.memType.wsCartRam)) end end,moves={{60,64,'right2'},{300,304,'a'},{600,604,'down'},{800,804,'a'},{1000,1004,'a'},{1550,1554,'b'},{1650,1654,'b'},{1750,1754,'b'},{2200,2204,'right2'},{2600,2604,'a'},{3100,3104,'a'},{3500,3504,'a'}}}
