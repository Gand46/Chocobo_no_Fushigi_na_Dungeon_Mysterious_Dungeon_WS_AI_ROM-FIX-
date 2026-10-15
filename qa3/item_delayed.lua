local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/item_slow.lua'))()
p.frames=4800;p.moves={{800,804,'right2'},{1200,1204,'a'},{1800,1804,'a'},{2200,2204,'a'},{3500,3504,'b'},{3800,3804,'b'},{4200,4220,'up'}}
return p
