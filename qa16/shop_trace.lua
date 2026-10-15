local p={frames=1100,capture_every=60,moves={{20,28,'up'},{160,164,'a'},{450,454,'a'},{800,804,'a'},{1100,1104,'b'},{1300,1304,'down'},{1500,1504,'a'}}}
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))();p.tick=function(f,save,memory)o.tick(f,save,memory);if f==p.frames then o.finish(save)end end;return p
