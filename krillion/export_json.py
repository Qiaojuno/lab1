"""Export the SQLite archive to a JSON array of prompt objects:
{ "id", "text", "category", "difficulty", "date", "answers": [ {"answer","tier"} ] }

category   - keyword-derived (see categorize.py); the source site has no categories.
difficulty - 1 (easy) .. 5 (hard), by quintile of accepted-answer count:
             fewer accepted answers => harder.
Usage: python3 export_json.py krillion_answers.sqlite krillion_answers.json
"""
import json, re, sqlite3, sys
from categorize import categorize

STOP = {'name', 'a', 'an', 'the', 'of', 'that', 'is', 'in', 'or', 'and', 'to', 'with',
        'its', 'their', 'by', 'for', 'on', 'at', 'from', 'like', 'type', 'kind', 'one'}

def slug(text, words=5):
    toks = re.findall(r'[a-z0-9]+', text.lower().split('(')[0])
    return '-'.join([t for t in toks if t not in STOP][:words]) or 'prompt'

con = sqlite3.connect(sys.argv[1])
prompts = con.execute('''SELECT p.prompt_id, p.text, d.date, COUNT(a.answer_id)
                         FROM prompts p JOIN dives d USING (dive_number)
                         JOIN answers a USING (prompt_id)
                         GROUP BY p.prompt_id ORDER BY d.date, p.position''').fetchall()

# difficulty: rank prompts by answer count descending, split into 5 equal bands
by_count = sorted(prompts, key=lambda p: -p[3])
difficulty = {p[0]: 1 + i * 5 // len(by_count) for i, p in enumerate(by_count)}

answers = {}
for pid, ans, tier in con.execute('SELECT prompt_id, answer, tier FROM answers ORDER BY answer_id'):
    answers.setdefault(pid, []).append({'answer': ans, 'tier': tier})

used, out = set(), []
for pid, text, date, _ in prompts:
    pid_slug = base = slug(text)
    n = 2
    while pid_slug in used: pid_slug, n = f'{base}-{n}', n + 1
    used.add(pid_slug)
    out.append({'id': pid_slug, 'text': text, 'category': categorize(text),
                'difficulty': difficulty[pid], 'date': date, 'answers': answers[pid]})

# Pretty top level, one answer per line (full indent would triple the file size)
with open(sys.argv[2], 'w', encoding='utf-8') as f:
    f.write('[\n')
    for i, o in enumerate(out):
        head = {k: v for k, v in o.items() if k != 'answers'}
        f.write('  {\n')
        for k, v in head.items():
            f.write(f'    {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},\n')
        f.write('    "answers": [\n')
        f.write(',\n'.join('      ' + json.dumps(a, ensure_ascii=False) for a in o['answers']))
        f.write('\n    ]\n  }' + (',' if i < len(out) - 1 else '') + '\n')
    f.write(']\n')
