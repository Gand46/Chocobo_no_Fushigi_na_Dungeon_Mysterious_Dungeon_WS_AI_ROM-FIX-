local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/cold_event_trace.lua'))();local old=p.setup
p.setup=function()
 old();local sr=emu.memType.wsCartRam
 emu.addMemoryCallback(function()
  local ptr=emu.read16(0x64a1,sr,false);local bank=emu.read(0x649b,sr,false)
  if bank==0xe1 and ptr==0x5971 then
   local n=emu.read16(0x7303,sr,false)
   for i=0,4 do emu.write(0x753a+i,n%10,sr);n=math.floor(n/10)end
  end
 end,emu.callbackType.exec,0x4d18a,0x4d18a,emu.cpuType.ws)
end
return p
