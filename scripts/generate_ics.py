import json
from datetime import datetime, timedelta
 
# ── Config ────────────────────────────────────────────────
YEAR       = 2026
INPUT_FILE = f"data/ipl_{YEAR}.json"
# ─────────────────────────────────────────────────────────
 
PLAYOFF_MATCHES = {"Qualifier 1", "Eliminator", "Qualifier 2", "Final"}
 
 
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
        is_playoff = m["match"] in PLAYOFF_MATCHES
 
        if is_playoff:
            summary = f"IPL {YEAR} {m['match']}"
            if m["home"] != "TBD":
                summary += f" \u2022 {m['home']} vs {m['away']}"
            desc = f"IPL {YEAR} {m['match']}\\nVenue: {m['venue']}"
        else:
            summary = f"IPL {m['match']} \u2022 {m['home']} vs {m['away']}"
            desc = f"IPL {YEAR} Match {m['match']}\\n{m['home']} vs {m['away']}\\nVenue: {m['venue']}"
 
        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{str(m['match']).replace(' ', '-').lower()}@ipl{YEAR}",
            f"DTSTAMP:{start.strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{start.strftime('%Y%m%dT%H%M%SZ')}",
            f"DTEND:{end.strftime('%Y%m%dT%H%M%SZ')}",
            f"SUMMARY:{summary}",
            f"LOCATION:{m['venue']}",
            f"DESCRIPTION:{desc}",
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
    all_matches = json.load(f)
 
league_matches = [m for m in all_matches if m["match"] not in PLAYOFF_MATCHES]
playoff_matches = [m for m in all_matches if m["match"] in PLAYOFF_MATCHES]
 
# Full calendar (league + playoffs)
generate_ics(all_matches, "ipl.ics", f"IPL {YEAR}", f"Full IPL {YEAR} schedule — {len(league_matches)} league matches + playoffs")
 
# Team calendars (league matches for that team + all playoffs)
teams = {
    "RCB":  ("rcb.ics",  f"RCB IPL {YEAR}",  f"Royal Challengers Bengaluru — IPL {YEAR}"),
    "MI":   ("mi.ics",   f"MI IPL {YEAR}",   f"Mumbai Indians — IPL {YEAR}"),
    "CSK":  ("csk.ics",  f"CSK IPL {YEAR}",  f"Chennai Super Kings — IPL {YEAR}"),
    "KKR":  ("kkr.ics",  f"KKR IPL {YEAR}",  f"Kolkata Knight Riders — IPL {YEAR}"),
    "SRH":  ("srh.ics",  f"SRH IPL {YEAR}",  f"Sunrisers Hyderabad — IPL {YEAR}"),
    "RR":   ("rr.ics",   f"RR IPL {YEAR}",   f"Rajasthan Royals — IPL {YEAR}"),
    "GT":   ("gt.ics",   f"GT IPL {YEAR}",   f"Gujarat Titans — IPL {YEAR}"),
    "LSG":  ("lsg.ics",  f"LSG IPL {YEAR}",  f"Lucknow Super Giants — IPL {YEAR}"),
    "DC":   ("dc.ics",   f"DC IPL {YEAR}",   f"Delhi Capitals — IPL {YEAR}"),
    "PBKS": ("pbks.ics", f"PBKS IPL {YEAR}", f"Punjab Kings — IPL {YEAR}"),
}
 
for team, (filename, cal_name, cal_desc) in teams.items():
    team_matches = [m for m in league_matches if m["home"] == team or m["away"] == team]
    generate_ics(team_matches + playoff_matches, filename, cal_name, cal_desc)