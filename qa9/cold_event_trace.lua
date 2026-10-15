local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/../qa6/load_data_trace.lua'))();local old=p.setup;local oldtick=p.tick;local frame=0;local rows={};local flags={}
p.setup=function()
 old()
 emu.addMemoryCallback(function()
  local sr=emu.memType.wsCartRam;local bank=emu.read(0x649b,sr,false);local ptr=emu.read16(0x64a1,sr,false)
  if bank~=0xe1 or ptr<0x5800 or ptr>0x6600 or #rows>=300 then return end
  local s=emu.getState();rows[#rows+1]=string.format('%d,%02X:%04X,op=%02X,event=%04X,floor=%d',frame,bank,ptr-1,s['cpu.ax']&255,emu.read16(0x7335,sr,false),emu.read16(0x7303,sr,false))
 end,emu.callbackType.exec,0x4d18a,0x4d18a,emu.cpuType.ws)
 emu.addMemoryCallback(function(a,v)
  if #flags>=120 then return end;local s=emu.getState();flags[#flags+1]=string.format('%d,%04X:%04X,%05X,%04X',frame,s['cpu.cs'],s['cpu.ip'],a,v)
 end,emu.callbackType.write,0x17335,0x17336,emu.cpuType.ws)
end
p.tick=function(f,save,memory)frame=f;oldtick(f,save,memory);if f==p.frames then save('script_ops.txt',table.concat(rows,'\n'));save('event_writes.txt',table.concat(flags,'\n'))end end
return p
