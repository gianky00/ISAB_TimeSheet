"""Modulo Messages."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from src.core.telegram.ui.keyboards import TelegramUI

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import ContextTypes

    from src.core.telegram.service import TelegramService


async def handle_text_input(
    service: TelegramService, update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Main router for incoming text messages.

    Routes based on current user state (DB query, wizard) or passes to query dispatcher.
    """
    if (
        not await service._check_auth(update)
        or not update.effective_chat
        or not update.message
        or not update.message.text
    ):
        return

    chat_id = update.effective_chat.id
    state = service.user_states.get(chat_id)
    text = update.message.text

    # 1. Gestione Ricerca DB
    if isinstance(state, str) and state.startswith("WAITING_DB_QUERY_"):
        await _handle_db_query_input(service, chat_id, state, text, update)
        return

    # 2. Gestione Query (senza stato)
    if not state:
        service.query_received.emit(str(chat_id), text)
        return

    # 3. Gestione Input Sequenziali (OdA, PDL, Time)
    await _handle_sequential_input(service, chat_id, state, text, update)


async def _handle_db_query_input(
    service: TelegramService, chat_id: int, state: str, text: str, update: Update
) -> None:
    """Processes search queries for the database browser."""
    parts = state.replace("WAITING_DB_QUERY_", "").split("_")
    params = {"db": parts[0].lower(), "query": text, "chat_id": str(chat_id)}
    if len(parts) > 1:
        params["year"] = parts[1]

    if update.message:
        await update.message.reply_chat_action("typing")
    service.command_received.emit("search_db_pdf", params)
    service.user_states[chat_id] = None


async def _handle_sequential_input(
    service: TelegramService, chat_id: int, state: str, text: str, update: Update
) -> None:
    """Handles multi-line or list inputs for specific wizards (PDL, OdA, Time)."""
    items = [i.strip() for i in text.replace(",", "\n").replace(";", "\n").split("\n") if i.strip()]
    if not items:
        return

    if state == "WAITING_PDL":
        service.data_received.emit("pdl", items)
    elif state == "WAITING_ODA":
        service.data_received.emit("oda", items)
    elif state == "WAITING_BP":
        service.data_received.emit("bp", items)
    elif state == "WAITING_AUTOPILOT_TIME":
        if re.match(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$", items[0]):
            service.command_received.emit("set_autopilot", {"time": items[0]})
        else:
            if update.message:
                await update.message.reply_text("❌ Formato non valido. Usa HH:MM.")
            return

    service.user_states[chat_id] = None
    if update.message:
        await update.message.reply_text(
            "✅ Operazione completata.", reply_markup=TelegramUI.get_main_keyboard()
        )


async def handle_voice(service: TelegramService, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles voice messages. (AI functionality removed)."""
    if update.message:
        await update.message.reply_text("   Messaggiàvocali non supportati in questa versione.")


async def handle_photo(service: TelegramService, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles photo messages.

    Downloads the high-res photo and emits a 'photo_received' signal.
    """
    if not await service._check_auth(update):
        return
    if not update.effective_chat or not update.message or not update.message.photo:
        return

    chat_id = str(update.effective_chat.id)
    photo = update.message.photo[-1]
    caption = update.message.caption or ""
    file = await context.bot.get_file(photo.file_id)
    photo_bytes = await file.download_as_bytearray()
    service.photo_received.emit(chat_id, bytes(photo_bytes), caption)
