local p={frames=1800,capture_every=100,moves={{300,304,'down'},{400,404,'a'},{700,1600,'a',100,4}}}
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))()
p.setup=function()
 local sr=emu.memType.wsCartRam
 emu.write(0x1fae,0x0a,sr);emu.write(0x1fb0,0xff,sr);emu.write16(0x1fb3,0,sr)
 emu.write(0x649b,0xe0,sr);emu.write16(0x64a1,0x1950,sr);emu.write(0x649c,0,sr);emu.write(0x649f,0x80,sr);emu.write(0x64a0,0,sr)
end
p.tick=function(f,w,m)o.tick(f,w,m);if f==p.frames then o.finish(w)end end
return p
