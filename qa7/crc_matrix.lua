local p={frames=3000,no_dump=true,capture_every=3000,moves={}}
local out=assert(os.getenv('QA_OUT'));local source=assert(os.getenv('MATRIX_SOURCE'));local sr=emu.memType.wsCartRam
local h=assert(io.open(source..'/generation_B.sav','rb'));local base=h:read('*a');h:close()
local cases={{name='valid',address=0,xor=0}}
for _,a in ipairs({0x75b6,0x75b7,0x75d5,0x765b,0x767e,0x79b6,0x7db5,0x7f89})do
 for bit=0,7 do cases[#cases+1]={name='payload',address=a,xor=2^bit}end
end
for a=0x75b0,0x75b3 do for bit=0,7 do cases[#cases+1]={name='active_marker',address=a,xor=2^bit}end end
for a=0x7f8a,0x7f8f do for bit=0,7 do cases[#cases+1]={name='metadata',address=a,xor=2^bit}end end
local index=1;local rows={};local done=false
local function save(name,b)local f=assert(io.open(out..'/'..name,'w'));f:write(b);f:close()end
p.setup=function()
 emu.addMemoryCallback(function()
  for a=0x75ac,0x7f8f do emu.write(a,base:byte(a+1),sr)end
  local c=assert(cases[index]);if c.address~=0 then emu.write(c.address,base:byte(c.address+1)~c.xor,sr)end
 end,emu.callbackType.exec,0x9fc0b,0x9fc0b,emu.cpuType.ws)
 emu.addMemoryCallback(function()
  local c=cases[index];rows[#rows+1]=string.format('%s,%04X,%02X,%d',c.name,c.address,c.xor,emu.read(0x75b4,sr,false));index=index+1
 end,emu.callbackType.exec,0x9fc10,0x9fc10,emu.cpuType.ws)
 emu.addMemoryCallback(function()
  if done then return end;done=true
  save('native_results.csv','kind,address,xor,valid_mask\n'..table.concat(rows,'\n'));save('completed.txt','native CRC cases='..#rows);emu.stop(0)
 end,emu.callbackType.exec,0x9fc12,0x9fc12,emu.cpuType.ws)
end
return p
