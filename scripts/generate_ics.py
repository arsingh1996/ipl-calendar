import json
from datetime import datetime, timedelta

# ── Config ────────────────────────────────────────────────
YEAR        = 2026
INPUT_FILE  = f"data/ipl_{YEAR}.json"
# ─────────────────────────────────────────────────────────


def ist_to_utc(date_str, time_str):
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    return dt - timedelta(hours=5, minutes=30)


def generate_ics(matches, filename, cal_name, cal_desc):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//IPL Calendar//EN",
        f"X-WR-CALNAME:{cal_name}",
        "X-WR-TIMEZONE:Asia/Kolkata",
        f"X-WR-CALDESC:{cal_desc}",
        "CALSCALE:GREGORIAN"
    ]

    for m in matches:
        start = ist_to_utc(m["date"], m["time"])
        end = start + timedelta(hours=3)
        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{m['match']}@ipl{YEAR}",
            f"DTSTAMP:{start.strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{start.strftime('%Y%m%dT%H%M%SZ')}",
            f"DTEND:{end.strftime('%Y%m%dT%H%M%SZ')}",
            f"SUMMARY:IPL {m['match']} \u2022 {m['home']} vs {m['away']}",
            f"LOCATION:{m['venue']}",
            f"DESCRIPTION:IPL {YEAR} Match {m['match']}\\n{m['home']} vs {m['away']}\\nVenue: {m['venue']}",
            "BEGIN:VALARM",
            "TRIGGER:-PT30M",
            "ACTION:DISPLAY",
            "DESCRIPTION:Match starting in 30 minutes",
            "END:VALARM",
            "BEGIN:VALARM",
            "TRIGGER:-PT10M",
            "ACTION:DISPLAY",
            "DESCRIPTION:Match starting in 10 minutes",
            "END:VALARM",
            "END:VEVENT"
        ])

    lines.append("END:VCALENDAR")

    with open(f"dist/{filename}", "w") as f:
        f.write("\n".join(lines))

    print(f"✅ Generated dist/{filename} ({len(matches)} matches)")


with open(INPUT_FILE) as f:
    matches = json.load(f)

# Full calendar
generate_ics(matches, "ipl.ics", f"IPL {YEAR}", f"Full IPL {YEAR} schedule with all {len(matches)} matches")

# Team calendars
teams = {
    "RCB":  ("rcb.ics",  f"RCB IPL {YEAR}",  "Royal Challengers Bengaluru - IPL {YEAR} matches"),
    "MI":   ("mi.ics",   f"MI IPL {YEAR}",   "Mumbai Indians - IPL {YEAR} matches"),
    "CSK":  ("csk.ics",  f"CSK IPL {YEAR}",  "Chennai Super Kings - IPL {YEAR} matches"),
    "KKR":  ("kkr.ics",  f"KKR IPL {YEAR}",  "Kolkata Knight Riders - IPL {YEAR} matches"),
    "SRH":  ("srh.ics",  f"SRH IPL {YEAR}",  "Sunrisers Hyderabad - IPL {YEAR} matches"),
    "RR":   ("rr.ics",   f"RR IPL {YEAR}",   "Rajasthan Royals - IPL {YEAR} matches"),
    "GT":   ("gt.ics",   f"GT IPL {YEAR}",   "Gujarat Titans - IPL {YEAR} matches"),
    "LSG":  ("lsg.ics",  f"LSG IPL {YEAR}",  "Lucknow Super Giants - IPL {YEAR} matches"),
    "DC":   ("dc.ics",   f"DC IPL {YEAR}",   "Delhi Capitals - IPL {YEAR} matches"),
    "PBKS": ("pbks.ics", f"PBKS IPL {YEAR}", "Punjab Kings - IPL {YEAR} matches"),
}

for team, (filename, cal_name, cal_desc) in teams.items():
    team_matches = [m for m in matches if m["home"] == team or m["away"] == team]
    generate_ics(team_matches, filename, cal_name, cal_desc)