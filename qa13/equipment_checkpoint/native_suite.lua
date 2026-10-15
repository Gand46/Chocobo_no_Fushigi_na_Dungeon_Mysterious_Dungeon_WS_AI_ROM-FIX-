-- Native menu regression after explicit synthetic inventory construction.
local out=assert(os.getenv('SUITE_OUT')); local path=assert(os.getenv('SUITE_STATE'))
local cases=assert(loadfile(assert(os.getenv('SUITE_CASES'))))()
local sf=assert(io.open(path,'rb'));local snapshot=sf:read('*a');sf:close()
local frame=0;local caseidx=0;local localframe=0;local current=nil;local ready=false
local log=assert(io.open(out..'/events.csv','w'));log:write('case,frame,event,detail\n')
local reads=assert(io.open(out..'/text_reads.csv','w'));reads:write('case,frame,family,index,word_index,cpu_address,value,return_ip\n')
local guard=assert(io.open(out..'/buffer_guard.csv','w'));guard:write('case,frame,ip,di,value\n')
local results=assert(io.open(out..'/results.csv','w'));results:write('case,item,mode,frames,poweroff,menu_state,inventory_qty,inventory_id\n')
local seen={};local extras=assert(io.open(out..'/properties.csv','w'));extras:write('case,p1,p2,list1,list2,list3\n')
local writes=assert(io.open(out..'/persistent_writes.csv','w'));writes:write('case,frame,address,value,pc\n')
emu.addMemoryCallback(function(a,v) if ready then local z=emu.getState();writes:write(string.format('%s,%d,%05X,%02X,%04X:%04X\n',current.name,localframe,a,v,z['cpu.cs'],z['cpu.ip']));writes:flush()end end,emu.callbackType.write,0x175ac,0x17f8f,emu.cpuType.ws)
local function save(n,data)local f=assert(io.open(out..'/'..n,'wb'));f:write(data);f:close() end
local function step()
 caseidx=caseidx+1
 if caseidx>#cases then save('completed.txt','cases='..#cases..'\nframes='..frame..'\n');log:close();reads:close();guard:close();results:close();emu.stop(0);return end
 current=cases[caseidx];seen={};localframe=0;ready=false
 local cb
 cb=emu.addMemoryCallback(function()
  emu.removeMemoryCallback(cb,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws)
  emu.loadSavestate(snapshot)
  local cap=emu.read(0x6c9e,emu.memType.wsCartRam,false)
  for k=0,cap-1 do
   local id=(k==current.slot) and current.id or ((0x65+k==current.id) and (0x80+k) or (0x65+k))
   local fl=(k==current.slot) and current.flags or 16
   local level=(k==current.slot) and current.level or 0
   for j,v in ipairs({1,id,level,0,fl}) do emu.write(0x6c9f+k*5+j-1,v,emu.memType.wsCartRam) end
   local base=(id<0x9d) and (0x19b663+(id-0x65)*15+7) or (0x19b98d+(id-0x9d)*14+7)
   emu.write(0x6d3f+k*10,k,emu.memType.wsCartRam)
   for j=1,7 do emu.write(0x6d3f+k*10+j,emu.read(base+j-1,emu.memType.wsPrgRom,false),emu.memType.wsCartRam) end
   emu.write(0x6d3f+k*10+8,(k==current.slot) and current.properties[1] or 1,emu.memType.wsCartRam)
   emu.write(0x6d3f+k*10+9,(k==current.slot) and current.properties[2] or 2,emu.memType.wsCartRam)
  end
  ready=true
  log:write(string.format('%s,%d,fixture,"id=%02X level=%d aux=%d flags=%02X"\n',current.name,frame,current.id,current.level or 0,current.aux or 0,current.flags or 0));log:flush()
 end,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws)
end
emu.addMemoryCallback(function()
 if not ready then return end
 local s=emu.getState()
 if s['cpu.cs']~=0x3000 then return end
 local a=s['cpu.es']*16+s['cpu.si'];local v=s['cpu.ax']
 local family=emu.read(0x6427,emu.memType.wsCartRam,false)
 local idx=s['cpu.dx']//2;local wi=s['cpu.cx']//2
 local key=string.format('%d/%d/%d',family,idx,wi)
 if seen[key] then return end;seen[key]=true
 reads:write(string.format('%s,%d,%d,%d,%d,%05X,%04X,%04X\n',current.name,localframe,family,idx,wi,a,v,emu.read16(s['cpu.ss']*16+s['cpu.sp'],emu.memType.wsMemory,false)));reads:flush()
end,emu.callbackType.exec,0x37e1d,0x37e1d,emu.cpuType.ws)
-- Trace the actual stores in the common list/name copy consumers.
for _,ip in ipairs({0x7aff,0x7b7d,0x7bc1,0x7bfd}) do
 emu.addMemoryCallback(function()
  if not ready then return end
  local s=emu.getState();local di=s['cpu.di']
  if di>=0x23c then
   guard:write(string.format('%s,%d,%04X,%04X,%04X\n',current.name,localframe,s['cpu.ip'],di,s['cpu.ax']));guard:flush()
  end
 end,emu.callbackType.exec,0x30000+ip,0x30000+ip,emu.cpuType.ws)
end
local function pulse(t,at,button)if t>=at and t<at+4 then return button end end
emu.addEventCallback(function()
 local input={up=false,down=false,left=false,right=false,up2=false,down2=false,left2=false,right2=false,a=false,b=false,start=false,sound=false}
 if ready then
  local t=localframe
  local shift=(current.actualslot or 0)*40
  local b=pulse(t,60,'right2') or pulse(t,300,'a')
  for k=0,(current.actualslot or 0)-1 do b=b or pulse(t,400+k*40,'down') end
  b=b or pulse(t,450+shift,'a')
  local slot=0;for k=0,4 do if emu.read16(0x629a+k*2,emu.memType.wsCartRam,false)==4 then slot=k;break end end
  for k=0,slot-1 do b=b or pulse(t,490+shift+k*35,'down') end
  b=b or pulse(t,635+shift,'a')
  b=b or pulse(t,790+shift,'b') or pulse(t,850+shift,'b') or pulse(t,910+shift,'b') or pulse(t,970+shift,'b') or pulse(t,1030+shift,'b') or pulse(t,1090+shift,'b')
  if b then input[b]=true end
 end
 emu.setInput(input,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 frame=frame+1
 if not current then step();return end
 if not ready then return end
 localframe=localframe+1
 if localframe==380 then
  current.actualslot=0
  for k=0,emu.read(0x6c9e,emu.memType.wsCartRam,false)-1 do if emu.read(0x6ca0+k*5,emu.memType.wsCartRam,false)==current.id then current.actualslot=k;break end end
  log:write(string.format("%s,%d,sorted_target,%d\n",current.name,localframe,current.actualslot));log:flush()
 end
 if localframe==430+(current.actualslot or 0)*40 or localframe==750+(current.actualslot or 0)*40 or localframe==1180+(current.actualslot or 0)*40 then
  save(string.format('%s_f%03d.png',current.name,localframe),emu.takeScreenshot())
 end
 if localframe==1180+(current.actualslot or 0)*40 then
  extras:write(string.format('%s,%d,%d,%d,%d,%d\n',current.name,emu.read(0x5f6,emu.memType.wsCartRam,false),emu.read(0x5f7,emu.memType.wsCartRam,false),emu.read16(0x629a,emu.memType.wsCartRam,false),emu.read16(0x629c,emu.memType.wsCartRam,false),emu.read16(0x629e,emu.memType.wsCartRam,false)));extras:flush()
  save(current.name..'_sram.bin',(function()local z={};for a=0,32767 do z[#z+1]=string.char(emu.read(a,emu.memType.wsCartRam,false))end;return table.concat(z)end)())
  local s=emu.getState()
  results:write(string.format('%s,%d,%s,%d,%s,%04X,%d,%d\n',current.name,current.id,current.mode,localframe,tostring(s['cpu.powerOff']),emu.read16(0x6032,emu.memType.wsCartRam,false),emu.read(0x6c9f,emu.memType.wsCartRam,false),emu.read(0x6ca0,emu.memType.wsCartRam,false)));results:flush()
  ready=false;local key=current.name;local cb
  cb=emu.addMemoryCallback(function()emu.removeMemoryCallback(cb,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws);save(key..'_checkpoint.mss',emu.createSavestate());step()end,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws)
 end
end,emu.eventType.endFrame)
