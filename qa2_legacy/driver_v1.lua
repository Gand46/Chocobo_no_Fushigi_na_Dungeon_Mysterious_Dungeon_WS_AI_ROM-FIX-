local out=assert(os.getenv('QA_OUT'));local plan=assert(loadfile(os.getenv('QA_PLAN')))();local f=0;local ready=false
local function save(n,b)local h=assert(io.open(out..'/'..n,'wb'));h:write(b);h:close() end
local function memory(mt)local t={};for a=0,emu.getMemorySize(mt)-1 do t[#t+1]=string.char(emu.read(a,mt,false)) end;return table.concat(t) end
local cb;cb=emu.addMemoryCallback(function()
 emu.removeMemoryCallback(cb,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws)
 local p=os.getenv('QA_STATE');if p~='' then local h=assert(io.open(p,'rb'));local b=h:read('*a');h:close();emu.loadSavestate(b) end
 if plan.setup then plan.setup() end
 ready=true
end,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws)
local log=assert(io.open(out..'/frames.csv','w'));log:write('frame,cs,ip,sp,poweroff,menu,qty,item\n')
emu.addEventCallback(function()
 local input={up=false,down=false,left=false,right=false,up2=false,down2=false,left2=false,right2=false,a=false,b=false,start=false,sound=false}
 if ready then for _,r in ipairs(plan.moves or {}) do if f>=r[1] and f<r[2] and (not r[4] or (f-r[1])%r[4]<(r[5] or 3)) then input[r[3]]=true end end end
 emu.setInput(input,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 if not ready then return end;f=f+1
 if plan.tick then plan.tick(f,save,memory) end
 if f%60==0 then local s=emu.getState();log:write(string.format('%d,%04X,%04X,%04X,%s,%04X,%d,%d\n',f,s['cpu.cs'],s['cpu.ip'],s['cpu.sp'],tostring(s['cpu.powerOff']),emu.read16(0x6032,emu.memType.wsCartRam,false),emu.read(0x6c9f,emu.memType.wsCartRam,false),emu.read(0x6ca0,emu.memType.wsCartRam,false)));log:flush() end
 if f%(plan.capture_every or 120)==0 or f==plan.frames then save(string.format('f%05d.png',f),emu.takeScreenshot()) end
 if f==plan.frames then
 save('sram.bin',memory(emu.memType.wsCartRam));save('wram.bin',memory(emu.memType.wsWorkRam));log:close()
 emu.addMemoryCallback(function()save('checkpoint.mss',emu.createSavestate());save('completed.txt','frames='..f);emu.stop(0)end,emu.callbackType.exec,0,0xfffff,emu.cpuType.ws)
 end
end,emu.eventType.endFrame)
