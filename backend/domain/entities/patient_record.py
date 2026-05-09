from dataclasses import dataclass
from pathlib import Path


@dataclass
class PatientRecord:
    file_path: Path
    file_name: str

    @classmethod
    def from_path(cls, csv_path):
        path = Path(csv_path)
        return cls(
            file_path=path,
            file_name=path.name
        )