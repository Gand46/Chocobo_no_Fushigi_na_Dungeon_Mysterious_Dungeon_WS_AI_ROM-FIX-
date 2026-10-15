-- Ordinary runs: read-only observer and controller inputs.
-- AUDIT_SYNTHETIC_TARGET: explicitly synthetic substitution of ROM read values.
-- No permanent ROM changes and no WRAM/CPU register pokes.
local out=assert(os.getenv('AUDIT_OUT'))
local limit=tonumber(os.getenv('AUDIT_FRAMES') or '2400')
local route=assert(loadfile(assert(os.getenv('AUDIT_ROUTE'))))()
local frames=0
local probe=os.getenv('AUDIT_PROBE')
if probe then assert(loadfile(probe))() end
local resume=os.getenv('AUDIT_RESUME')
if resume and resume~='' then
 local loaded=false
 local reference
 reference=emu.addMemoryCallback(function()
  if not loaded then
   loaded=true
   local f=assert(io.open(resume,'rb'));local data=f:read('*a');f:close()
   emu.loadSavestate(data)
   emu.removeMemoryCallback(reference,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws)
  end
 end,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws)
end
local log=assert(io.open(out..'/frames.csv','w')); log:write('frame,cs,ip,sp,poweroff,lcd,bank0,bank1,bank2,bank3,sramwrites\n')
local swrites=0
local syntheticTarget=tonumber(os.getenv('AUDIT_SYNTHETIC_TARGET') or '')
if syntheticTarget then
 local f=assert(io.open(out..'/synthetic_reads.csv','w'));f:write('frame,requested_word,source_rom_offset,returned_value\n')
 local seen={}
 emu.addMemoryCallback(function(addr,value)
  local s=emu.getState()
  if s['cpu.cs']==0x3000 and s['cpu.ip']==0x7E1D and s['cpu.dx']==2 then
   local delta=(addr & 0xFFFF)-0xE2E2
   local v=emu.read16(syntheticTarget+delta,emu.memType.wsPrgRom,false)
   if not seen[delta] then
    seen[delta]=true;f:write(string.format('%d,%d,%06X,%04X\n',frames,delta//2,syntheticTarget+delta,v));f:flush()
   end
   return v
  end
 end,emu.callbackType.read,0x16E2E2,0x16E522,emu.cpuType.ws,emu.memType.wsPrgRom)
end
if os.getenv('AUDIT_TRACE_TEXT')=='1' then
 local seen={};local count=0
 local f=assert(io.open(out..'/text_consumers.csv','w'))
 f:write('frame,cpu_address,value_hex,cs,ip,ds,es,si,di,ax,cx\n')
 local function observe(addr,value)
  if not seen[addr] and count<400 then
   seen[addr]=true;count=count+1
   local s=emu.getState()
   f:write(string.format('%d,%06X,%02X,%04X,%04X,%04X,%04X,%04X,%04X,%04X,%04X\n',frames,addr,value,s['cpu.cs'],s['cpu.ip'],s['cpu.ds'],s['cpu.es'],s['cpu.si'],s['cpu.di'],s['cpu.ax'],s['cpu.cx']));f:flush()
  end
 end
 for _,r in ipairs({{0x15AD00,0x15DADF},{0x16E1E0,0x16FC07},{0x19BFC4,0x19C7E7},{0x06C364,0x06CB85}}) do
  emu.addMemoryCallback(observe,emu.callbackType.read,r[1],r[2],emu.cpuType.ws,emu.memType.wsPrgRom)
 end
end
local function write(path,bytes)
 local f=assert(io.open(out..'/'..path,'wb'));f:write(bytes);f:close()
end
local function bytes(t)
 local a={}
 for i=1,#t,4096 do a[#a+1]=string.char(table.unpack(t,i,math.min(i+4095,#t))) end
 return table.concat(a)
end
local function mem(mt)
 local t={};local n=emu.getMemorySize(mt)
 for a=0,n-1 do t[#t+1]=emu.read(a,mt,false) end
 return bytes(t)
end
local ports={}
for _,port in ipairs({0x60,0xA0,0xC0,0xC1,0xC2,0xC3}) do
 emu.addMemoryCallback(function(addr,value)
  local k=string.format('%02X=%02X',addr,value); ports[k]=(ports[k] or 0)+1
 end,emu.callbackType.write,port,port,emu.cpuType.ws,emu.memType.wsPort)
end
emu.addMemoryCallback(function(a,v) swrites=swrites+1 end,emu.callbackType.write,0,0x7fff,emu.cpuType.ws,emu.memType.wsCartRam)
emu.addEventCallback(function()
 local input={up=false,down=false,left=false,right=false,up2=false,down2=false,left2=false,right2=false,a=false,b=false,start=false,sound=false}
 for _,r in ipairs(route) do
  if frames>=r[1] and frames<r[2] then
   if not r[4] or (frames-r[1])%r[4]<(r[5] or 3) then input[r[3]]=true end
  end
 end
 emu.setInput(input,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 frames=frames+1
 if frames%60==0 then
  local s=emu.getState()
  log:write(string.format('%d,%04X,%04X,%04X,%s,%s,%d,%d,%d,%d,%d\n',frames,s['cpu.cs'],s['cpu.ip'],s['cpu.sp'],tostring(s['cpu.powerOff']),tostring(s['ppu.lcdEnabled']),s['cart.selectedBanks0'],s['cart.selectedBanks1'],s['cart.selectedBanks2'],s['cart.selectedBanks3'],swrites))
  log:flush()
 end
 if frames==180 or frames%240==0 or frames==limit then
  write(string.format('frame_%05d.png',frames),emu.takeScreenshot())
 end
 if frames==limit then
  local c=emu.getCdlData(emu.memType.wsPrgRom);local ct={}
  for i=0,emu.getMemorySize(emu.memType.wsPrgRom)-1 do ct[#ct+1]=c[i] end
  write('cdl.bin',bytes(ct))
  write('sram.bin',mem(emu.memType.wsCartRam))
  write('wram.bin',mem(emu.memType.wsWorkRam))
  local a={};for k,v in pairs(ports) do a[#a+1]=k..','..v end;table.sort(a);write('ports.csv',table.concat(a,'\n')..'\n')
  write('completed.txt','frames='..frames..'\nsramwrites='..swrites..'\nmethod='..(syntheticTarget and 'SYNTHETIC_RESOURCE_SUBSTITUTION' or (resume and 'SAVESTATE_CONTINUATION' or 'SCRIPTED_NATURAL'))..'\n')
  log:close()
  emu.addMemoryCallback(function()
   write('checkpoint.mss',emu.createSavestate());emu.stop(0)
  end,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws)
 end
end,emu.eventType.endFrame)
