return {frames=800,capture_every=60,setup=function()
 for i,v in ipairs({1,222,0,0,0}) do emu.write(0x6c9f+i-1,v,emu.memType.wsCartRam) end
end,moves={{60,64,'right2'},{300,304,'a'},{430,434,'a'},{550,554,'a'},{900,904,'a'},{1500,1504,'b'},{1700,1704,'b'},{2000,2020,'up'}},tick=function(f,save,memory)
 if f==720 then save('sram_f'..f..'.bin',memory(emu.memType.wsCartRam));save('wram_f'..f..'.bin',memory(emu.memType.wsWorkRam));local t={};for k,v in pairs(emu.getState()) do t[#t+1]=k..'='..tostring(v) end;table.sort(t);save('state.txt',table.concat(t,'\n')) end
end}
