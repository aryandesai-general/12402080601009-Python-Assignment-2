"""Q7: Streaming JSONL ETL with per-device temperature summaries."""
import json
import math


def read_records(path):
    """Yield one parsed JSON object at a time; never load the whole file."""
    with open(path, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            try:
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError("record is not an object")
                yield line_number, record, None
            except (json.JSONDecodeError, ValueError) as exc:
                yield line_number, None, str(exc)


def valid_record(record):
    if not record or not record.get("device_id"):
        return False
    try:
        temperature = float(record["temperature_c"])
        humidity = float(record["humidity"])
        return math.isfinite(temperature) and math.isfinite(humidity) and 0 <= humidity <= 100
    except (KeyError, TypeError, ValueError):
        return False


def main():
    path = input("JSONL file path: ").strip()
    stats = {}
    corrupted = 0
    try:
        for _, record, error in read_records(path):
            if error or not valid_record(record):
                corrupted += 1
                continue
            device = str(record["device_id"])
            temp = float(record["temperature_c"])
            if device not in stats:
                stats[device] = {"count": 0, "min": temp, "max": temp, "sum": 0.0}
            item = stats[device]
            item["count"] += 1
            item["min"] = min(item["min"], temp)
            item["max"] = max(item["max"], temp)
            item["sum"] += temp
    except OSError as exc:
        print("File error:", exc); return

    for device in sorted(stats):
        s = stats[device]
        print(f"{device} count={s['count']} min={s['min']:g} max={s['max']:g} "
              f"avg={s['sum']/s['count']:.2f} corrupted={corrupted}")


if __name__ == "__main__":
    main()
