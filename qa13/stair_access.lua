local p={frames=1700,capture_every=100,moves={{60,78,'up'},{200,1600,'a',100,4}}}
p.setup=function()
 local sr=emu.memType.wsCartRam;local x=emu.read(0x4ac7,sr,false);local y=emu.read(0x4ac8,sr,false)-1
 emu.write16(0x24b4+y*128+x*2,0x031d,sr)
end
return p
