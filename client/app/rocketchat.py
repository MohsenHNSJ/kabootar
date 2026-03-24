import requests


def login(rc_url: str, username: str, password: str) -> tuple[str, str]:
    r = requests.post(f"{rc_url.rstrip('/')}/api/v1/login", json={"user": username, "password": password}, timeout=30)
    r.raise_for_status()
    data = r.json().get("data", {})
    token = data.get("authToken")
    user_id = data.get("userId")
    if not token or not user_id:
        raise RuntimeError("rocket login failed")
    return token, user_id


def room_id_by_name(rc_url: str, token: str, user_id: str, room_name: str) -> str | None:
    r = requests.get(
        f"{rc_url.rstrip('/')}/api/v1/channels.info",
        params={"roomName": room_name},
        headers={"X-Auth-Token": token, "X-User-Id": user_id},
        timeout=30,
    )
    if not r.ok:
        return None
    return r.json().get("channel", {}).get("_id")


def post_message(rc_url: str, token: str, user_id: str, room_id: str, text: str) -> None:
    r = requests.post(
        f"{rc_url.rstrip('/')}/api/v1/chat.postMessage",
        json={"roomId": room_id, "text": text},
        headers={"X-Auth-Token": token, "X-User-Id": user_id},
        timeout=30,
    )
    r.raise_for_status()
