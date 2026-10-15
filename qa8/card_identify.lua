local p={frames=1100,capture_every=220,moves={{60,64,'right2'},{300,304,'a'},{500,700,'down',20,4}}}
p.setup=function()
 local sr=emu.memType.wsCartRam;local start=tonumber(os.getenv('ITEM_START')) or 0x2d
 for k=0,17 do for i,v in ipairs({1,start+k,0,0,0})do emu.write(0x6c9f+k*5+i-1,v,sr)end end
end
return p
