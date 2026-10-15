-- Synthetic selection into the original text engine; real glyphs and controls.
local p={frames=2400,capture_every=100000,moves={{50,54,'a'}}}
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))()
local f=0;local active=false;local finished=false;local seenpause=false;local wait=0;local pages=0
local out=assert(os.getenv('QA_OUT'))
local function save(n,b)local h=assert(io.open(out..'/'..n,'wb'));h:write(b);h:close()end
p.setup=function()
 local cb;cb=emu.addMemoryCallback(function()
  if emu.getState()['cpu.cs']~=0x5000 then return end
  emu.removeMemoryCallback(cb,emu.callbackType.exec,0x50e77,0x50e77,emu.cpuType.ws)
  emu.write(0x648f,10,emu.memType.wsCartRam);emu.write(0x648e,31,emu.memType.wsCartRam)
  
  active=true
 end,emu.callbackType.exec,0x50e77,0x50e77,emu.cpuType.ws)
 emu.addMemoryCallback(function()
  if active and not finished and emu.getState()['cpu.cs']==0x5000 and emu.getState()['cpu.ax']==0xffff and (emu.read(0x6480,emu.memType.wsCartRam) & 0x40)==0 and emu.read(0x648f,emu.memType.wsCartRam)==10 and emu.read(0x648e,emu.memType.wsCartRam)==31 then
   save('end_text.png',emu.takeScreenshot());finished=true;p.frames=f+30
  end
 end,emu.callbackType.exec,0x51158,0x51158,emu.cpuType.ws)
end
p.tick=function(frame,writer,memory)
 f=frame;o.tick(f,writer,memory)
 if active and not finished then
  local state=emu.read(0x6480,emu.memType.wsCartRam) & 0x7f
  if state==4 or state==1 then
   wait=wait+1
   if wait==24 and not seenpause then pages=pages+1;save(string.format('page_%02d.png',pages),emu.takeScreenshot());p.moves[#p.moves+1]={f+1,f+5,'a'};seenpause=true end
  else wait=0;seenpause=false end
 end
 if f==p.frames then writer('target_completed.txt',tostring(finished));o.finish(writer)end
end
return p
