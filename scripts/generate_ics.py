import json
from datetime import datetime, timedelta


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
            f"UID:{m['match']}@ipl2026",
            f"DTSTAMP:{start.strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{start.strftime('%Y%m%dT%H%M%SZ')}",
            f"DTEND:{end.strftime('%Y%m%dT%H%M%SZ')}",
            f"SUMMARY:IPL {m['match']} \u2022 {m['home']} vs {m['away']}",
            f"LOCATION:{m['venue']}",
            f"DESCRIPTION:IPL 2026 Match {m['match']}\\n{m['home']} vs {m['away']}\\nVenue: {m['venue']}",
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


with open("data/ipl_2026.json") as f:
    matches = json.load(f)

# Full calendar
generate_ics(matches, "ipl.ics", "IPL 2026", "Full IPL 2026 schedule with all 70 matches")

# Team calendars
teams = {
    "RCB":  ("rcb.ics",  "RCB IPL 2026",  "Royal Challengers Bengaluru - IPL 2026 matches"),
    "MI":   ("mi.ics",   "MI IPL 2026",   "Mumbai Indians - IPL 2026 matches"),
    "CSK":  ("csk.ics",  "CSK IPL 2026",  "Chennai Super Kings - IPL 2026 matches"),
    "KKR":  ("kkr.ics",  "KKR IPL 2026",  "Kolkata Knight Riders - IPL 2026 matches"),
    "SRH":  ("srh.ics",  "SRH IPL 2026",  "Sunrisers Hyderabad - IPL 2026 matches"),
    "RR":   ("rr.ics",   "RR IPL 2026",   "Rajasthan Royals - IPL 2026 matches"),
    "GT":   ("gt.ics",   "GT IPL 2026",   "Gujarat Titans - IPL 2026 matches"),
    "LSG":  ("lsg.ics",  "LSG IPL 2026",  "Lucknow Super Giants - IPL 2026 matches"),
    "DC":   ("dc.ics",   "DC IPL 2026",   "Delhi Capitals - IPL 2026 matches"),
    "PBKS": ("pbks.ics", "PBKS IPL 2026", "Punjab Kings - IPL 2026 matches"),
}

for team, (filename, cal_name, cal_desc) in teams.items():
    team_matches = [m for m in matches if m["home"] == team or m["away"] == team]
    generate_ics(team_matches, filename, cal_name, cal_desc)