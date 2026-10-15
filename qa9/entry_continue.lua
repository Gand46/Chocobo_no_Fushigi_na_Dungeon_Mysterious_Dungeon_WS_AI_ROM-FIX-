local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/ending_flag_trace.lua'))();p.frames=2500;p.capture_every=250;p.moves={{60,2400,'a',100,4}};return p
