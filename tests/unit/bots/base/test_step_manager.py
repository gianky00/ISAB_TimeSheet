from unittest.mock import MagicMock

from src.bots.base.step_manager import BotStepManager, StepStatus


class TestBotStepManager:
    def test_initialization(self):
        steps = [("login", "Accesso"), ("download", "Scaricamento")]
        manager = BotStepManager(steps)
        assert manager.steps == steps
        assert manager.current_index == -1
        assert manager.current_step_name == ""

    def test_update_step_by_index(self):
        steps = [("s1", "Step 1"), ("s2", "Step 2")]
        manager = BotStepManager(steps)
        mock_signal = MagicMock()
        manager.step_changed.connect(mock_signal.emit)

        idx, name = manager.update_step(0, StepStatus.RUNNING)
        assert idx == 0
        assert name == "Step 1"
        assert manager.current_index == 0
        assert mock_signal.emit.called
        mock_signal.emit.assert_called_with(0, "Step 1", StepStatus.RUNNING)

    def test_update_step_by_id(self):
        steps = [("login", "Accesso"), ("run", "Esecuzione")]
        manager = BotStepManager(steps)

        idx, name = manager.update_step("run", StepStatus.COMPLETED)
        assert idx == 1
        assert name == "Esecuzione"
        assert manager.current_index == 1

    def test_update_step_invalid(self):
        steps = [("s1", "S1")]
        manager = BotStepManager(steps)

        idx, name = manager.update_step("invalid", StepStatus.RUNNING)
        assert idx == -1
        assert name == ""

        idx, name = manager.update_step(5, StepStatus.RUNNING)
        assert idx == -1

    def test_reset(self):
        steps = [("s1", "S1")]
        manager = BotStepManager(steps)
        manager.update_step(0, StepStatus.COMPLETED)

        manager.reset()
        assert manager.current_index == -1
        assert manager._states[0] == StepStatus.PENDING

    def test_current_step_name(self):
        steps = [("s1", "Nome 1")]
        manager = BotStepManager(steps)
        assert manager.current_step_name == ""

        manager.update_step(0, StepStatus.RUNNING)
        assert manager.current_step_name == "Nome 1"
