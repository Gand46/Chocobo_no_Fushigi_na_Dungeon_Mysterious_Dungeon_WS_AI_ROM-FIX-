local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/lafoss_effect_trace.lua'))();local old=p.setup;local oldtick=p.tick;local hits={};local sr=emu.memType.wsCartRam
p.capture_every=240
p.setup=function()
 old();for _,pc in ipairs({0xe9c0a,0xea76f,0x4ca16})do
  emu.addMemoryCallback(function()
   if #hits>=60 then return end;local s=emu.getState()
   hits[#hits+1]=string.format('%05X,dx=%04X,si=%04X,di=%04X,item=%02X,hp=%04X',pc,s['cpu.dx'],s['cpu.si'],s['cpu.di'],emu.read(0x6b14,sr,false),emu.read16(0x58e3+s['cpu.si']*2,sr,false))
  end,emu.callbackType.exec,pc,pc,emu.cpuType.ws)
 end
end
p.tick=function(f,save,memory)
 oldtick(f,save,memory)
 if f>=660 and f<=810 and f%5==0 then save(string.format('detail%04d.png',f),emu.takeScreenshot())end
 if f==660 or f==810 then save('sram_f'..f..'.bin',memory(sr))end
 if f==p.frames then save('magic_dispatch.txt',table.concat(hits,'\n'))end
end
return p
