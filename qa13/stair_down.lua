-- Synthetic stair placement on the next downward step; native movement opens the prompt.
local p={frames=240,capture_every=60,moves={{60,90,'down'}}}
p.setup=function()
 local sr=emu.memType.wsCartRam;local x=emu.read(0x4ac7,sr,false);local y=emu.read(0x4ac8,sr,false)+1
 emu.write16(0x24b4+y*128+x*2,0x031d,sr)
 emu.write16(0x6c7e,emu.read16(0x6c80,sr,false),sr)
end
return p
