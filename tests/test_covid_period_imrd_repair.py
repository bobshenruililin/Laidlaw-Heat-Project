"""Current COVID paper: source-value checks and interpretable scientific structure.

The September exact-prose fixtures are superseded; they required unsupported
ruling-out language. No governed panels are opened by these checks.
"""
from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
COVID=ROOT/'manuscript/covid_period/Manuscript_covid_period_draft.md'
def test_source_bound_tables_and_claims():
    proc=subprocess.run([sys.executable,str(ROOT/'scripts/81_covid_research_manuscript.py'),'--audit'],cwd=ROOT,capture_output=True,text=True)
    assert proc.returncode==0,proc.stdout+proc.stderr
    report=json.loads((ROOT/'manuscript/covid_period/claim_ledger.yml').read_text().split('\n',1)[1])
    assert report['status']=='PASS'
    assert all(x['passed']for x in report['checks'])
def test_scientific_structure_and_identification_boundaries():
    text=COVID.read_text()
    headings=['## Abstract','## Introduction','## Methods','## Results','## Discussion','## Conclusion','## Data and code availability','## References']
    positions=[text.index(h)for h in headings]
    assert positions==sorted(positions)
    assert 'No 2020–2023-only model or exposure-by-period interaction was available.'in text
    assert 'Their difference is not an estimated pre/post effect.'in text
    assert 'It does not supply the eligible person-time denominator needed for incidence rates.'in text
    assert 'The thermal panel also cannot exclude weather as an explanation'in text
    assert 'UW XX-XXX'not in text
    assert 'Author 2'not in text
