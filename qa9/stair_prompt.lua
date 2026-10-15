local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/stair_access.lua'))();p.frames=180;p.capture_every=60;p.moves={{60,78,'up'}};return p
