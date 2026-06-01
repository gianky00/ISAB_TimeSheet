"""Modulo Callbacks."""

from typing import TYPE_CHECKING, Any

from telegram import CallbackQuery, Update, constants
from telegram.ext import ContextTypes

from src.core import config_manager
from src.core.contabilita_manager import ContabilitaManager
from src.core.telegram.ui.keyboards import TelegramUI
from src.utils.printing import get_installed_printers

if TYPE_CHECKING:
    from src.core.telegram import TelegramService


async def handle_button(
    service: "TelegramService", update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Gestisce tutti i callback dei bottoni inline."""
    query = update.callback_query
    if not await _validate_button_query(service, update, query):
        return

    if not query or not query.data or not update.effective_chat:
        return

    chat_id = update.effective_chat.id
    data = query.data

    if data == "menu_main" or data.startswith("nav_"):
        await _handle_nav_actions(service, data, query)
    elif data.startswith("db_"):
        await _handle_db_actions(service, data, query, chat_id)
    elif _is_bot_data(data):
        await _handle_bot_actions(service, data, query, chat_id, update, context)
    elif _is_utility_data(data):
        await _handle_utility_actions(service, data, query, chat_id)


async def _validate_button_query(
    service: "TelegramService", update: Update, query: "CallbackQuery | None"
) -> bool:
    if not query or not query.message:
        return False

    if (
        service.connected_chat_id
        and update.effective_user
        and str(update.effective_user.id) != service.connected_chat_id
    ):
        return False

    await query.answer()
    return bool(query.data)


def _is_bot_data(data: str) -> bool:
    prefixes = ["menu_", "run_", "input_", "clear_", "list_", "confirm_"]
    return any(data.startswith(p) for p in prefixes) or data == "toggle_merge_all_pdl"


def _is_utility_data(data: str) -> bool:
    items = ["status", "screenshot", "snap_app", "snap_pc", "stop_all"]
    prefixes = ["app_", "set_", "toggle_"]
    return data in items or any(data.startswith(p) for p in prefixes)


async def _handle_nav_actions(service: "TelegramService", data: str, query: "CallbackQuery") -> None:
    if data == "menu_main":
        await query.edit_message_text(
            "📱 *Command Center*",
            reply_markup=TelegramUI.get_main_keyboard(),
            parse_mode=constants.ParseMode.MARKDOWN,
        )
    elif data == "nav_bots":
        await query.edit_message_text(
            "🤖 Seleziona Piattaforma:",
            reply_markup=TelegramUI.get_bots_menu(),
            parse_mode=constants.ParseMode.MARKDOWN,
        )
    elif data == "nav_db":
        await query.edit_message_text(
            "📊 Seleziona Database:",
            reply_markup=TelegramUI.get_db_menu(),
            parse_mode=constants.ParseMode.MARKDOWN,
        )
    elif data == "nav_lyra":
        await query.edit_message_text(
            "ℹ️ **Lyra AI Assistant**\n\nPuoi inviare vocali, foto di rapportini o domande sui dati.\n_Scrivi o parla direttamente qui!_",
            reply_markup=TelegramUI.get_lyra_menu(),
            parse_mode=constants.ParseMode.MARKDOWN,
        )
    elif data == "nav_utility":
        await query.edit_message_text(
            "    *Utility & Stato*",
            reply_markup=TelegramUI.get_utility_menu(),
            parse_mode=constants.ParseMode.MARKDOWN,
        )
    elif data == "nav_portale":
        await query.edit_message_text(
            "   *Portale Fornitori*",
            reply_markup=TelegramUI.get_portale_menu(),
            parse_mode=constants.ParseMode.MARKDOWN,
        )
    elif data == "nav_safework":
        await query.edit_message_text(
            "    *SafeWork*",
            reply_markup=TelegramUI.get_safework_menu(),
            parse_mode=constants.ParseMode.MARKDOWN,
        )


async def _handle_db_actions(
    service: "TelegramService", data: str, query: "CallbackQuery", chat_id: int
) -> None:
    if data == "db_select_year_strumentale":
        years = ContabilitaManager.get_available_years()
        if not years:
            await query.edit_message_text(
                "⚠️ Nessun anno disponibile nel database.",
                reply_markup=TelegramUI.get_db_menu(),
            )
            return
        await query.edit_message_text(
            "   *Seleziona Anno*",
            reply_markup=TelegramUI.get_db_year_selection(years),
            parse_mode=constants.ParseMode.MARKDOWN,
        )
    elif data.startswith("db_year_"):
        parts = data.replace("db_year_", "").split("_")
        db_name = parts[0]
        year = parts[1]
        service.user_states[chat_id] = f"WAITING_DB_QUERY_{db_name.upper()}_{year}"
        await query.edit_message_text(
            f"   **Strumentale {year}**\nCosa stai cercando? (es. nome fornitore, descrizione...)",
            reply_markup=TelegramUI.get_back_keyboard("db_select_year_strumentale"),
            parse_mode=constants.ParseMode.MARKDOWN,
        )
    elif data.startswith("db_info_"):
        db_name = data.replace("db_info_", "")
        service.user_states[chat_id] = f"WAITING_DB_QUERY_{db_name.upper()}"
        await query.edit_message_text(
            f"    **DB {db_name.capitalize()}**\nScrivi cosa cercare, Lyra risponder .",
            reply_markup=TelegramUI.get_back_keyboard("nav_db"),
            parse_mode=constants.ParseMode.MARKDOWN,
        )


async def _handle_bot_actions(  # noqa: PLR0913
    service: "TelegramService",
    data: str,
    query: "CallbackQuery",
    chat_id: int,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if await _handle_menu_and_input_dispatch(service, data, query, chat_id, update, context):
        return

    if data.startswith("sel_print_run_"):
        await _handle_printer_selection(service, data, query, chat_id)
    elif data.startswith("confirm_merge_"):
        await _handle_run_pdl_confirm(service, data, query, chat_id)
    else:
        _handle_direct_bot_commands(service, data, chat_id)


async def _handle_menu_and_input_dispatch(  # noqa: C901, PLR0913
    service: "TelegramService",
    data: str,
    query: "CallbackQuery",
    chat_id: int,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> bool:
    async def handle_menu_pdl() -> None:
        merge_all = service.pdl_settings.get(chat_id, {}).get("merge_all", False)
        await query.edit_message_text(
            "    *SafeWork PDL*",
            reply_markup=TelegramUI.get_pdl_menu(merge_all),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def handle_toggle_merge_all_pdl() -> None:
        if chat_id not in service.pdl_settings:
            service.pdl_settings[chat_id] = {}
        current = service.pdl_settings[chat_id].get("merge_all", False)
        service.pdl_settings[chat_id]["merge_all"] = not current
        query.data = "menu_pdl"
        await handle_button(service, update, context)

    async def handle_menu_ts() -> None:
        await query.edit_message_text(
            "   *Portale TS*",
            reply_markup=TelegramUI.get_ts_menu(),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def handle_menu_oda_details() -> None:
        await query.edit_message_text(
            "   *Dettagli OdA*",
            reply_markup=TelegramUI.get_oda_details_menu(),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def handle_menu_carico() -> None:
        await query.edit_message_text(
            "   *Carico TS*",
            reply_markup=TelegramUI.get_carico_menu(),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def handle_menu_timbrature() -> None:
        await query.edit_message_text(
            "    *Timbrature*",
            reply_markup=TelegramUI.get_timbrature_menu(),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def handle_menu_prenota_bp() -> None:
        await query.edit_message_text(
            "   *Prenota BP*",
            reply_markup=TelegramUI.get_prenota_bp_menu(),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def handle_input_pdl() -> None:
        service.user_states[chat_id] = "WAITING_PDL"
        await query.edit_message_text("[INPUT] Inserisci PDL:")

    async def handle_input_oda() -> None:
        service.user_states[chat_id] = "WAITING_ODA"
        await query.edit_message_text("[INPUT] Inserisci OdA:")

    async def handle_input_bp() -> None:
        service.user_states[chat_id] = "WAITING_BP"
        await query.edit_message_text(
            "[INPUT] Inserisci BP (Formato: NUMERO [NOTE]):\nEs: `123456 Urgente`\nEs: `987654`"
        )

    async def handle_run_pdl_on() -> None:
        printers = get_installed_printers()
        await query.edit_message_text(
            "Seleziona la stampante:",
            reply_markup=TelegramUI.get_printer_selection_menu(printers, "menu_pdl"),
        )

    async def handle_run_pdl_off() -> None:
        await query.edit_message_text(
            "Vuoi ricevere il PDF unito in chat?",
            reply_markup=TelegramUI.get_confirm_merge_menu(noprint=True),
        )

    map_handlers = {
        "menu_pdl": handle_menu_pdl,
        "toggle_merge_all_pdl": handle_toggle_merge_all_pdl,
        "menu_ts": handle_menu_ts,
        "menu_oda_details": handle_menu_oda_details,
        "menu_carico": handle_menu_carico,
        "menu_timbrature": handle_menu_timbrature,
        "menu_prenota_bp": handle_menu_prenota_bp,
        "input_pdl": handle_input_pdl,
        "input_oda": handle_input_oda,
        "input_bp": handle_input_bp,
        "run_pdl_on": handle_run_pdl_on,
        "run_pdl_off": handle_run_pdl_off,
    }

    if handler := map_handlers.get(data):
        await handler()
        return True
    return False


async def _handle_printer_selection(
    service: "TelegramService", data: str, query: "CallbackQuery", chat_id: int
) -> None:
    sn = data.replace("sel_print_run_", "")
    fpn = _get_full_printer_name(sn)
    service.user_states[chat_id] = {"printer": fpn}
    await query.edit_message_text(
        f"Stampante: `{fpn}`. Vuoi il PDF unito in chat?",
        reply_markup=TelegramUI.get_confirm_merge_menu(noprint=False),
        parse_mode=constants.ParseMode.MARKDOWN,
    )


async def _handle_run_pdl_confirm(
    service: "TelegramService", data: str, query: "CallbackQuery", chat_id: int
) -> None:
    state = service.user_states.pop(chat_id, {})
    p = state.get("printer", "") if isinstance(state, dict) else ""
    merge_all = service.pdl_settings.get(chat_id, {}).get("merge_all", False)

    params: dict[str, Any] = {"merge_all": merge_all}

    if "_print" in data and "_noprint" not in data:
        if not p:
            return
        service.command_received.emit("set_printer", {"printer": p})
        params.update({"print": True, "merge_and_send": ("_yes_" in data)})
        msg = f"✅ Avvio con stampa su `{p}`"
    else:
        params.update({"print": False, "merge_and_send": ("_yes_" in data)})
        msg = "✅ Avvio scarico"

    service.command_received.emit("run_pdl", params)
    await query.edit_message_text(f"{msg}, invio PDF={params['merge_and_send']}, merge finale={merge_all}.")


def _get_full_printer_name(short_name: str) -> str:
    for p in get_installed_printers():
        if p.startswith(short_name):
            return p
    return short_name


def _handle_direct_bot_commands(service: "TelegramService", data: str, chat_id: int) -> None:
    direct_map = {
        "run_ts": ("run_ts", {}),
        "run_timbrature_yesterday": ("run_timbrature", {"period": "yesterday"}),
        "run_timbrature_today": ("run_timbrature", {"period": "today"}),
        "run_oda_details": ("run_oda_details", {}),
        "run_carico": ("run_carico", {}),
        "run_prenota_bp": ("run_prenota_bp", {}),
        "list_pdl": ("list_pdl", {"chat_id": str(chat_id)}),
        "clear_pdl": ("clear_pdl", {}),
        "list_ts": ("list_ts", {"chat_id": str(chat_id)}),
        "clear_ts": ("clear_ts", {}),
    }
    if cmd := direct_map.get(data):
        service.command_received.emit(cmd[0], cmd[1])


async def _handle_utility_actions(  # noqa: C901
    service: "TelegramService", data: str, query: "CallbackQuery", chat_id: int
) -> None:
    if data == "status":
        service.status_requested.emit(str(chat_id))
    elif data == "screenshot":
        await query.edit_message_text("📸 Screenshot:", reply_markup=TelegramUI.get_screenshot_menu())
    elif data in ("snap_app", "snap_pc"):
        service.screenshot_requested.emit(data.replace("snap_", ""))
    elif data == "stop_all":
        service.command_received.emit("stop_all", {})
    elif data.startswith("app_"):
        if data == "app_restart":
            service.command_received.emit("restart_app", {})
        elif data == "app_conn_test":
            service.command_received.emit("test_connectivity", {})
    elif data == "menu_power":
        await query.edit_message_text("  Manutenzione:", reply_markup=TelegramUI.get_power_menu())
    elif data.startswith("menu_"):
        await _handle_utility_menus(service, data, query)
    elif data.startswith(("set_", "toggle_")):
        await _handle_setting_changes(service, data, query, chat_id)


async def _handle_utility_menus(service: "TelegramService", data: str, query: "CallbackQuery") -> None:
    if data == "menu_settings":
        config = config_manager.load_config()
        fornitori = config.get("fornitori", [])
        await query.edit_message_text(
            "    Impostazioni:", reply_markup=TelegramUI.get_settings_menu(fornitori)
        )
    elif data == "menu_autopilot":
        await query.edit_message_text("   Autopilot:", reply_markup=TelegramUI.get_autopilot_menu())
    elif data == "menu_printers":
        printers = get_installed_printers()
        await query.edit_message_text("    Stampanti:", reply_markup=TelegramUI.get_printers_menu(printers))


async def _handle_setting_changes(
    service: "TelegramService", data: str, query: "CallbackQuery", chat_id: int
) -> None:
    if data.startswith("set_forn_"):
        service.command_received.emit("set_fornitore", {"fornitore": data.replace("set_forn_", "")})
    elif data == "toggle_autopilot":
        enabled = not config_manager.load_config().get("timbrature_autopilot_enabled", False)
        service.command_received.emit("set_autopilot", {"enabled": enabled})
    elif data == "input_autopilot_time":
        service.user_states[chat_id] = "WAITING_AUTOPILOT_TIME"
        await query.edit_message_text("   Inserisci orario (HH:MM):")
    elif data.startswith("set_print_"):
        service.command_received.emit("set_printer", {"printer": data.replace("set_print_", "")})
