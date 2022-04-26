import json
from pathlib import Path


class Session:
    def __init__(self):
        self.__start_data = {}
        self.__end_data = {}
        self.save_file_loaded = False

    def save_session_stats(self, data: list, session_ending: bool):
        session_stats = {}
        for index in range(1, len(data) - 2):
            if index <= 6 and index % 2 == 0:
                property_name = "".join(data[index - 1].split(":")).strip()
                session_stats[property_name] = data[index]
            elif not index in (1, 3, 5):
                stat_data = [item.strip() for item in data[index].split(":")]
                session_stats[stat_data[0]] = stat_data[1]

        if not session_ending:
            self.__start_data = session_stats
        else:
            self.__end_data = session_stats

    def save_session(self):
        data = json.loads(Path("data/sessions.json").read_text())

        save_file_data = {"saves": {"loaded": self.save_file_loaded, "file_location": None}}
        if self.save_file_loaded:
            save_settings = json.loads(
                Path("data/settings.json").read_text())[0]["saves"]
            save_file_data["saves"]["file_location"] = save_settings["location"]

        session_data = {"session_count": len(data) + 1,
                        "save_file": save_file_data,
                        "stats_from_start": self.__start_data,
                        "stats_at_end": self.__end_data}
        data.append(session_data)

        formatted = json.dumps(data, sort_keys=False,
                               indent=2, separators=(',', ': '))
        Path("data/sessions.json").write_text(formatted)
