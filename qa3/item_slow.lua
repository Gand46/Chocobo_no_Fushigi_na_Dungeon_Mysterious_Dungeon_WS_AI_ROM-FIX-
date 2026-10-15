local id=tonumber(os.getenv('ITEM_ID') or '255')
return {frames=3300,capture_every=60,setup=function()
 for i,v in ipairs({1,id,0,0,0}) do emu.write(0x6c9f+i-1,v,emu.memType.wsCartRam) end
end,moves={{60,64,'right2'},{400,404,'a'},{900,904,'a'},{1300,1304,'a'},{2200,2204,'b'},{2500,2504,'b'},{2900,2920,'up'}},tick=function(f,save,memory)
 if f==1290 or f==2300 then save('sram_f'..f..'.bin',memory(emu.memType.wsCartRam)) end
end}
