local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/stair_save.lua'))()
local sr=emu.memType.wsCartRam;local frame=0;local events={};local payload=0
local function bytes(a,n)local t={};for i=a,a+n-1 do t[#t+1]=string.char(emu.read(i,sr,false))end;return table.concat(t)end
local function save(name,b)local f=assert(io.open(os.getenv('QA_OUT')..'/'..name,'wb'));f:write(b);f:close()end
p.setup=function()
 save('before_save.sav',bytes(0,32768))
 emu.addMemoryCallback(function(a,v)
  local z=emu.getState();events[#events+1]=string.format('%d,%05X,%02X,%04X:%04X',frame,a,v,z['cpu.cs'],z['cpu.ip'])
  if a>=0x175b6 and a<=0x17f89 then payload=payload+1 end
 end,emu.callbackType.write,0x175ac,0x17f8f,emu.cpuType.ws)
 emu.addMemoryCallback(function()save('commit_live.sav',bytes(0,32768))end,emu.callbackType.exec,0x9fa9a,0x9fa9a,emu.cpuType.ws)
 emu.addMemoryCallback(function()save('commit_live.sav',bytes(0,32768))end,emu.callbackType.exec,0x9fab3,0x9fab3,emu.cpuType.ws)
end
p.tick=function(f,write,memory)
 frame=f
 if f==p.frames then write('writes.csv','frame,address,value,pc\n'..table.concat(events,'\n'));write('payload_write_count.txt',tostring(payload))end
end
return p
