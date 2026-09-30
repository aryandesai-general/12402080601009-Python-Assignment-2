"""Q1: Stream a text file and summarize unique .com/.edu/.org email addresses."""
import re
import sys
from collections import defaultdict

EMAIL_RE = re.compile(
    r"(?<![A-Za-z0-9._+-])([A-Za-z0-9._+-]+@(?:[A-Za-z0-9-]+\.)+(?:com|edu|org))\b",
    re.IGNORECASE,
)


def extract_emails(path):
    unique_by_domain = defaultdict(set)
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            for match in EMAIL_RE.finditer(line):
                email = match.group(1)
                local, domain = email.rsplit("@", 1)
                # Reject empty labels and labels with leading/trailing hyphens.
                labels = domain.split(".")
                if any(not label or label.startswith("-") or label.endswith("-") for label in labels):
                    continue
                unique_by_domain[domain.lower()].add(f"{local}@{domain.lower()}")
    return unique_by_domain


def main():
    path = input("Text file path: ").strip()
    try:
        groups = extract_emails(path)
    except OSError as exc:
        print(f"File error: {exc}")
        return
    for domain in sorted(groups):
        emails = groups[domain]
        print(domain, len(emails), min(emails))


if __name__ == "__main__":
    main()
