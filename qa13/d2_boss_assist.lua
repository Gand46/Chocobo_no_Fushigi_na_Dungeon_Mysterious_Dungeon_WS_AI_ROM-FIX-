local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/event_progress.lua'))();local old=p.tick;local sr=emu.memType.wsCartRam
p.frames=4800;p.capture_every=400;p.moves={{60,130,'up'},{240,4700,'a',60,4}}
p.setup=function()
 -- Explicit synthetic combat assistance, never a natural fight claim.
 emu.write16(0x5a32,1,sr)
 emu.write16(0x6c7e,500,sr);emu.write16(0x6c80,500,sr)
end
p.tick=function(f,save,memory)
 old(f,save,memory)
 if f%60==0 then emu.write16(0x6c7e,500,sr)end
end
return p
