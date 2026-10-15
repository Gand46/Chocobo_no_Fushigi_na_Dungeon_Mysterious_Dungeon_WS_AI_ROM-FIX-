local out=assert(os.getenv('QA_OUT'));local f=0;local seen={};local pending={};local last='';local getters={};local buffer={}
local log=assert(io.open(out..'/getters.csv','w'));log:write('frame,window,family,index,word_index,cpu_source,value,return_ip,buffer_row,column\n')
local events=assert(io.open(out..'/windows.csv','w'));events:write('frame,window,event,pointer,buffer_row,param_hex\n')
local function byte(a)return emu.read(a,emu.memType.wsCartRam,false)end
local function word(a)return emu.read16(a,emu.memType.wsCartRam,false)end
local function dump(n,s)local h=assert(io.open(out..'/'..n,'wb'));h:write(s);h:close()end
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.cs']~=0x3000 then return end
 local fam=byte(0x6427);local idx=s['cpu.dx']//2;local wi=s['cpu.cx']//2;local win=byte(0x641a);local rip=emu.read16(s['cpu.ss']*16+s['cpu.sp'],emu.memType.wsMemory,false)
 local key=string.format('%d/%d/%d/%d/%04X',win,fam,idx,wi,rip)
 if not seen[key] then seen[key]=true;log:write(string.format('%d,%d,%d,%d,%d,%05X,%04X,%04X,%d,%d\n',f,win,fam,idx,wi,s['cpu.es']*16+s['cpu.si'],s['cpu.ax'],rip,word(0x6293),word(0x642c)));log:flush()end
end,emu.callbackType.exec,0x37e1d,0x37e1d,emu.cpuType.ws)
emu.addMemoryCallback(function(a,v)
 local s=emu.getState();local k=string.format('%04X:%04X',s['cpu.cs'],s['cpu.ip']);buffer[k]=(buffer[k] or 0)+1
end,emu.callbackType.write,0x16057,0x16292,emu.cpuType.ws)
local story=assert(io.open(out..'/story.csv','w'));story:write('frame,event,group,message,bank,pointer,word_index,value,column,line,line_limit,state,return_ip\n')
local function storylog(event,value)
 local s=emu.getState();if s['cpu.cs']~=0x5000 then return end
 story:write(string.format('%d,%s,%d,%d,%02X,%04X,%d,%04X,%d,%d,%d,%02X,%04X\n',f,event,byte(0x648f),byte(0x648e),byte(0x6493),s['cpu.di'],word(0x6482),value,byte(0x6499),byte(0x6491),byte(0x6495),byte(0x6480),emu.read16(s['cpu.ss']*16+s['cpu.sp'],emu.memType.wsMemory,false)));story:flush()
end
emu.addMemoryCallback(function()storylog('start',0)end,emu.callbackType.exec,0x50eae,0x50eae,emu.cpuType.ws)
emu.addMemoryCallback(function()storylog('read',emu.getState()['cpu.ax'])end,emu.callbackType.exec,0x51158,0x51158,emu.cpuType.ws)
emu.addMemoryCallback(function()storylog('auto_line',emu.read16(0x1fed,emu.memType.wsCartRam,false))end,emu.callbackType.exec,0x51002,0x51002,emu.cpuType.ws)
local observer={}
observer.tick=function(frame,save,memory)
 f=frame;local w=byte(0x641a);local ev=word(0x6032);local key=string.format('%02X_%04X',w,ev)
 if key~=last then
  local params={};for a=0x641a,0x642d do params[#params+1]=string.format('%02X',byte(a))end
  events:write(string.format('%d,%d,%04X,%04X,%d,%s\n',f,w,ev,word(0x1fb0),word(0x6293),table.concat(params)));events:flush();last=key
  if not pending[key] then pending[key]=f+25 end
 end
 for k,t in pairs(pending) do if f==t then save(string.format('window_%s_f%05d.png',k,f),emu.takeScreenshot()) end end
end
observer.finish=function(save)
 local lines={'pc,writes'};for k,v in pairs(buffer)do lines[#lines+1]=k..','..v end;table.sort(lines);save('buffer_writers.csv',table.concat(lines,'\n'));log:close();events:close();story:close()
 local c=emu.getCdlData(emu.memType.wsPrgRom);local blocks={};for start=0,2097151,4096 do local t={};for i=start,start+4095 do t[#t+1]=string.char(c[i])end;blocks[#blocks+1]=table.concat(t)end;save('cdl.bin',table.concat(blocks))
end
return observer
