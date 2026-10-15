local p={frames=400,capture_every=400,moves={}}
p.tick=function(f,save,memory) if f==400 then local a={};for k,v in pairs(emu.getState())do a[#a+1]=tostring(k)..'='..tostring(v) end;table.sort(a);save('state.txt',table.concat(a,'\n')) end end
return p
