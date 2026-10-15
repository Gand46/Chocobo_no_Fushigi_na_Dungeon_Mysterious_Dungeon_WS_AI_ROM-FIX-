local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/../qa3/whistle_dump.lua'))();local old=p.setup
p.setup=function()
 old();local h=assert(io.open(os.getenv('QA_OUT')..'/palettes.txt','w'));local n=0
 emu.addMemoryCallback(function()
  n=n+1;if n>20 then return end
  local s=emu.getState();h:write(string.format('ax=%04X dx=%04X bank=%02X ',s['cpu.ax'],s['cpu.dx'],s['cart.selectedBanks2']));for i=0,11 do h:write(tostring(s['ppu.bwPalettes'..i])..',') end;h:write('\n');h:flush()
 end,emu.callbackType.exec,0x54935,0x54935,emu.cpuType.ws)
end
return p
