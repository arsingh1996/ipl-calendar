import json
from datetime import datetime, timedelta

def ist_to_utc(date_str, time_str):
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    return dt - timedelta(hours=5, minutes=30)

with open("data/ipl_2026.json") as f:
    matches = json.load(f)

lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//IPL Calendar//EN",
    "X-WR-CALNAME:IPL 2026",
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
        f"SUMMARY:IPL {m['match']} • {m['home']} vs {m['away']}",
        f"LOCATION:{m['venue']}",
        f"DESCRIPTION:IPL 2026 Match {m['match']}\\n{m['home']} vs {m['away']}\\nVenue: {m['venue']}",
        "BEGIN:VALARM",
        "TRIGGER:-PT30M",
        "ACTION:DISPLAY",
        "DESCRIPTION:Match starting in 30 minutes",
        "END:VALARM",
        "END:VEVENT"
    ])

lines.append("END:VCALENDAR")

with open("dist/ipl.ics", "w") as f:
    f.write("\n".join(lines))

print("✅ ICS file generated at dist/ipl.ics")