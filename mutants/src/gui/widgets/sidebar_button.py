from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QPushButton

from src.utils.helpers import get_colored_icon


class SidebarButton(QPushButton):
    """Pulsante personalizzato per la sidebar con supporto modalità compatta e icone SVG."""

    def __init__(self, text: str, icon_path: str = "", parent=None):
        super().__init__(parent)
        self.label_text = text
        self.icon_path = icon_path
        self._collapsed = False

        if icon_path:
            self.setIcon(get_colored_icon(icon_path, "#ffffff"))

        self.setCheckable(True)
        self.setMinimumHeight(48)

        self._refresh_state()
        self._update_style()
        self.toggled.connect(self._update_style)

    def set_collapsed(self, collapsed: bool):
        """Attiva o disattiva la modalità solo icona."""
        self._collapsed = collapsed
        self._refresh_state()
        self._update_style()

    def _refresh_state(self):
        """Aggiorna testo e dimensione icona in base allo stato."""
        if self._collapsed:
            self.setText("")
            self.setIconSize(QSize(22, 22))
            self.setToolTip(self.label_text)
        else:
            self.setText(f"   {self.label_text}")  # Spazio extra per separare da icona
            self.setIconSize(QSize(18, 18))
            self.setToolTip("")

    def set_badge(self, count: int):
        """Imposta un badge di notifica."""
        # TODO: Implementare un badge grafico (pallino rosso) sovrapposto all'icona
        if not self._collapsed:
            base = f"   {self.label_text}"
            if count > 0:
                self.setText(f"{base} ({count})")
            else:
                self.setText(base)

    def _update_style(self):
        """Aggiorna lo stile in base allo stato."""
        align = "center" if self._collapsed else "left"
        # Padding ottimizzato per centrare l'icona quando collassato
        padding = "0px" if self._collapsed else "12px 15px"

        base_style = f"""
            QPushButton {{
                color: rgba(255, 255, 255, 0.85);
                border-radius: 10px;
                padding: {padding};
                text-align: {align};
                font-size: 14px;
                font-weight: 500;
                margin: 2px 5px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
            }}
        """

        if self.isChecked():
            self.setStyleSheet(
                base_style
                + """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.2);
                    border-left: 3px solid #ffffff;
                    border-radius: 0px 10px 10px 0px;
                    color: #ffffff;
                    font-weight: bold;
                }
            """
            )
        else:
            self.setStyleSheet(
                base_style
                + """
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
            """
            )
