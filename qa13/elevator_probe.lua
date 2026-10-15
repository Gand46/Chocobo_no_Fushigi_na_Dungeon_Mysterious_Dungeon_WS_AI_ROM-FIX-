local p={frames=2000,capture_every=100,moves={{500,1100,'a',100,4}}}
local frame=0;local rows={}
p.setup=function()
 emu.addMemoryCallback(function()
 local sr=emu.memType.wsCartRam;local z=emu.getState();if #rows<2000 then rows[#rows+1]=string.format("%d,%02X:%04X,%02X",frame,emu.read(0x649b,sr,false),emu.read16(0x64a1,sr,false)-1,z["cpu.ax"]%256)end
 end,emu.callbackType.exec,0x4d18a,0x4d18a,emu.cpuType.ws)
 local sr=emu.memType.wsCartRam
 emu.write(0x7301,3,sr);emu.write(0x1fae,5,sr);emu.write(0x649b,0xe0,sr);emu.write16(0x64a1,0x2873,sr);emu.write(0x649c,0,sr);emu.write(0x649f,0x80,sr);emu.write(0x64a0,0,sr)
end
p.tick=function(f,save,memory)
 frame=f
 if f==p.frames then save("ops.csv","frame,script,op\n"..table.concat(rows,"\n"))end
 if f==350 then emu.write16(0x060e,tonumber(os.getenv('TARGET_FLOOR')) or 30,emu.memType.wsCartRam)end
end
return p
