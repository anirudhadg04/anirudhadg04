#!/usr/bin/env python3
"""
Fetch live daily contribution counts from GitHub's public contributions endpoint
for anirudhadg04 and write data/contributions.json with raw days and calculated stats
(current streak, longest streak, active days, best day, monthly totals).

No token or authentication required.
"""
import datetime
import json
import os
import re
import sys
import requests
from html.parser import HTMLParser

USERNAME = os.environ.get("GH_PROFILE_USER", "anirudhadg04")
URL = f"https://github.com/users/{USERNAME}/contributions"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "..", "data", "contributions.json")

class GitHubContributionsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []
        self.tooltips = {}
        self.current_for = None
        self.current_text = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "td" and "data-date" in attr_dict:
            date = attr_dict.get("data-date")
            level = int(attr_dict.get("data-level", 0))
            td_id = attr_dict.get("id")
            count = int(attr_dict.get("data-count", 0))
            self.days.append({"date": date, "level": level, "id": td_id, "count": count})
        elif tag == "tool-tip" and "for" in attr_dict:
            self.current_for = attr_dict["for"]
            self.current_text = []

    def handle_data(self, data):
        if self.current_for:
            self.current_text.append(data)

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.current_for:
            text = "".join(self.current_text).strip()
            self.tooltips[self.current_for] = text
            self.current_for = None

def fetch_and_build():
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=30)
    resp.raise_for_status()

    parser = GitHubContributionsParser()
    parser.feed(resp.text)

    days = parser.days
    for d in days:
        td_id = d.get("id")
        if td_id and td_id in parser.tooltips:
            tip = parser.tooltips[td_id]
            if "no contributions" in tip.lower():
                d["count"] = 0
            else:
                m = re.match(r"(\d+)", tip)
                if m:
                    d["count"] = int(m.group(1))

    days.sort(key=lambda x: x["date"])

    total_contribs = sum(d["count"] for d in days)
    active_days = sum(1 for d in days if d["count"] > 0)
    best_day = max(days, key=lambda d: d["count"]) if days else {"date": "N/A", "count": 0}

    cur_len = 0
    cur_start = None
    cur_end = None
    idx = len(days) - 1
    if idx >= 0 and days[idx]["count"] == 0:
        idx -= 1

    if idx >= 0:
        cur_end = days[idx]["date"]
        while idx >= 0 and days[idx]["count"] > 0:
            cur_len += 1
            idx -= 1
        cur_start = days[idx + 1]["date"] if cur_len > 0 else None

    longest_len = 0
    longest_start = None
    longest_end = None
    temp_len = 0
    temp_start = None
    for d in days:
        if d["count"] > 0:
            if temp_len == 0:
                temp_start = d["date"]
            temp_len += 1
            if temp_len > longest_len:
                longest_len = temp_len
                longest_start = temp_start
                longest_end = d["date"]
        else:
            temp_len = 0

    monthly = {}
    for d in days:
        k = d["date"][:7]
        monthly[k] = monthly.get(k, 0) + d["count"]
    monthly_list = [{"month": k, "total": v} for k, v in sorted(monthly.items())]

    result = {
        "username": USERNAME,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]} if days else {"start": "", "end": ""},
        "total_contributions": total_contribs,
        "active_days": active_days,
        "avg_per_active_day": round(total_contribs / active_days, 1) if active_days else 0,
        "current_streak": {"length": cur_len, "start": cur_start, "end": cur_end},
        "longest_streak": {"length": longest_len, "start": longest_start, "end": longest_end},
        "best_day": {"date": best_day["date"], "count": best_day["count"]},
        "monthly": monthly_list,
        "days": days
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Updated {OUT_PATH}: {total_contribs} contributions, streak: {cur_len}, best: {best_day['count']}")

if __name__ == "__main__":
    fetch_and_build()
