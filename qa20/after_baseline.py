from pathlib import Path
import time,subprocess
while not Path('qa20/runs/baseline_G05_M003/completed.txt').exists():time.sleep(1)
subprocess.run(['python3','qa20/run_batch.py','--rom','qa20/private/candidate.ws','--prefix','candidate_','--ids','qa20/changed_ids.json'],check=True)
