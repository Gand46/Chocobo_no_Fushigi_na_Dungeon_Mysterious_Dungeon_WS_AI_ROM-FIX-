local p={frames=1200,capture_every=100,moves={{500,1100,'a',100,4}}}
p.setup=function()
 local sr=emu.memType.wsCartRam
 emu.write(0x1fae,5,sr);emu.write(0x649b,0xe0,sr);emu.write16(0x64a1,0x2873,sr);emu.write(0x649c,0,sr);emu.write(0x649f,0x80,sr);emu.write(0x64a0,0,sr)
end
p.tick=function(f)
 if f==350 then emu.write16(0x060e,tonumber(os.getenv('TARGET_FLOOR')) or 30,emu.memType.wsCartRam)end
end
return p
