# Krillion answers archive (SQLite)

Every saved dive from <https://krilliongame.com/krillion-answers/>:
**113 dives (2026-07-16 → 2026-11-06), 791 prompts, 756,289 answers.**
Dive #111 (2026-11-03) isn't on the site, so it's missing here too.

```bash
gunzip -k krillion_answers.sqlite.gz
sqlite3 krillion_answers.sqlite
```

## Schema

```
tiers   (code PK, label, points)                 -- 6 rows
dives   (dive_number PK, date UNIQUE)
prompts (prompt_id PK, dive_number FK, position 1-7, text)
answers (answer_id PK, prompt_id FK, answer, tier FK -> tiers.code)
VIEW answers_flat (date, dive_number, prompt_no, prompt, answer, tier, points)
```

| tier code | label | points |
|---|---|---|
| krillion | One in a Krillion | 100 |
| deepcut | Deep Cut | 85 |
| rare | Rare | 60 |
| schooler | Schooler | 30 |
| tooclever | Too Clever | 15 |
| plankton | Plankton | 10 |

## Practice queries

```sql
-- The 100-point answer(s) for every prompt on a given day
SELECT prompt_no, prompt, answer FROM answers_flat
WHERE date = '2026-11-06' AND points = 100;

-- Answer count per tier per prompt (GROUP BY + conditional aggregation)
SELECT p.prompt_id, p.text,
       SUM(a.tier = 'krillion') AS krillion, SUM(a.tier = 'plankton') AS plankton, COUNT(*) AS total
FROM prompts p JOIN answers a USING (prompt_id)
GROUP BY p.prompt_id ORDER BY total DESC LIMIT 10;

-- Answers that show up across many prompts, with their average score
SELECT a.answer, COUNT(DISTINCT a.prompt_id) AS prompts, AVG(t.points) AS avg_pts
FROM answers a JOIN tiers t ON t.code = a.tier
GROUP BY a.answer COLLATE NOCASE HAVING prompts >= 5 ORDER BY prompts DESC LIMIT 20;

-- Max attainable score per dive (window function)
SELECT date, SUM(best) FROM (
  SELECT d.date, MAX(t.points) OVER (PARTITION BY p.prompt_id) AS best,
         ROW_NUMBER() OVER (PARTITION BY p.prompt_id) AS rn
  FROM dives d JOIN prompts p USING (dive_number)
  JOIN answers a USING (prompt_id) JOIN tiers t ON t.code = a.tier
) WHERE rn = 1 GROUP BY date ORDER BY date;
```

## Rebuilding / updating

```bash
python3 crawl.py raw                              # downloads only dates not already in raw/
python3 build.py raw krillion_answers.sqlite
gzip -9 -kf krillion_answers.sqlite
```

Data comes from a third-party fan archive (not the official game) and is for
personal study only. Its robots.txt opts out of AI training (`ai-train=no`), so
don't use it for that.
