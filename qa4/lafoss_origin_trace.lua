local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/../qa3/lafoss_use.lua'))();local old=p.setup
p.setup=function()
 old();local n=0
 emu.addMemoryCallback(function()
  local s=emu.getState();if s['cpu.cx']~=0xffff or n>=3 then return end;n=n+1
  local h=assert(io.open(os.getenv('QA_OUT')..'/origin.txt','a'))
  for _,r in ipairs({'cs','ip','ax','bx','cx','dx','si','di','bp','ds','es','ss','sp'}) do h:write(string.format('%s=%04X ',r,s['cpu.'..r])) end
  h:write(' stack=');for i=0,60,2 do h:write(string.format('%04X,',emu.read16((s['cpu.ss']*16+s['cpu.sp']+i)%0x100000,emu.memType.wsMemory,false))) end
  h:write('\n');h:close()
 end,emu.callbackType.exec,0x54392,0x54392,emu.cpuType.ws)
end
return p
