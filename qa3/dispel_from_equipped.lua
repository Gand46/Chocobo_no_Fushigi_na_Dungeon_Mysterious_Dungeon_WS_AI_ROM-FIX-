return {frames=1600,capture_every=60,setup=function()
 if os.getenv('ADD_DRINK')=='1' then for i,v in ipairs({1,89,0,0,0}) do emu.write(0x6ca4+i-1,v,emu.memType.wsCartRam) end end
end,moves={{60,64,'b'},{400,404,'a'},{750,754,'a'}},tick=function(f,save,memory)
 if f==30 or f==650 or f==1500 then save('sram_f'..f..'.bin',memory(emu.memType.wsCartRam)) end
end}
