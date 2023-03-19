#!/usr/bin/env python3
from datetime import datetime, timedelta
import re
from sys import argv

class Globals:
    options = "RDdTtFf"

# Parse the "+6h23m" type arguments
def parse_timedelta(t:str) -> timedelta:
    adjustments = {"seconds":0,"minutes":0,"hours":0,"days":0,"weeks":0}
    t = t.lower()
    if match := re.search(r"(?P<n>[\d\.]+)s",t):
        adjustments["seconds"] = float(match['n'])
    if match := re.search(r"(?P<n>[\d\.]+)m",t):
        adjustments["minutes"] = float(match['n'])
    if match := re.search(r"(?P<n>[\d\.]+)h",t):
        adjustments["hours"] = float(match['n'])
    if match := re.search(r"(?P<n>[\d\.]+)d",t):
        adjustments["days"] = float(match['n'])
    if match := re.search(r"(?P<n>[\d\.]+)w",t):
        adjustments["weeks"] = float(match['n'])
    return timedelta(**adjustments)

# Format for displaying and output
def discord_format(date:datetime, format:str, displayed:bool=False) -> str:
    if not displayed:
        return f"<t:{date.timestamp():.0f}:{format}>"
    if format == "R":
        return "0 seconds ago (example)"
    if format == "D":
        return date.strftime("%B ") + date.strftime("%d").strip("0") + date.strftime(", %Y")
    if format == "d":
        return date.strftime('%x')
    if format == "T":
        return date.strftime("%I:%M:%S %p").strip("0")
    if format == "t":
        return date.strftime("%I:%M %p").strip("0")
    if format == "F":
        return date.strftime("%A, %B ") + date.strftime("%d").strip("0") + date.strftime(", %Y ") + date.strftime("%I:%M:%S %p").strip("0")
    if format == "f":
        return date.strftime("%d %B %Y ") + date.strftime("%I:%M-").strip("0").strip("-")
    return ""

# Parse "@5:20pm" type arguments
def extract_time(now:datetime, time:str) -> datetime:
    formats_w_minutes = [
        "@%I:%M%p",
        "@%Hh%Mm"
    ]
    formats_wo_minutes = [
        "@%I%p",
        "@%Hh"
    ]
    if time.startswith('@'):
        for f in formats_w_minutes:
            try:
                today = datetime.strptime(time, f)
                return datetime(
                    year=now.year,
                    month=now.month,
                    day=now.day,
                    hour=today.hour,
                    minute=today.minute,
                    second=today.second,
                    tzinfo=now.tzinfo,
                )
            except ValueError:
                pass
        for f in formats_wo_minutes:
            try:
                today = datetime.strptime(time, f)
                return datetime(
                    year=now.year,
                    month=now.month,
                    day=now.day,
                    hour=today.hour,
                    minute=today.minute,
                    second=today.second,
                    tzinfo=now.tzinfo,
                )
            except ValueError:
                pass
    else:
        return now

# Parse "on:01/01/1900" type arguments
def extract_date(today:datetime, date:str) -> datetime:
    formats_w_year = [
        "on %B %d, %Y",
        "on %B %d, %y",
        "on %b %d, %Y",
        "on %b %d, %y",
        "on %B %d %Y",
        "on %B %d %y",
        "on %b %d %Y",
        "on %b %d %y",
        "on %B %dth, %Y",
        "on %B %dth, %y",
        "on %b %dth, %Y",
        "on %b %dth, %y",
        "on %B %dth %Y",
        "on %B %dth %y",
        "on %b %dth %Y",
        "on %b %dth %y",
        "on:%d/%m/%Y",
        "on:%d/%m/%y",
    ]
    formats_wo_year = [
        "on %B %d",
        "on %B %d",
        "on %b %d",
        "on %b %d",
        "on %B %dth",
        "on %B %dth",
        "on %b %dth",
        "on %b %dth",
        "on:%d/%m",
    ]    
    if date.startswith("on"):
        for f in formats_w_year:
            try:
                new_date = datetime.strptime(date, f)
                return datetime(
                    year=new_date.year,
                    month=new_date.month,
                    day=new_date.day,
                    hour=today.hour,
                    minute=today.minute,
                    second=today.second,
                    tzinfo=today.tzinfo,
                )
            except ValueError:
                pass
        for f in formats_wo_year:
            try:
                new_date = datetime.strptime(date, f)
                return datetime(
                    year=today.year,
                    month=new_date.month,
                    day=new_date.day,
                    hour=today.hour,
                    minute=today.minute,
                    second=today.second,
                    tzinfo=today.tzinfo,
                )
            except ValueError:
                pass
    return today

def main():
    # Get the current times
    now = datetime.now()

    # Check for help message
    if "--help" in argv or "-h" in argv:
        print("TODO: write help message")
        return

    # Extract user selected format
    selected_format = "F"
    for f in Globals.options:
        if f"-{f}" in argv:
            selected_format = f
    # Extract user specified time
    for arg in argv:
        if arg.startswith('@'):
            now = extract_time(now, arg)
    # Extract user specified date
    for arg in argv:
        if arg.startswith("on"):
            now = extract_date(now, arg)
    # Get time adjustments
    for arg in argv:
        if arg.startswith('+'):
            now = now + parse_timedelta(arg)
        if arg.startswith('-'):
            now = now - parse_timedelta(arg)

    # Output timestamp
    stamp = discord_format(now, selected_format)
    print(stamp)

    # Print timestamp in all available formats
    print("All available formats:")
    print(f"  -R {discord_format(now,'R')}: {discord_format(now,'R',True)}")
    print(f"  -D {discord_format(now,'D')}: {discord_format(now,'D',True)}")
    print(f"  -d {discord_format(now,'d')}: {discord_format(now,'d',True)}")
    print(f"  -T {discord_format(now,'T')}: {discord_format(now,'T',True)}")
    print(f"  -t {discord_format(now,'t')}: {discord_format(now,'t',True)}")
    print(f"  -F {discord_format(now,'F')}: {discord_format(now,'F',True)}")
    print(f"  -f {discord_format(now,'f')}: {discord_format(now,'f',True)}")
    
    # Try copying the selected timestamp to clipboard
    try:
        import pyperclip as pc
        pc.copy(stamp)
    except ModuleNotFoundError:
        print("pyperclip not installed, timestamp not copied to clipboard")
        print("to install, use python3 -m pip install pyperclip")

if __name__ == "__main__":
    main()
