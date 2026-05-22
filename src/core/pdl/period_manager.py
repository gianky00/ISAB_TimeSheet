"""SyncroJob - PDL Period Manager.

Logica di business per il calcolo dei range settimanali e degli header temporali.
"""

from datetime import UTC, datetime, timedelta


class PDLPeriodManager:
    """Gestore dei periodi temporali per la programmazione PDL."""

    @staticmethod
    def get_week_range(offset_weeks: int = 0) -> tuple[str, str, datetime]:
        """Calcola il range della settimana basato sull'offset rispetto alla corrente.

        Returns: (start_str, end_str, start_datetime).
        """
        today = datetime.now(UTC).astimezone()
        current_weekday = today.weekday()
        # Inizio settimana (Luned )
        start_current = today - timedelta(days=current_weekday)

        start_target = start_current + timedelta(weeks=offset_weeks)
        end_target = start_target + timedelta(days=6)

        return (start_target.strftime("%d/%m/%Y"), end_target.strftime("%d/%m/%Y"), start_target)

    @staticmethod
    def get_table_headers(start_dt: datetime) -> list[str]:
        """Genera gli header delle colonne con le date dei giorni della settimana."""
        days = [(start_dt + timedelta(days=i)).strftime("%d/%m") for i in range(7)]
        return [
            "Richiedente",
            "Area",
            "Unità",
            "N  PDL",
            "Descrizione",
            f"LUN {days[0]}",
            f"MAR {days[1]}",
            f"MER {days[2]}",
            f"GIO {days[3]}",
            f"VEN {days[4]}",
            f"SAB {days[5]}",
            f"DOM {days[6]}",
        ]

    @staticmethod
    def is_today(start_dt: datetime, day_offset: int) -> bool:
        """Verifica se il giorno all'offset specificato  oggi."""
        target_day = (start_dt + timedelta(days=day_offset)).date()
        return target_day == datetime.now(UTC).astimezone().date()
