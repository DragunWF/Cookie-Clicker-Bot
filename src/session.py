import json
from pathlib import Path


class Session:
    def __init__(self):
        self.start_data = {}
        self.end_data = {}
        self.result = None

    def save_session_stats(self, data, session_ending):
        session_stats = {}
        for index in range(1, len(data) - 2):
            if index <= 6 and index % 2 == 0:
                session_stats[data[index - 1]] = data[index]
                continue
            stat_data = [item.strip() for item in data[index].split(":")]
            session_stats[stat_data[0]] = stat_data[1]

        if not session_ending:
            self.start_data = session_stats
        else:
            self.end_data = session_stats

    def save_session(self):
        data = json.loads(Path("data/sessions.json").read_text())

        result = "Success" if self.result else "Interuptted"
        session_data = {"session_count": len(data),
                        "stats_from_start": self.start_data,
                        "stats_at_end": self.end_data,
                        "session_result": result}
        data.append(session_data)

        formatted = json.dumps(data, sort_keys=False,
                               indent=2, separators=(',', ': '))
        Path("data/session_data.json").write_text(formatted)
