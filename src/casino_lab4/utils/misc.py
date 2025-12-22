def ensure_within_100(value: int|float) -> int|float:
    return max(min(value, 100), 0)
