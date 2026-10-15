local p={frames=2000,capture_every=60,moves={{60,64,'right2'},{300,304,'a'},{430,434,'a'},{600,604,'b'},{700,704,'b'},{800,804,'down'},{900,904,'a'},{1100,1104,'b'},{1200,1204,'down'},{1300,1304,'a'},{1500,1504,'b'},{1600,1604,'down'},{1700,1704,'a'}}}
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))();p.tick=function(f,save,memory)o.tick(f,save,memory);if f==p.frames then o.finish(save)end end
return p
