local p={frames=1600,capture_every=100,moves={{500,1500,'a',100,4}}}
p.setup=function()
 local sr=emu.memType.wsCartRam
 emu.write(0x649b,0xe0,sr);emu.write16(0x64a1,0x2d7e,sr);emu.write(0x649c,0,sr);emu.write(0x64a0,0,sr)
 emu.write16(0x7303,tonumber(os.getenv('TARGET_FLOOR')) or 30,sr)
end
return p
