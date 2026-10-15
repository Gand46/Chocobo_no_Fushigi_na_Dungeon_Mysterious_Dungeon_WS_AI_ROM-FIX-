return {frames=250,capture_every=5,moves={{30,34,'a'}},tick=function(f,save,memory)
 if f==25 or f==40 then save('sram_f'..f..'.bin',memory(emu.memType.wsCartRam));local s=emu.getState();local h={};for k,v in pairs(s) do h[#h+1]=k..'='..tostring(v) end;table.sort(h);save('state_f'..f..'.txt',table.concat(h,'\n')) end
end}
