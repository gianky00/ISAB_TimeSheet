from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class TelegramUI:
    """Static factory for creating Telegram Inline Keyboards."""

    @staticmethod
    def get_main_keyboard():  # noqa: ANN205
        """Returns the main menu keyboard."""
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🤖 Bot", callback_data="nav_bots"),
                    InlineKeyboardButton("🗄️ Database", callback_data="nav_db"),
                ],
                [
                    InlineKeyboardButton("✨ Lyra AI", callback_data="nav_lyra"),
                    InlineKeyboardButton("⚙️ Utility & Stato", callback_data="nav_utility"),
                ],
            ]
        )

    @staticmethod
    def get_back_button(callback_data):  # noqa: ANN001, ANN205
        """Returns a generic back button with dynamic callback."""
        return InlineKeyboardButton("🔙 Indietro", callback_data=callback_data)

    @staticmethod
    def get_bots_menu():  # noqa: ANN205
        """Returns the Bots selection menu."""
        keyboard = [
            [InlineKeyboardButton("🏭 Portale Fornitori", callback_data="nav_portale")],
            [InlineKeyboardButton("🛡️ SafeWork", callback_data="nav_safework")],
            [TelegramUI.get_back_button("menu_main")],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_db_menu():  # noqa: ANN205
        """Returns the Database selection menu."""
        keyboard = [
            [InlineKeyboardButton("⏱️ Timbrature Isab", callback_data="db_info_timbrature")],
            [InlineKeyboardButton("📊 Strumentale", callback_data="db_select_year_strumentale")],
            [InlineKeyboardButton("🏗️ DataEase", callback_data="db_info_dataease")],
            [TelegramUI.get_back_button("menu_main")],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_utility_menu():  # noqa: ANN205
        """Returns the Utilities menu (Status, Screenshot, Settings)."""
        keyboard = [
            [
                InlineKeyboardButton("📊 Stato", callback_data="status"),
                InlineKeyboardButton("📸 Screenshot", callback_data="screenshot"),
            ],
            [
                InlineKeyboardButton("⚙️ Impostazioni", callback_data="menu_settings"),
                InlineKeyboardButton("🛑 Stop Globale", callback_data="stop_all"),
            ],
            [InlineKeyboardButton("⚡ Manutenzione", callback_data="menu_power")],
            [TelegramUI.get_back_button("menu_main")],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_portale_menu():  # noqa: ANN205
        """Returns the Portale Fornitori specific bot menu."""
        keyboard = [
            [InlineKeyboardButton("📥 Scarico TS", callback_data="menu_ts")],
            [InlineKeyboardButton("📤 Carico TS", callback_data="menu_carico")],
            [InlineKeyboardButton("📋 Dettagli OdA", callback_data="menu_oda_details")],
            [InlineKeyboardButton("⏱️ Timbrature", callback_data="menu_timbrature")],
            [InlineKeyboardButton("📦 Prenota BP", callback_data="menu_prenota_bp")],
            [TelegramUI.get_back_button("nav_bots")],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_safework_menu():  # noqa: ANN205
        """Returns the SafeWork specific bot menu."""
        keyboard = [
            [InlineKeyboardButton("🛡️ Scarico PDL", callback_data="menu_pdl")],
            [TelegramUI.get_back_button("nav_bots")],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_lyra_menu():  # noqa: ANN205
        """Returns the Lyra AI menu."""
        return InlineKeyboardMarkup([[TelegramUI.get_back_button("menu_main")]])

    @staticmethod
    def get_db_year_selection(years):  # noqa: ANN001, ANN205
        """Returns a keyboard for selecting a year for DB queries."""
        keyboard = []
        row = []
        for y in sorted(years, reverse=True):
            row.append(InlineKeyboardButton(str(y), callback_data=f"db_year_strumentale_{y}"))
            if len(row) == 3:  # noqa: PLR2004
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        keyboard.append([TelegramUI.get_back_button("nav_db")])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_pdl_menu(merge_all):  # noqa: ANN001, ANN205
        """Returns the PDL management menu with dynamic merge state."""
        merge_icon = "✅" if merge_all else "❌"
        keyboard = [
            [InlineKeyboardButton("➕ Inserisci", callback_data="input_pdl")],
            [
                InlineKeyboardButton("📋 Lista", callback_data="list_pdl"),
                InlineKeyboardButton("🗑️ Svuota", callback_data="clear_pdl"),
            ],
            [
                InlineKeyboardButton(
                    f"🔗 Unisci Tutto: {merge_icon}",
                    callback_data="toggle_merge_all_pdl",
                )
            ],
            [InlineKeyboardButton("🖨️ Avvia (Print ON)", callback_data="run_pdl_on")],
            [InlineKeyboardButton("📄 Avvia (Print OFF)", callback_data="run_pdl_off")],
            [TelegramUI.get_back_button("nav_safework")],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_ts_menu():  # noqa: ANN205
        """Returns the Timesheet (TS) management menu."""
        keyboard = [
            [InlineKeyboardButton("➕ OdA", callback_data="input_oda")],
            [
                InlineKeyboardButton("📋 Lista", callback_data="list_ts"),
                InlineKeyboardButton("🗑️ Svuota", callback_data="clear_ts"),
            ],
            [InlineKeyboardButton("▶ Avvia", callback_data="run_ts")],
            [TelegramUI.get_back_button("nav_portale")],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_oda_details_menu():  # noqa: ANN205
        """Returns the OdA Details bot menu."""
        keyboard = [
            [InlineKeyboardButton("➕ OdA", callback_data="input_oda")],
            [
                InlineKeyboardButton("📋 Lista", callback_data="list_ts"),
                InlineKeyboardButton("🗑️ Svuota", callback_data="clear_ts"),
            ],
            [InlineKeyboardButton("▶ Avvia Dettagli", callback_data="run_oda_details")],
            [TelegramUI.get_back_button("nav_portale")],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_carico_menu():  # noqa: ANN205
        """Returns the Time Upload (Carico TS) menu."""
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("▶ Avvia Carico", callback_data="run_carico")],
                [TelegramUI.get_back_button("nav_portale")],
            ]
        )

    @staticmethod
    def get_timbrature_menu():  # noqa: ANN205
        """Returns the Attendance (Timbrature) menu."""
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🕒 Ieri", callback_data="run_timbrature_yesterday")],
                [InlineKeyboardButton("📅 Oggi", callback_data="run_timbrature_today")],
                [TelegramUI.get_back_button("nav_portale")],
            ]
        )

    @staticmethod
    def get_prenota_bp_menu():  # noqa: ANN205
        """Returns the Buoni Pasto (BP) booking menu."""
        keyboard = [
            [InlineKeyboardButton("➕ Inserisci BP", callback_data="input_bp")],
            [InlineKeyboardButton("▶ Avvia", callback_data="run_prenota_bp")],
            [TelegramUI.get_back_button("nav_portale")],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_printer_selection_menu(printers, back_callback):  # noqa: ANN001, ANN205
        """Returns a keyboard for selecting a printer."""
        keyboard = [
            [InlineKeyboardButton(f"🖨️ {p[:30]}", callback_data=f"sel_print_run_{p[:25]}")]
            for p in printers[:6]
        ]
        keyboard.append([TelegramUI.get_back_button(back_callback)])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_confirm_merge_menu(noprint=False):  # noqa: ANN001, ANN205
        """Returns a confirmation dialog for merging files."""
        suffix = "_noprint" if noprint else "_print"
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("✅ Sì, invia", callback_data=f"confirm_merge_yes{suffix}")],
                [InlineKeyboardButton("❌ No", callback_data=f"confirm_merge_no{suffix}")],
                [TelegramUI.get_back_button("menu_pdl")],
            ]
        )

    @staticmethod
    def get_screenshot_menu():  # noqa: ANN205
        """Returns the screenshot type selection menu."""
        keyboard = [
            [
                InlineKeyboardButton("🖼️ App", callback_data="snap_app"),
                InlineKeyboardButton("🖥️ PC", callback_data="snap_pc"),
            ],
            [TelegramUI.get_back_button("nav_utility")],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_power_menu():  # noqa: ANN205
        """Returns the system maintenance/power menu."""
        keyboard = [
            [InlineKeyboardButton("🔄 Riavvia App", callback_data="app_restart")],
            [InlineKeyboardButton("🔌 Test Net", callback_data="app_conn_test")],
            [TelegramUI.get_back_button("nav_utility")],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_settings_menu(fornitori):  # noqa: ANN001, ANN205
        """Returns the settings menu, including provider selection."""
        keyboard = [[InlineKeyboardButton(f"🏢 {f}", callback_data=f"set_forn_{f}")] for f in fornitori[:6]]
        keyboard.extend(
            [
                [InlineKeyboardButton("📅 Autopilot", callback_data="menu_autopilot")],
                [InlineKeyboardButton("🖨️ Stampante", callback_data="menu_printers")],
                [TelegramUI.get_back_button("nav_utility")],
            ]
        )
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_autopilot_menu():  # noqa: ANN205
        """Returns the Autopilot configuration menu."""
        keyboard = [
            [InlineKeyboardButton("🔄 Toggle", callback_data="toggle_autopilot")],
            [InlineKeyboardButton("🕒 Orario", callback_data="input_autopilot_time")],
            [TelegramUI.get_back_button("menu_settings")],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_printers_menu(printers):  # noqa: ANN001, ANN205
        """Returns list of printers for configuration."""
        keyboard = [
            [InlineKeyboardButton(f"🖨️ {p[:30]}", callback_data=f"set_print_{p[:30]}")] for p in printers[:6]
        ]
        keyboard.append([TelegramUI.get_back_button("menu_settings")])
        return InlineKeyboardMarkup(keyboard)
