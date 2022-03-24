import json
from pathlib import Path


class Session:
    def __init__(self):
        self.cookies_from_start = 0
        self.cookies_at_end = 0
        self.cookies_gained = 0
        self.upgrades_bought = 0

        self.save_file_loaded = None
        self.result = None

    def save_session(self):
        data = json.loads(Path("data/session.json").read_text())

        result = "Success" if self.result else "Error"
        session_data = {"cookies_gained": self.cookies_gained,
                        "cookies_from_start": self.cookies_from_start,
                        "cookies_at_end": self.cookies_at_end,
                        "upgrades_bought": self.upgrades_bought,
                        "save_file_loaded": self.save_file_loaded,
                        "end_result": result}
        data.append(session_data)

        formatted = json.dumps(data, sort_keys=False,
                               indent=2, separators=(',', ': '))
        Path("data/session_data.json").write_text(formatted)
