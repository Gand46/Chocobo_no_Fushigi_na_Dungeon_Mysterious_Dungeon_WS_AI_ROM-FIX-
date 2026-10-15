local p={frames=5000,capture_every=200,moves={{650,654,'a'},{900,904,'a'},{1100,1104,'a'},{1300,1304,'a'},{1500,1504,'a'},{1700,1704,'a'},{1900,1904,'a'},{2100,2104,'a'},{2300,2304,'a'},{2500,2504,'a'},{2700,2704,'a'},{2900,2904,'a'},{3100,3104,'a'},{3300,3304,'a'},{3500,3504,'a'},{3700,3704,'a'},{4100,4104,'right2'},{4350,4354,'down'},{4500,4504,'a'},{4700,4704,'b'}}}
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))();p.tick=function(f,save,memory)o.tick(f,save,memory);if f==p.frames then o.finish(save)end end
return p
