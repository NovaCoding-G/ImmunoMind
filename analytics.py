"""Export CSV delle simulazioni. © G.Roscino / NovaCoding."""

import csv
import os
from datetime import datetime
from typing import Dict, List, Any

from config import EXPORT_DIR, LOG_INTERVAL


class SimulationLogger:

    def __init__(self, run_id: str, enabled: bool = True):
        self.run_id = run_id
        self.enabled = enabled
        self._records: List[Dict[str, Any]] = []
        self._accumulatore_tempo = 0.0

    def update(self, dt_sim: float, stats: Dict[str, Any]) -> None:
        if not self.enabled:
            return

        self._accumulatore_tempo += dt_sim
        if self._accumulatore_tempo < LOG_INTERVAL:
            return

        self._accumulatore_tempo = 0.0
        record = dict(stats)
        record.setdefault("run_id", self.run_id)
        self._records.append(record)

    def has_data(self) -> bool:
        return bool(self._records)

    def export_csv(self, note: str = "") -> str:
        if not self._records:
            return ""

        os.makedirs(EXPORT_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_note = note.replace(" ", "_") if note else ""
        filename = f"immunomind_run_{self.run_id}_{timestamp}"
        if safe_note:
            filename += f"_{safe_note}"
        filename += ".csv"

        path = os.path.join(EXPORT_DIR, filename)

        all_keys = set()
        for r in self._records:
            all_keys.update(r.keys())
        fieldnames = sorted(all_keys)

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in self._records:
                writer.writerow(r)

        return path
