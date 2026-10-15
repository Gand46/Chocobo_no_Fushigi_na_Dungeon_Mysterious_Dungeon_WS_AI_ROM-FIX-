-- Synthetic generation B saved by the unmodified native save routine.
-- Generation A is an independently captured native HF3 save.
local p={frames=250,capture_every=250,moves={{30,34,'a'}}}
local sr=emu.memType.wsCartRam
local function bytes(a,n)
 local t={};for i=a,a+n-1 do t[#t+1]=string.char(emu.read(i,sr,false)) end
 return table.concat(t)
end
local function save(n,b)local h=assert(io.open(os.getenv('QA_OUT')..'/'..n,'wb'));h:write(b);h:close()end
local n=0;local writes={};local frame=0
p.setup=function()
 local h=assert(io.open(assert(os.getenv('SAVE_FIXTURE')),'rb'));local b=h:read('*a');h:close();assert(#b==32768)
 for a=0x75ac,0x7f89 do emu.write(a,b:byte(a+1),sr) end
 -- Controlled changes with known meaning; not natural progression.
 emu.write(0x6c7d,2,sr);emu.write16(0x6c7e,29,sr)
 emu.write16(0x050e,0x1234,emu.memType.wsWorkRam)
 save('generation_A.sav',bytes(0,32768))
 emu.addMemoryCallback(function(a,v)
  n=n+1
  if n==1 or n==200 or n==2516 then
   -- Write callbacks fire after the native store in this Mesen build.
   save(string.format('cut_%04d.sav',n),bytes(0,32768))
  end
 end,emu.callbackType.write,0x175b6,0x17f89,emu.cpuType.ws)
 emu.addMemoryCallback(function(a,v)
  writes[#writes+1]=string.format('%d,%d,%05X,%02X',frame,n,a,v)
 end,emu.callbackType.write,0x175ac,0x175b3,emu.cpuType.ws)
 emu.addMemoryCallback(function()
  save('before_copy.sav',bytes(0,32768))
 end,emu.callbackType.exec,0x90373,0x90373,emu.cpuType.ws)
 emu.addMemoryCallback(function()
  save('after_copy.sav',bytes(0,32768))
 end,emu.callbackType.exec,0x9037f,0x9037f,emu.cpuType.ws)
 emu.addMemoryCallback(function()
  save('generation_B.sav',bytes(0,32768))
 end,emu.callbackType.exec,0x9038b,0x9038b,emu.cpuType.ws)
end
p.tick=function(f)
 frame=f
 if f==p.frames then save('marker_writes.csv','frame,payload_writes,address,value\n'..table.concat(writes,'\n'));save('copy_count.txt',tostring(n)) end
end
return p
