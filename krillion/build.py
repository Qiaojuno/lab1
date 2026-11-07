import json, glob, sqlite3, os, sys
db_path = sys.argv[2]
if os.path.exists(db_path): os.remove(db_path)
con = sqlite3.connect(db_path)
con.executescript('''
PRAGMA foreign_keys = ON;
CREATE TABLE tiers (
  code   TEXT PRIMARY KEY,
  label  TEXT NOT NULL,
  points INTEGER NOT NULL UNIQUE
);
CREATE TABLE dives (
  dive_number INTEGER PRIMARY KEY,
  date        TEXT NOT NULL UNIQUE          -- ISO yyyy-mm-dd
);
CREATE TABLE prompts (
  prompt_id   INTEGER PRIMARY KEY,
  dive_number INTEGER NOT NULL REFERENCES dives(dive_number),
  position    INTEGER NOT NULL,             -- 1..7 within the dive
  text        TEXT NOT NULL,
  UNIQUE (dive_number, position)
);
CREATE TABLE answers (
  answer_id INTEGER PRIMARY KEY,
  prompt_id INTEGER NOT NULL REFERENCES prompts(prompt_id),
  answer    TEXT NOT NULL,
  tier      TEXT NOT NULL REFERENCES tiers(code),
  UNIQUE (prompt_id, answer)
);
''')
con.executemany('INSERT INTO tiers VALUES (?,?,?)', [
  ('krillion','One in a Krillion',100), ('deepcut','Deep Cut',85), ('rare','Rare',60),
  ('schooler','Schooler',30), ('tooclever','Too Clever',15), ('plankton','Plankton',10)])
points = dict(con.execute('SELECT code, points FROM tiers'))
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*.json'))):
    d = json.load(open(f))
    con.execute('INSERT INTO dives VALUES (?,?)', (d['dayNumber'], d['date']))
    for p in d['prompts']:
        pos = int(p['id'].lstrip('p'))
        cur = con.execute('INSERT INTO prompts (dive_number, position, text) VALUES (?,?,?)', (d['dayNumber'], pos, p['text']))
        pid = cur.lastrowid
        for a in p['answers']:
            assert points[a['tier']] == a['score']
        con.executemany('INSERT INTO answers (prompt_id, answer, tier) VALUES (?,?,?)',
                        [(pid, a['answer'], a['tier']) for a in p['answers']])
con.executescript('''
CREATE INDEX idx_answers_prompt ON answers(prompt_id);
CREATE INDEX idx_answers_answer ON answers(answer COLLATE NOCASE);
CREATE INDEX idx_prompts_dive   ON prompts(dive_number);
CREATE VIEW answers_flat AS
  SELECT d.date, d.dive_number, p.position AS prompt_no, p.text AS prompt,
         a.answer, t.label AS tier, t.points
  FROM answers a JOIN prompts p USING (prompt_id)
                 JOIN dives d   USING (dive_number)
                 JOIN tiers t   ON t.code = a.tier;
''')
con.commit(); con.execute('VACUUM'); con.close()
