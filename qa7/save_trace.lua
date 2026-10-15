local p={frames=250,capture_every=250,moves={{30,34,'a'}}}
local sr=emu.memType.wsCartRam;local n=0;local events={}
local function bytes(a,n)local t={};for i=a,a+n-1 do t[#t+1]=string.char(emu.read(i,sr,false))end;return table.concat(t)end
local function save(n,b)local h=assert(io.open(os.getenv('QA_OUT')..'/'..n,'wb'));h:write(b);h:close()end
p.setup=function()
 local h=assert(io.open(assert(os.getenv('SAVE_FIXTURE')),'rb'));local b=h:read('*a');h:close();assert(#b==32768)
 for a=0x75ac,0x7fff do emu.write(a,b:byte(a+1),sr)end
 emu.write(0x6c7d,tonumber(os.getenv('SAVE_LEVEL')) or 2,sr);emu.write16(0x6c7e,tonumber(os.getenv('SAVE_HP')) or 29,sr);emu.write16(0x050e,tonumber(os.getenv('SAVE_COUNTER')) or 0x1234,emu.memType.wsWorkRam)
 save('generation_A.sav',bytes(0,32768))
 emu.addMemoryCallback(function(a,v)
  events[#events+1]=string.format('%05X,%02X',a,v)
  if a>=0x175b6 and a<=0x17f89 then
   n=n+1
   if n==1 or n==200 or n==2516 then save(string.format('cut_%04d.sav',n),bytes(0,32768))end
  end
 end,emu.callbackType.write,0x175ac,0x17f8f,emu.cpuType.ws)
 emu.addMemoryCallback(function()save('native_marker_only.sav',bytes(0,32768))end,emu.callbackType.exec,0x9038b,0x9038b,emu.cpuType.ws)
 emu.addMemoryCallback(function()save('generation_B.sav',bytes(0,32768))end,emu.callbackType.exec,0x9fa9a,0x9fa9a,emu.cpuType.ws)
 emu.addMemoryCallback(function()save('generation_B.sav',bytes(0,32768))end,emu.callbackType.exec,0x9fab3,0x9fab3,emu.cpuType.ws)
end
p.tick=function(f)
 if f==p.frames then save('writes.csv','address,value\n'..table.concat(events,'\n'));save('payload_write_count.txt',tostring(n))end
end
return p
