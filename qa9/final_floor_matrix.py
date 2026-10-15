from pathlib import Path
import subprocess,json,struct
for n in [11,22,33,44,55,66,77,88,100,30]:
 out=f'runs/q9_final{n}'
 subprocess.run(['python3','qa9/run.py','private_roms/qa9_floor_scoped.ws','-','qa9/cold_event_trace.lua',out,'--mesen','profiles/q9_trace/Mesen','--input-save',f'qa9/event_fixtures/D3_to_{n}.sav','--timeout','25'],stdout=subprocess.DEVNULL,check=True)
 b=Path(out,'sram.bin').read_bytes();print(n,struct.unpack_from('<H',b,0x7303)[0],hex(struct.unpack_from('<H',b,0x7335)[0]),flush=True)
