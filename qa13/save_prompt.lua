local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/../qa9/stair_prompt.lua'))()
return p
