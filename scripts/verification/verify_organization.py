"""Verify organization-only changes against the research PR commit (requires Git history)."""
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote
import nbformat

ROOT=Path(__file__).resolve().parents[2]
import csv
REFERENCE = '3558e76'
with (ROOT/'docs/file-map.csv').open() as handle:
    mapping = {r['previous_path']:r['current_path'] for r in csv.DictReader(handle)}
original_paths = subprocess.check_output(['git','ls-tree','-r','--name-only',REFERENCE],cwd=ROOT,text=True).splitlines()
before = {}
for old in original_paths:
    payload = subprocess.check_output(['git','show',REFERENCE+':'+old],cwd=ROOT)
    before[old] = dict(new=mapping.get(old,old),sha256=hashlib.sha256(payload).hexdigest())
class NormalizePaths(ast.NodeTransformer):
    def visit_Constant(self,node):
        if isinstance(node.value,str):return ast.copy_location(ast.Constant(value='<string>'),node)
        return node
    def visit_Assign(self,node):
        names=[n.id for n in node.targets if isinstance(n,ast.Name)]
        if set(names)&{'ROOT','RAW','OUT','DATA_DIR','assets_dir','cohort_plot_root'}:
            node.value=ast.Constant(value='<path>')
            return node
        return self.generic_visit(node)
def normalized(source):
    return ast.dump(NormalizePaths().visit(ast.parse(source)),include_attributes=False)

preserved=[];notebooks=[];functions=0
for old,record in before.items():
    new=ROOT/record['new']
    assert new.is_file(),record['new']
    scientific=old.startswith(('code/assets/','data/raw/','literature_review/papers/')) or Path(old).suffix.lower() in {'.docx','.pptx','.pdf','.dotx','.xlsx'}
    if scientific:
        assert hashlib.sha256(new.read_bytes()).hexdigest()==record['sha256'],old
        preserved.append(record['new'])
    if old.endswith('.ipynb'):
        prior=json.loads(subprocess.check_output(['git','show',REFERENCE+':'+old],cwd=ROOT,text=True))
        current=json.loads(new.read_text());nbformat.validate(nbformat.from_dict(current))
        assert len(prior['cells'])==len(current['cells'])
        changed=[]
        for i,(a,b) in enumerate(zip(prior['cells'],current['cells'])):
            assert a['cell_type']==b['cell_type']
            assert a.get('outputs')==b.get('outputs'),(old,i,'outputs')
            assert a.get('execution_count')==b.get('execution_count')
            if a['cell_type']=='code':assert normalized(''.join(a['source']))==normalized(''.join(b['source'])),(old,i,'non-path code change')
            if a['source']!=b['source']:changed.append(i)
        notebooks.append(dict(path=record['new'],cells=len(current['cells']),path_or_navigation_cells_changed=changed,outputs_preserved=True))
    if old.endswith('.py'):
        prior=ast.parse(subprocess.check_output(['git','show',REFERENCE+':'+old],cwd=ROOT,text=True))
        current=ast.parse(new.read_text())
        a={n.name:ast.dump(NormalizePaths().visit(n),include_attributes=False) for n in prior.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
        b={n.name:ast.dump(NormalizePaths().visit(n),include_attributes=False) for n in current.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
        assert a==b,(old,'algorithm function changed')
        functions+=len(a)
assert hashlib.sha256((ROOT/'docs/methods/extension_analysis_protocol.md').read_bytes()).hexdigest()==before['reports/extension_analysis_protocol.md']['sha256']

checked_links=0
for p in list(ROOT.rglob('*.md'))+list((ROOT/'notebooks').glob('*.ipynb')):
    if '.git' in p.parts:continue
    if p.suffix=='.ipynb':
        text='\n'.join(''.join(c['source']) for c in json.loads(p.read_text())['cells'] if c['cell_type']=='markdown')
    else:text=p.read_text()
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if '://' in target or target.startswith('#'):continue
        target=unquote(target.strip('<>').split('#')[0])
        assert (p.parent/target).exists(),(str(p.relative_to(ROOT)),target)
        checked_links+=1
result=dict(status='passed',reference_commit='3558e76',moved_files=sum(a!=r['new'] for a,r in before.items()),
            scientific_files_byte_identical=len(preserved),scientific_file_paths=preserved,
            notebook_audit=notebooks,algorithm_functions_preserved=functions,
            local_markdown_links_checked=checked_links,dated_protocol_byte_identical=True)
(ROOT/'docs/verification/organization_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['scientific_file_paths','notebook_audit']},indent=2))
