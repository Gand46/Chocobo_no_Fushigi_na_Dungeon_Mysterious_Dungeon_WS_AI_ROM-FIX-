-- Explicit synthetic, one-time bag fixture. Inventory record: qty,id,level,aux,flags.
local out=assert(os.getenv('AUDIT_OUT'))
local ids={0x65,0x9d,0xff,0xde,0x59}
local frame=0
local f=assert(io.open(out..'/inventory_fixture.csv','w'));f:write('address,before,after\n')
emu.addEventCallback(function()
 frame=frame+1
 if frame==10 then
  for i,id in ipairs(ids) do
   local base=0x6c9f+(i-1)*5
   for j,v in ipairs({1,id,0,0,0}) do
    local addr=base+j-1;local prev=emu.read(addr,emu.memType.wsCartRam,false)
    emu.write(addr,v,emu.memType.wsCartRam);f:write(string.format('%04X,%02X,%02X\n',addr,prev,v))
   end
  end
  f:close()
 end
end,emu.eventType.endFrame)
