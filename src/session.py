import json
from pathlib import Path


class Session:
    def __init__(self):
        self.cookies_from_start = 0
        self.cookies_at_end = 0
        self.cookies_gained = 0
        self.save_file_loaded = None

    def save_session(self):
        data = json.loads(Path("data/session.json").read_text())

        session_data = {"cookies_from_start": self.cookies_from_start,
                        "cookies_at_end": self.cookies_at_end,
                        "cookies_gained": self.cookies_gained,
                        "save_file_loaded": self.save_file_loaded}
        data.append(session_data)

        formatted = json.dumps(data, sort_keys=False,
                               indent=2, separators=(',', ': '))
        Path("data/session_data.json").write_text(formatted)
