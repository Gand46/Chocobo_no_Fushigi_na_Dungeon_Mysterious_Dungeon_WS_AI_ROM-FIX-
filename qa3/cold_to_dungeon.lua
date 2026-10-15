local plans={'cold_verified.lua','home_exit_valid.lua','home_exit_align.lua','enter_dungeon.lua'}
local moves={};local offset=0
for _,n in ipairs(plans) do
 local p=assert(loadfile(os.getenv('QA_PLAN'):match('(.*)/')..'/'..n))()
 for _,m in ipairs(p.moves) do if not (n=='cold_verified.lua' and m[1]==3800) then moves[#moves+1]={m[1]+offset,m[2]+offset,m[3],m[4],m[5]} end end
 offset=offset+p.frames
end
return {frames=offset,capture_every=200,moves=moves}
