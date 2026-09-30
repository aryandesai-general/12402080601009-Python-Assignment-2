"""Q6: Detect failure bursts followed by success from a different IP."""
from collections import defaultdict, deque
from datetime import datetime
import re
import sys

LOG_RE = re.compile(r"^(\d{2}:\d{2})\s+(\S+)\s+(\S+)\s+(FAIL|SUCCESS)$")


def minute_of_day(timestamp):
    parsed = datetime.strptime(timestamp, "%H:%M")
    return parsed.hour * 60 + parsed.minute


def main():
    try:
        x, window = map(int, sys.stdin.readline().split())
        n = int(sys.stdin.readline())
        if not 1 <= x <= 100 or not 1 <= window <= 1440 or n < 1:
            raise ValueError
    except ValueError:
        print("Invalid input."); return

    failures = defaultdict(deque)
    first_suspicious = {}
    for _ in range(n):
        line = sys.stdin.readline().strip()
        match = LOG_RE.fullmatch(line)
        if not match:
            print("Invalid log line:", line); return
        timestamp, user, ip, status = match.groups()
        now = minute_of_day(timestamp)
        queue = failures[user]
        while queue and now - queue[0][0] > window:
            queue.popleft()
        if status == "FAIL":
            queue.append((now, ip))
        elif user not in first_suspicious:
            if len(queue) >= x and any(failed_ip != ip for _, failed_ip in queue):
                first_suspicious[user] = timestamp

    for user in sorted(first_suspicious):
        print(user, first_suspicious[user])


if __name__ == "__main__":
    main()
