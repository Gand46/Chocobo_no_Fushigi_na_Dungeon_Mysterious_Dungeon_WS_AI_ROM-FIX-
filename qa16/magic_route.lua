local p={frames=850,capture_every=60,moves={{60,64,'right2'},{130,134,'down'},{200,204,'down'},{270,274,'down'},{340,344,'down'},{410,414,'a'},{700,704,'b'}}}
local o=assert(loadfile(os.getenv('LAYOUT_OBSERVER')))();p.tick=function(f,save,memory)o.tick(f,save,memory);if f==p.frames then o.finish(save)end end;return p
