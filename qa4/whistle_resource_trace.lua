local p=assert(loadfile(''..os.getenv('QA_PLAN'):match('(.*)/')..'/../qa3/whistle_dump.lua'))();local old=p.setup
p.setup=function()
 old();local h=assert(io.open(os.getenv('QA_OUT')..'/resource_trace.txt','w'));local count=0
 local function log(label,a,v)
  count=count+1;if count>600 then return end
  local s=emu.getState();h:write(label..string.format(' a=%05X v=%04X',a or 0,v or 0))
  for _,r in ipairs({'cs','ip','ax','bx','cx','dx','si','di','bp','ds','es','ss','sp'}) do h:write(string.format(' %s=%04X',r,s['cpu.'..r])) end
  for i=0,3 do h:write(string.format(' bank%d=%02X',i,s['cart.selectedBanks'..i] or 0)) end
  h:write(' stack=');for i=0,30,2 do h:write(string.format('%04X,',emu.read16((s['cpu.ss']*16+s['cpu.sp']+i)%0x100000,emu.memType.wsMemory,false))) end;h:write('\n');h:flush()
 end
 for _,pc in ipairs({0x5e1bb,0x5e232}) do emu.addMemoryCallback(function(a,v)log('exec',a,v)end,emu.callbackType.exec,pc,pc,emu.cpuType.ws) end
 emu.addMemoryCallback(function(a,v) if a==0x18d6 then log('map',a,v) end end,emu.callbackType.write,0x18d6,0x18d7,emu.cpuType.ws)
end
return p
