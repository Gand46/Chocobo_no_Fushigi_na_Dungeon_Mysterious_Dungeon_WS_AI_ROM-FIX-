local p={frames=1500,capture_every=100,moves={{180,184,'start'},{900,904,'down'},{1100,1104,'a'}}}
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))()
p.tick=function(f,w,m)o.tick(f,w,m);if f==p.frames then o.finish(w)end end
return p
