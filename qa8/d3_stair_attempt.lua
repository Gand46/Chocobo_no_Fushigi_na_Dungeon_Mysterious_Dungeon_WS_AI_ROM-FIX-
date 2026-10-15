local p={frames=1500,capture_every=100,moves={{60,85,'right'},{200,245,'up'},{500,1400,'a',90,4}}}
p.tick=function(f)
 if f%30==0 then emu.write16(0x6c7e,500,emu.memType.wsCartRam)end
end
return p
