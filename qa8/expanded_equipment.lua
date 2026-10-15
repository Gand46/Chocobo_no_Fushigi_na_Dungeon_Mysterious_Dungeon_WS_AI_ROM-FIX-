local p={frames=1600,capture_every=200,moves={{60,64,'right2'},{300,304,'a'},{840,844,'a'},{885,889,'down'},{920,924,'down'},{955,959,'down'},{1005,1009,'a'},{1240,1244,'b'},{1320,1324,'b'},{1400,1404,'b'}}}
local sr=emu.memType.wsCartRam;local frame=0;local rows={};local guards={};local touched={};local case=tonumber(os.getenv('EQUIP_ID')) or 192;local slot=tonumber(os.getenv('EQUIP_SLOT')) or 17
p.moves[#p.moves+1]={430,430+slot*18,'down',18,4}
p.setup=function()
 emu.write(0x6c9e,18,sr)
 for k=0,17 do for i,v in ipairs({1,k==slot and case or 0x65,k==slot and 99 or 0,0,0})do emu.write(0x6c9f+k*5+i-1,v,sr)end end
 for _,pc in ipairs({0x37aff,0x37b7d})do emu.addMemoryCallback(function()
  local s=emu.getState();if s['cpu.cs']==0x3000 and s['cpu.di']>=0x23c and #guards<40 then guards[#guards+1]=string.format('%d,%05X,%04X',frame,pc,s['cpu.di'])end
 end,emu.callbackType.exec,pc,pc,emu.cpuType.ws)end
 emu.addMemoryCallback(function(a,v)if #touched<64 then local s=emu.getState();touched[#touched+1]=string.format('%d,%04X:%04X,%05X,%02X',frame,s['cpu.cs'],s['cpu.ip'],a,v)end end,emu.callbackType.write,0x175ac,0x17f8f,emu.cpuType.ws)
end
p.tick=function(f,save,memory)
 frame=f
 if f==820 or f==1180 then save('selection'..f..'.png',emu.takeScreenshot());save('sram'..f..'.bin',memory(sr))end
 if f==p.frames then save('buffer_guard.csv',table.concat(guards,'\n'));save('save_writes.csv',table.concat(touched,'\n'))end
end
return p
