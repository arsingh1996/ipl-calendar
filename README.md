# 🏏 IPL 2026 Calendar

A self-hosted, auto-updating IPL 2026 schedule — subscribe once and your calendar stays current forever.

**Live dashboard → [arsingh1996.github.io/ipl-calendar](https://arsingh1996.github.io/ipl-calendar)**

---

## Subscribe

| Calendar | URL |
|----------|-----|
| All matches | `https://raw.githubusercontent.com/arsingh1996/ipl-calendar/main/dist/ipl.ics` |
| RCB | `https://raw.githubusercontent.com/arsingh1996/ipl-calendar/main/dist/rcb.ics` |
| MI | `https://raw.githubusercontent.com/arsingh1996/ipl-calendar/main/dist/mi.ics` |
| CSK | `https://raw.githubusercontent.com/arsingh1996/ipl-calendar/main/dist/csk.ics` |
| KKR | `https://raw.githubusercontent.com/arsingh1996/ipl-calendar/main/dist/kkr.ics` |
| SRH | `https://raw.githubusercontent.com/arsingh1996/ipl-calendar/main/dist/srh.ics` |
| RR | `https://raw.githubusercontent.com/arsingh1996/ipl-calendar/main/dist/rr.ics` |
| GT | `https://raw.githubusercontent.com/arsingh1996/ipl-calendar/main/dist/gt.ics` |
| LSG | `https://raw.githubusercontent.com/arsingh1996/ipl-calendar/main/dist/lsg.ics` |
| DC | `https://raw.githubusercontent.com/arsingh1996/ipl-calendar/main/dist/dc.ics` |
| PBKS | `https://raw.githubusercontent.com/arsingh1996/ipl-calendar/main/dist/pbks.ics` |

### Apple Calendar
1. Open Calendar → File → New Calendar Subscription
2. Paste the URL → Subscribe
3. Set auto-refresh to every hour

### Google Calendar
1. Open Google Calendar → Other calendars → From URL
2. Paste the URL → Add calendar

---

## How it works

```
JSON schedule data
      ↓
Python script (IST → UTC conversion)
      ↓
.ics files in dist/
      ↓
GitHub raw URL (public CDN)
      ↓
Your calendar app (auto-refreshing subscription)
```

- **Source of truth** — `data/ipl_2026.json` contains all 70 league matches + 4 playoff fixtures
- **Auto-generation** — GitHub Actions regenerates all `.ics` files on every push
- **Team calendars** — each team gets its own `.ics` with their 14 league matches + all 4 playoff fixtures
- **Playoffs** — included with `TBD` teams; updated in JSON as qualifiers are confirmed

---

## Project structure

```
ipl-calendar/
├── data/
│   └── ipl_2026.json          # Schedule data (edit this)
├── scripts/
│   └── generate_ics.py        # Generates all .ics files
├── dist/
│   ├── ipl.ics                # Full season calendar
│   ├── rcb.ics                # Team-specific calendars
│   ├── mi.ics
│   └── ...
├── index.html                 # Web dashboard (GitHub Pages)
├── .github/
│   └── workflows/
│       └── generate-ics.yml   # Auto-regeneration on push
└── README.md
```

---

## Updating the schedule

### Update a match (e.g. venue change)
1. Edit `data/ipl_2026.json`
2. `git add data/ipl_2026.json && git commit -m "fix: update venue for match X" && git push`
3. GitHub Actions automatically regenerates all `.ics` files

### Update playoff teams (as they qualify)
Find the playoff entries at the bottom of `ipl_2026.json` and replace `TBD` with actual team codes:

```json
{ "match": "Qualifier 1", "date": "2026-05-26", "time": "19:30", "home": "RCB", "away": "MI", "venue": "Ahmedabad" }
```

Then push — everything updates automatically.

### Running the script locally
```bash
cd ipl-calendar
python3 scripts/generate_ics.py
```

---

## Calendar features

- ✅ All 70 league matches + 4 playoff fixtures
- ✅ IST times converted to UTC for universal compatibility
- ✅ 3-hour match duration
- ✅ Venue and match description on every event
- ✅ 30-minute and 10-minute pre-match reminders
- ✅ Team-specific calendars (14 league + 4 playoffs each)
- ✅ Auto-regeneration via GitHub Actions

---

## Next season (IPL 2027)

1. Add `data/ipl_2027.json` with the new schedule
2. Change `YEAR = 2026` → `YEAR = 2027` in `scripts/generate_ics.py`
3. Push — the same subscription URLs update automatically

---

## Tech stack

- **Python 3** — ICS generation
- **GitHub Actions** — automation
- **GitHub Pages** — web dashboard hosting
- **GitHub raw files** — `.ics` hosting (acts as a public CDN)