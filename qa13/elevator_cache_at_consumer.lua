-- Causal control: JP unchanged; refresh only cached floor digits at the native selector read.
local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/elevator_causal_trace.lua'))()
local old=p.setup;local tick=p.tick;local frame=0;local rows={}
p.setup=function()
 old();local sr=emu.memType.wsCartRam
 emu.addMemoryCallback(function()
  local s=emu.getState();local ptr=emu.read16(0x64a1,sr,false);local di=s['cpu.di']
  if emu.read(0x649b,sr,false)~=0xe1 or ptr<0x639c or ptr>=0x6a00 or di<0x753a or di>0x753e then return end
  local n=emu.read16(0x7303,sr,false);local prior={}
  for a=0x753a,0x753e do prior[#prior+1]=tostring(emu.read(a,sr,false)) end
  rows[#rows+1]=string.format('%d,%04X,%04X,%d,%s',frame,ptr,di,n,table.concat(prior,' '))
  for a=0x753a,0x753e do emu.write(a,n%10,sr);n=math.floor(n/10)end
 end,emu.callbackType.exec,0x4d39b,0x4d39b,emu.cpuType.ws)
end
p.tick=function(f,save,memory)
 frame=f;tick(f,save,memory)
 if f==p.frames then save('cache_interventions.csv','frame,script,di,floor,prior_digits\n'..table.concat(rows,'\n'))end
end
return p
