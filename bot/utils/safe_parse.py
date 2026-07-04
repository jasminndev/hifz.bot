def parse_callback_int(data: str, index: int, separator: str = "_") -> int | None:
    try:
        parts = data.split(separator)
        return int(parts[index])
    except (IndexError, ValueError):
        return None
