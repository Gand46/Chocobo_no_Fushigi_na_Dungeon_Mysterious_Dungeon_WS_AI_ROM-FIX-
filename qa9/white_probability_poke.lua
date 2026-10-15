local p={frames=900,capture_every=150,moves={{400,800,'a',90,4}}}
p.setup=function()emu.write(0x647,1,emu.memType.wsCartRam)end
return p
