"""Download public CDC BMI/independent-cycle inputs; record exact file hashes."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
jobs = [(2021, 'L', 'BMX', ROOT/'data/raw')]
jobs += [(2017, 'J', name, ROOT/'data/raw/2017_2018') for name in ['DEMO','CBC','GHB','DIQ','BMX','GLU']]
manifest_path = ROOT/'data/extension_download_manifest.json'
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
known = {x['path']:x for x in manifest}
for year, suffix, component, directory in jobs:
    directory.mkdir(parents=True, exist_ok=True)
    for extension in ['htm','xpt']:
        filename=f'{component}_{suffix}.{extension}'
        path=directory/filename
        url=f'https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{year}/DataFiles/{filename}'
        key=str(path.relative_to(ROOT))
        if not path.exists():
            with urlopen(Request(url, headers={'User-Agent':'BMEN600 research data acquisition'}),timeout=90) as response:
                payload=response.read()
            if extension=='xpt' and not payload.startswith(b'HEADER RECORD'):
                raise ValueError(f'Not an XPORT file: {url}')
            path.write_bytes(payload)
            stamp=datetime.now(timezone.utc).isoformat()
        else:
            stamp=known.get(key,{}).get('downloaded_at_utc','unknown; existing local file')
        known[key]=dict(path=key,url=url,downloaded_at_utc=stamp,
                        bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        manifest_path.write_text(json.dumps(list(known.values()),indent=2)+'\n')
        print(key,flush=True)
