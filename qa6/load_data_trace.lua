local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/../qa3/cold_verified.lua'))()
p.moves={{180,184,'start'},{900,904,'down'},{1100,1104,'a'},{2980,2984,'a'}}
p.capture_every=1000
local sr=emu.memType.wsCartRam;local frame=0;local copies=0;local rows={};local history={}
local function save(n,b)local h=assert(io.open(os.getenv('QA_OUT')..'/'..n,'wb'));h:write(b);h:close()end
local function bytes(a,n)local t={};for i=a,a+n-1 do t[#t+1]=string.char(emu.read(i,sr,false)) end;return table.concat(t)end
p.setup=function()
 emu.addMemoryCallback(function()
  copies=copies+1
  save('load_'..copies..'_before.sav',bytes(0,32768))
 end,emu.callbackType.exec,0x90333,0x90333,emu.cpuType.ws)
 emu.addMemoryCallback(function()
  save('load_'..copies..'_copied.sav',bytes(0,32768))
 end,emu.callbackType.exec,0x9033f,0x9033f,emu.cpuType.ws)
 emu.addMemoryCallback(function()
  save('load_'..copies..'_returned.sav',bytes(0,32768))
 end,emu.callbackType.exec,0x90359,0x90359,emu.cpuType.ws)
 emu.addMemoryCallback(function(a,v)
  if #history>=30 then return end
  local s=emu.getState();history[#history+1]=string.format('%d,%04X:%04X,%05X,%04X,%02X,%04X',frame,s['cpu.cs'],s['cpu.ip'],a,v,emu.read(0x649b,sr,false),emu.read16(0x64a1,sr,false))
 end,emu.callbackType.write,0x17301,0x17306,emu.cpuType.ws)
end
p.tick=function(f)
 frame=f
 if f==p.frames then save('transition_writes.csv','frame,pc,address,value,script_bank,script_pointer\n'..table.concat(history,'\n'));save('load_count.txt',tostring(copies)) end
end
return p
