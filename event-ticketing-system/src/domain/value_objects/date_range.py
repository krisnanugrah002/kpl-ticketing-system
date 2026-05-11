from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class DateRange:
    start_date: datetime
    end_date: datetime

    def __post_init__(self):
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be earlier than start date.")

    def is_within_range(self, date_to_check: datetime) -> bool:
        """
        Fungsi bantuan untuk mengecek apakah suatu tanggal (misal saat pelanggan mau beli tiket)
        masih berada di dalam periode jadwal ini.
        """
        return self.start_date <= date_to_check <= self.end_date