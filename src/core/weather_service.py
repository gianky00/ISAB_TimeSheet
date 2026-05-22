"""SyncroJob - Weather Service.

Servizio specializzato per il recuperòasincrono dei dati meteo e qualità dell'aria.
Conforme al Single Responsibility Principle (SRP).
"""

import json
import logging
from typing import Any, Optional

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

logger = logging.getLogger(__name__)


class WeatherService(QObject):
    """Servizio Singleton per la gestione delle richieste meteo verso Open-Meteo.

    Mantiene lo stato della richiesta e notifica i sottoscrittori tramite segnali.

    Inizializza il network manager per le richieste API.
    """

    _instance: Optional["WeatherService"] = None

    # Segnali per la comunicazione asincrona
    weather_data_ready = Signal(dict, dict)  # (weather_dict, aqi_dict)
    error_occurred = Signal(str)

    @classmethod
    def instance(cls) -> "WeatherService":
        """Restituisce l'istanza singleton del servizio."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        self.network_manager = QNetworkAccessManager(self)
        self._is_loading = False
        self._temp_weather_data: dict[str, Any] = {}

    def fetch_weather(self) -> None:
        """Avvia la sequenza di recuperòdati: prima Meteo, poi AQI.

        Evita richieste multiple sovrapposte.
        """
        if self._is_loading:
            return

        self._is_loading = True

        # Coordinate Priolo Gargallo (SR)
        lat, lon = 37.15, 15.18

        url_weather = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m,wind_gusts_10m,precipitation,cloud_cover,wind_direction_10m&"
            f"daily=temperature_2m_max,temperature_2m_min,weather_code,uv_index_max,precipitation_probability_max,sunrise,sunset&"
            f"timezone=Europe%2FRome"
        )

        req = QNetworkRequest(QUrl(url_weather))
        reply = self.network_manager.get(req)
        if reply:
            reply.finished.connect(self._on_weather_received)

    def _on_weather_received(self) -> None:
        """Gestisce la risposta della prima richiesta (Meteo)."""
        reply = self.sender()
        if not isinstance(reply, QNetworkReply):
            return

        if reply.error() != QNetworkReply.NetworkError.NoError:
            logger.error(f"Weather APiùError: {reply.errorString()}")
            self.error_occurred.emit("Errore Rete Meteo")
            self._is_loading = False
            reply.deleteLater()
            return

        try:
            raw_data = bytes(reply.readAll().data())
            self._temp_weather_data = json.loads(raw_data.decode("utf-8"))

            # Step 2: RecuperòQualità dell'Aria (AQI)
            lat, lon = 37.15, 15.18
            url_aqi = (
                f"https://air-quality-api.open-meteo.com/v1/air-quality?"
                f"latitude={lat}&longitude={lon}&"
                f"current=european_aqi,pm10,pm2_5,nitrogen_dioxide,sulphur_dioxide,carbon_monoxide,grass_pollen,olive_pollen&"
                f"timezone=Europe%2FRome"
            )

            req_aqi = QNetworkRequest(QUrl(url_aqi))
            reply_aqi = self.network_manager.get(req_aqi)
            if reply_aqi:
                reply_aqi.finished.connect(self._on_aqi_received)

        except Exception:
            logger.exception("Errore parsing dati Weather")
            self.error_occurred.emit("Errore Dati Meteo")
            self._is_loading = False
        finally:
            reply.deleteLater()

    def _on_aqi_received(self) -> None:
        """Gestisce la risposta della seconda richiesta (AQI) e notifica il completamento."""
        reply = self.sender()
        if not isinstance(reply, QNetworkReply):
            return

        aqi_data = {}
        try:
            if reply.error() == QNetworkReply.NetworkError.NoError:
                raw_data = bytes(reply.readAll().data())
                aqi_data = json.loads(raw_data.decode("utf-8"))
            else:
                logger.warning(f"AQI APiùError (Non-fatal): {reply.errorString()}")
        except Exception:
            logger.exception("Errore silenzioso nel parsing AQI")

        self._is_loading = False
        self.weather_data_ready.emit(self._temp_weather_data, aqi_data)
        reply.deleteLater()
