from unittest.mock import patch

from src.core.logging.sampling import ContextAwareSampler, get_sampler, should_log


class TestSampling:
    def test_validate_rate(self):
        sampler = ContextAwareSampler()
        assert sampler._validate_rate(1.5) == 1.0
        assert sampler._validate_rate(-0.5) == 0.0
        assert sampler._validate_rate(0.5) == 0.5

    def test_should_log_levels(self):
        sampler = ContextAwareSampler(default_rate=0.0, error_rate=1.0)

        # ERROR sempre sì (rate 1.0)
        assert sampler.should_log("ERROR") is True

        # INFO sempre no (rate 0.0)
        assert sampler.should_log("INFO") is False

    def test_should_log_slow_op(self):
        sampler = ContextAwareSampler(default_rate=0.0)
        extra = {"duration_ms": 5000, "threshold_ms": 100}
        assert sampler.should_log("INFO", extra=extra) is True

    def test_should_log_trace_id(self):
        sampler = ContextAwareSampler(default_rate=0.0)
        sampler.add_trace_to_always_log("T1")

        assert sampler.should_log("INFO", context={"trace_id": "T1"}) is True
        assert sampler.should_log("INFO", context={"trace_id": "T2"}) is False

    def test_should_log_operation_rate(self):
        sampler = ContextAwareSampler(default_rate=0.0)
        sampler.set_operation_rate("my_func", 1.0)

        assert sampler.should_log("INFO", context={"function": "my_func"}) is True
        assert sampler.should_log("INFO", context={"function": "other"}) is False

    def test_deterministic_sampling(self):
        # Rate 0.5 -> 1 ogni 2
        sampler = ContextAwareSampler(default_rate=0.5)

        # Primo tentativo: 1 % 2 = 1 -> False?
        # Vediamo logica: counter += 1 (1), threshold = 1.0/0.5 = 2.
        # 1 % 2 != 0 -> False.
        # Secondo tentativo: 2 % 2 == 0 -> True.

        res = [sampler.should_log("INFO") for _ in range(4)]
        assert res == [False, True, False, True]

    def test_get_stats(self):
        sampler = ContextAwareSampler(default_rate=0.5)
        sampler.should_log("INFO")
        stats = sampler.get_stats()
        assert stats["default_rate"] == 0.5
        assert stats["counters"]["default"] == 1

    def test_singleton_get_sampler(self):
        s1 = get_sampler()
        s2 = get_sampler()
        assert s1 is s2

    def test_should_log_helper(self):
        # should_log usa il singleton. Per il test lo resettiamo o patchiamo
        with patch("src.core.logging.sampling.get_sampler") as mock_get:
            mock_get.return_value.should_log.return_value = True
            assert should_log("INFO") is True
            mock_get.return_value.should_log.assert_called_with("INFO", None, None)
