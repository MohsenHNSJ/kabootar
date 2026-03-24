import re


def normalize_tg_s_url(value: str) -> str:
    v = value.strip().lstrip("@")
    if not v:
        raise ValueError("empty channel value")

    if v.startswith("http://") or v.startswith("https://"):
        v = v.replace("http://", "https://").rstrip("/")
        if "/s/" in v:
            return v
        if "t.me/" in v:
            username = v.rsplit("/", 1)[-1]
            return f"https://t.me/s/{username}"

    if "t.me/s/" in v:
        return ("https://" + v if not v.startswith("http") else v).replace("http://", "https://").rstrip("/")

    if "t.me/" in v:
        username = v.rsplit("/", 1)[-1]
        return f"https://t.me/s/{username}"

    return f"https://t.me/s/{v}".rstrip("/")


def parse_csv(value: str) -> list[str]:
    return [x.strip() for x in re.split(r"[,;\n\r،]+", value or "") if x.strip()]


def normalize_proxy_url(value: str) -> str:
    v = (value or "").strip()
    if not v:
        return ""
    # already standard
    if "://" in v and "@" in v:
        return v
    # custom: scheme://ip:port:user:pass
    m = re.match(r"^([a-zA-Z0-9]+)://([^:]+):(\d+):([^:]+):(.+)$", v)
    if m:
        scheme, host, port, user, pwd = m.groups()
        return f"{scheme}://{user}:{pwd}@{host}:{port}"
    return v
