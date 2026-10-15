return {frames=1500,capture_every=1,setup=function()
 for i,v in ipairs({1,222,0,0,0}) do emu.write(0x6c9f+i-1,v,emu.memType.wsCartRam) end
end,moves={{60,64,'right2'},{300,304,'a'},{430,434,'a'},{550,554,'a'},{900,904,'a'},{1500,1504,'b'},{1700,1704,'b'},{2000,2020,'up'}},tick=function(f,save,memory)
 if f==540 or f==1300 then save('sram_f'..f..'.bin',memory(emu.memType.wsCartRam));save('wram_f'..f..'.bin',memory(emu.memType.wsWorkRam)) end
end}
