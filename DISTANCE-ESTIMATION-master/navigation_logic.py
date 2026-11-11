"""Small, hardware-independent helpers for the historical hackathon prototype."""

def direction_for_offset(x, threshold=10):
    """Return a direction from marker-relative horizontal translation."""
    if x > threshold:
        return "left"
    if x < -threshold:
        return "right"
    return None


def should_announce(event, last_event, last_time, now, cooldown=5.0):
    """Suppress identical announcements during a short cooldown."""
    return event != last_event or now - last_time >= cooldown


def marker_message(marker_id, records):
    """Look up descriptions by marker ID, not JSON list position."""
    if marker_id == 0:
        names = [str(row["name"]) for row in records
                 if 1 <= row.get("id", -1) <= 9 and row.get("name")]
        return ", ".join(names), "en"
    if 1 <= marker_id <= 3 or marker_id > 40:
        for row in records:
            if row.get("id") == marker_id:
                return row.get("output", ""), "zh-TW"
    return "", "zh-TW"
