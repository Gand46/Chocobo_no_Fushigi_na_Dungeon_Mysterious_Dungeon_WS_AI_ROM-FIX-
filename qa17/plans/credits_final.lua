-- SAVESTATE from QA8 assisted boss. Native credits progression; no selectors changed.
local p={frames=7200,capture_every=120,moves={{50,7100,'a',60,4}}}
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))();local f=0;local page={};local pending={};local calls={};local sr=emu.memType.wsCartRam
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.cs']~=0x5000 then return end
 local id=s['cpu.ax'];if id<0xc5 or id>0xd2 then return end
 calls[#calls+1]=string.format('%d,%02X,%04X',f,id,emu.read16(s['cpu.ss']*16+s['cpu.sp'],emu.memType.wsMemory,false))
 if not page[id]then page[id]=f;pending[id]=f+120 end
end,emu.callbackType.exec,0x503c2,0x503c2,emu.cpuType.ws)
p.tick=function(frame,save,memory)
 f=frame;o.tick(f,save,memory)
 for id,t in pairs(pending)do if f==t then save(string.format('credits_%02X_f%05d.png',id,f),emu.takeScreenshot())end end
 if f==p.frames then save('credits_pages.csv','frame,resource_id,return_ip\n'..table.concat(calls,'\n'));o.finish(save)end
end
return p
