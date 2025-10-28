import csv, os, time
from datetime import datetime
from pathlib import Path

class SessionLogger:
    def __init__(self, log_dir: str = "logs"):
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(log_dir, f"session_{ts}.csv")
        self.start_time = time.time()

        # otevři CSV a napiš hlavičku
        self.file = open(self.log_path, "w", newline="")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["t_sec", "joint", "current_rad", "command_rad"])
        print(f"[logger] Logging to {self.log_path}")

    def log_step(self, current_state: dict, command_state: dict):
        t = time.time() - self.start_time
        for joint, cmd_val in command_state.items():
            cur_val = current_state.get(joint, 0.0)
            self.writer.writerow([round(t, 4), joint, cur_val, cmd_val])

    def close(self):
        self.file.close()
        print(f"[logger] Session saved: {self.log_path}")
