return {frames=1400,capture_every=200,moves={{180,184,'start'},{900,904,'down'},{1100,1104,'a'}},tick=function(f,save,memory)
 if f==1400 then save('validity.txt',string.format('%02X',emu.read(0x75b4,emu.memType.wsCartRam,false)))end
end}
