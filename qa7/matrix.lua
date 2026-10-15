local p={frames=300,no_dump=true,capture_every=300,moves={}}
local out=assert(os.getenv('QA_OUT'));local source=assert(os.getenv('MATRIX_SOURCE'));local sr=emu.memType.wsCartRam
local h=assert(io.open(source..'/generation_A.sav','rb'));local base=h:read('*a');h:close()
local events={};h=assert(io.open(source..'/writes.csv','r'))
for line in h:lines()do local a,v=line:match('^(%x+),(%x+)$');if a then events[#events+1]={tonumber(a,16)-0x10000,tonumber(v,16)}end end;h:close()
local n=0;local result={};local done=false
local function save(name,b)local f=assert(io.open(out..'/'..name,'w'));f:write(b);f:close()end
p.setup=function()
 emu.addMemoryCallback(function()
  if n==0 then for a=0x75ac,0x7f8f do emu.write(a,base:byte(a+1),sr)end
  else local e=assert(events[n]);assert(e[2]<256);emu.write(e[1],e[2],sr)end
 end,emu.callbackType.exec,0x9fc0b,0x9fc0b,emu.cpuType.ws)
 emu.addMemoryCallback(function()
  result[#result+1]=string.format('%d,%d',n,emu.read(0x75b4,sr,false));n=n+1
 end,emu.callbackType.exec,0x9fc10,0x9fc10,emu.cpuType.ws)
 emu.addMemoryCallback(function()
  if done then return end;done=true
  save('native_results.csv','write_prefix,valid_mask\n'..table.concat(result,'\n'))
  save('completed.txt','native validator cases='..n);emu.stop(0)
 end,emu.callbackType.exec,0x9fc12,0x9fc12,emu.cpuType.ws)
end
return p
