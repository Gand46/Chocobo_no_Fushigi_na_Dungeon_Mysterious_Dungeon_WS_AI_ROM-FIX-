return {frames=1500,capture_every=60,setup=function()
 for i,v in ipairs({1,157,0,0,1,0,0,0,0,0}) do emu.write(0x6c9f+i-1,v,emu.memType.wsCartRam) end
end,moves={{60,64,'right2'},{300,304,'a'},{800,804,'a'},{1000,1004,'a'}}}
