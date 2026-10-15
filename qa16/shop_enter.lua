local p={frames=1600,capture_every=60,moves={{20,50,'up'},{150,1500,'a',150,4}}}
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))();p.tick=function(f,save,memory)o.tick(f,save,memory);if f==p.frames then o.finish(save)end end;return p
