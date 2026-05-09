# mypy: disable-error-code="no-any-unimported, unused-ignore"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from telegram import Update, constants

from src.core import config_manager
from src.core.telegram.ui.keyboards import TelegramUI

if TYPE_CHECKING:
    from telegram.ext import ContextTypes

    from src.core.telegram.service import TelegramService


async def cmd_start(service: TelegramService, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /start command.
    Checks authentication status and displays the main menu or pairing prompt.
    """
    if not update.effective_chat:
        return

    chat_id = str(update.effective_chat.id)
    config = config_manager.load_config()
    saved_chat_id = config.get("telegram_chat_id", "")

    # 1. Verifica associazione esistente
    if saved_chat_id:
        if chat_id != saved_chat_id:
            if update.message:
                await update.message.reply_text("[BLOCCO] Questo bot  già associato a un altro dispositivo.")
            return
    # 2. Gestione nuovo accoppiamento
    elif not await _handle_initial_pairing(service, update, context, config, chat_id):
        return

    # 3. Menu principale
    if update.message:
        await update.message.reply_text(
            "[AVVIO] *SyncroJob Command Center*",
            reply_markup=TelegramUI.get_main_keyboard(),
            parse_mode=constants.ParseMode.MARKDOWN,
        )


async def _handle_initial_pairing(
    service: TelegramService,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    config: dict[str, Any],
    chat_id: str,
) -> bool:
    """
    Manages the initial device pairing process using an OTP code.
    Returns True if pairing is successful, False otherwise.
    """
    args = context.args
    pairing_code = config.get("telegram_pairing_code", "")

    if not pairing_code:
        if update.message:
            await update.message.reply_text("⚠️ Errore: Codice non trovato nell'app desktop.")
        return False

    if args and args[0] == pairing_code:
        service.connected_chat_id = chat_id
        config_manager.set_config_value("telegram_chat_id", chat_id)
        config_manager.set_config_value("telegram_pairing_code", "")
        if update.message:
            await update.message.reply_text(f"✅ Dispositivo associato!\nChat ID: {chat_id}")
        return True

    if update.message:
        await update.message.reply_text(
            "   *SyncroJob Security*\n\nInserisci il codice dell'app desktop.\nEsempio: `/start 123456`",
            parse_mode=constants.ParseMode.MARKDOWN,
        )
    return False


async def cmd_status(service: TelegramService, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /status command.
    Triggers a status report request to the desktop application to be sent back via callback.
    """
    if not await service._check_auth(update):
        return
    if update.effective_chat:
        service.status_requested.emit(str(update.effective_chat.id))


async def cmd_stop(service: TelegramService, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /stop command.
    Sends a 'stop_all' signal to the desktop application to halt all running operations.
    """
    if not await service._check_auth(update):
        return
    service.command_received.emit("stop_all", {})
    if update.message:
        await update.message.reply_text("   *Richiesta Stop Inviata*")
