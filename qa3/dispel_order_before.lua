local function put(a,t) for i,v in ipairs(t) do emu.write(a+i-1,v,emu.memType.wsCartRam) end end
return {frames=3800,capture_every=60,setup=function()
 put(0x6c9f,{1,157,0,0,1});put(0x6ca4,{1,89,0,0,0})
end,tick=function(f,save,memory)
 if f==1000 or f==2300 or f==3400 then save('sram_f'..f..'.bin',memory(emu.memType.wsCartRam)) end
end,moves={{60,64,'right2'},{300,304,'a'},{380,384,'down'},{430,434,'a'},{490,494,'a'},{680,684,'a'},{900,904,'b'},{980,984,'b'},{1060,1064,'b'},
{2400,2404,'right2'},{2520,2524,'a'},{2760,2764,'a'},{2850,2854,'a'},{3200,3204,'a'},{3440,3444,'b'},{3540,3544,'b'},{3640,3644,'b'}}}
