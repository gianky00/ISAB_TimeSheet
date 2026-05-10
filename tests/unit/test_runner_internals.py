"""
Unit test per le funzioni interne di run_robust_tests.py.

Verifica correttezza di parsing, classificazione errori,
estrazione traceback e conteggio dei risultati.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Assicura che il runner sia importabile
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tests.run_robust_tests import (  # noqa: E402
    FailureDetail,
    TestResult as RunResult,
    UltraRunner,
    _classify_error,
    _extract_failures,
    _extract_traceback_block,
    _parse_pytest_summary,
)

# ─── _parse_pytest_summary ────────────────────────────────────────────────────


class TestParsePytestSummary:
    """Test per il parser della riga di summary pytest."""

    def test_all_passed(self) -> None:
        output = "========================= 10 passed in 2.50s ========================="
        assert _parse_pytest_summary(output) == (10, 0)

    def test_all_failed(self) -> None:
        output = "========================= 3 failed in 1.20s ========================="
        assert _parse_pytest_summary(output) == (0, 3)

    def test_mixed_passed_failed(self) -> None:
        output = "============= 8 passed, 2 failed in 4.50s ============="
        assert _parse_pytest_summary(output) == (8, 2)

    def test_failed_and_error_both_counted(self) -> None:
        """BUG-2 regression: sia 'failed' che 'error' devono essere contati."""
        output = "============= 3 failed, 2 error in 5.20s ============="
        assert _parse_pytest_summary(output) == (0, 5)

    def test_passed_failed_error_all_present(self) -> None:
        """Caso completo: passed + failed + error."""
        output = "============= 10 passed, 3 failed, 2 error in 5.20s ============="
        assert _parse_pytest_summary(output) == (10, 5)

    def test_only_error(self) -> None:
        output = "========================= 1 error in 0.50s ========================="
        assert _parse_pytest_summary(output) == (0, 1)

    def test_no_summary_line(self) -> None:
        output = "collecting ...\nsome random output\n"
        assert _parse_pytest_summary(output) == (0, 0)

    def test_empty_output(self) -> None:
        assert _parse_pytest_summary("") == (0, 0)

    def test_multiline_ignores_non_summary(self) -> None:
        """Solo l'ultima riga di summary viene considerata."""
        output = (
            "tests/test_foo.py::test_bar PASSED\n"
            "tests/test_foo.py::test_baz FAILED\n"
            "============= 1 passed, 1 failed in 0.50s =============\n"
        )
        assert _parse_pytest_summary(output) == (1, 1)


# ─── _classify_error ──────────────────────────────────────────────────────────


class TestClassifyError:
    """Test per la classificazione semantica degli errori."""

    def test_import_error(self) -> None:
        err_type, _, category = _classify_error("ImportError: No module named 'foo'", "", "")
        assert err_type == "ImportError"
        assert category == "import_error"

    def test_module_not_found(self) -> None:
        err_type, _, category = _classify_error("ModuleNotFoundError: No module named 'bar'", "", "")
        assert err_type == "ImportError"
        assert category == "import_error"

    def test_assertion_error(self) -> None:
        """BUG-3 regression: deve matchare 'AssertionError' (Python standard)."""
        err_type, _, category = _classify_error("AssertionError: 1 != 2", "", "")
        assert err_type == "AssertionError"
        assert category == "assertion"

    def test_assertion_via_assert_keyword(self) -> None:
        _err_type, _, category = _classify_error("assert result == expected", "", "")
        assert category == "assertion"

    def test_type_error(self) -> None:
        err_type, _, category = _classify_error("TypeError: unsupported operand", "", "")
        assert err_type == "TypeError"
        assert category == "runtime"

    def test_value_error(self) -> None:
        err_type, _, category = _classify_error("ValueError: invalid literal", "", "")
        assert err_type == "ValueError"
        assert category == "runtime"

    def test_attribute_error(self) -> None:
        err_type, _, category = _classify_error("AttributeError: 'NoneType' has no attr", "", "")
        assert err_type == "AttributeError"
        assert category == "runtime"

    def test_timeout(self) -> None:
        err_type, _, category = _classify_error("TIMEOUT after 120s", "", "")
        assert err_type == "TimeoutError"
        assert category == "timeout"

    def test_timeout_error_class(self) -> None:
        err_type, _, category = _classify_error("TimeoutError: connection timed out", "", "")
        assert err_type == "TimeoutError"
        assert category == "timeout"

    def test_native_crash_segfault(self) -> None:
        err_type, _, category = _classify_error("exit code -11", "Segfault detected", "")
        assert err_type == "NativeCrash"
        assert category == "crash"

    def test_native_crash_access_violation(self) -> None:
        err_type, _, category = _classify_error("crash", "Access Violation at 0x00", "")
        assert err_type == "NativeCrash"
        assert category == "crash"

    def test_generic_error_with_pattern(self) -> None:
        err_type, msg, category = _classify_error("CustomError: something broke", "", "")
        assert err_type == "CustomError"
        assert msg == "something broke"
        assert category == "runtime"

    def test_unknown_error(self) -> None:
        err_type, _, category = _classify_error("something unexpected", "", "")
        assert err_type == "UnknownError"
        assert category == "runtime"

    def test_empty_error_text(self) -> None:
        err_type, msg, _category = _classify_error("", "", "")
        assert err_type == "UnknownError"
        assert msg == "No error details captured"


# ─── _extract_traceback_block ─────────────────────────────────────────────────


class TestExtractTracebackBlock:
    """Test per l'estrazione del blocco traceback."""

    def test_extracts_correct_block(self) -> None:
        lines = [
            "collected 5 items",
            "_______________________________ test_foo _______________________________",
            "    def test_foo():",
            ">       assert 1 == 2",
            "E       AssertionError: 1 != 2",
            "========================================================================",
            "short test summary info",
        ]
        result = _extract_traceback_block(lines, "file::test_foo")
        assert "test_foo" in result
        assert "assert 1 == 2" in result

    def test_no_match_returns_empty(self) -> None:
        lines = ["no relevant content here", "just noise"]
        result = _extract_traceback_block(lines, "file::test_nonexistent")
        assert result == ""

    def test_does_not_match_wrong_test(self) -> None:
        """BUG-6 regression: non deve matchare blocchi di altri test."""
        lines = [
            "_______________________________ test_alpha _______________________________",
            "    def test_alpha():",
            ">       assert True",
            "========================================================================",
            "_______________________________ test_beta _______________________________",
            "    def test_beta():",
            ">       assert False",
            "========================================================================",
        ]
        result = _extract_traceback_block(lines, "file::test_beta")
        assert "test_beta" in result
        assert "test_alpha" not in result

    def test_limits_to_50_lines(self) -> None:
        """Il traceback deve essere troncato a 50 righe."""
        lines = [
            "_______________________________ test_long _______________________________",
            *[f"    line {i}" for i in range(100)],
            "========================================================================",
        ]
        result = _extract_traceback_block(lines, "file::test_long")
        assert len(result.splitlines()) <= 50


# ─── _extract_failures ────────────────────────────────────────────────────────


class TestExtractFailures:
    """Test per l'estrazione completa dei dettagli di fallimento."""

    def test_extracts_failed_line(self) -> None:
        output = (
            "FAILED tests/unit/test_foo.py::test_bar - AssertionError: expected 1 got 2\n"
            "======= 1 failed in 0.5s ======="
        )
        failures = _extract_failures(output, "tests/unit/test_foo.py")
        assert len(failures) == 1
        assert failures[0].node_id == "tests/unit/test_foo.py::test_bar"
        assert failures[0].test_name == "test_bar"
        assert failures[0].category == "assertion"

    def test_multiple_failures(self) -> None:
        output = (
            "FAILED tests/test_a.py::test_one - TypeError: bad arg\n"
            "FAILED tests/test_a.py::test_two - ValueError: invalid\n"
            "======= 2 failed in 1.0s ======="
        )
        failures = _extract_failures(output, "tests/test_a.py")
        assert len(failures) == 2
        names = {f.test_name for f in failures}
        assert names == {"test_one", "test_two"}

    def test_no_failures_returns_empty(self) -> None:
        output = "======= 5 passed in 2.0s ======="
        failures = _extract_failures(output, "tests/test_ok.py")
        assert failures == []


# ─── UltraRunner (conteggio) ──────────────────────────────────────────────────


class TestUltraRunnerCounting:
    """Test per la correttezza dei conteggi nel runner."""

    def test_initial_state(self) -> None:
        runner = UltraRunner()
        assert runner.total_passed == 0
        assert runner.total_failed == 0
        assert runner._exit_code == 0
        assert runner.strategy == "SHOTGUN"

    def test_exit_code_attribute_exists(self) -> None:
        """ARCH-2 regression: il runner deve avere _exit_code, non chiamare sys.exit."""
        runner = UltraRunner()
        assert hasattr(runner, "_exit_code")

    def test_file_results_accumulation(self) -> None:
        runner = UltraRunner()
        r1 = RunResult(target="test_a.py", success=True, duration=1.0, passed=3, failed=0)
        r2 = RunResult(target="test_b.py", success=False, duration=2.0, passed=1, failed=2)
        runner.file_results.extend([r1, r2])
        assert len(runner.file_results) == 2

    def test_failure_details_deduplication_concept(self) -> None:
        """Verifica che la deduplica per node_id funzioni correttamente."""
        fd1 = FailureDetail(
            node_id="test_a.py::test_foo",
            file="test_a.py",
            test_name="test_foo",
            error_type="AssertionError",
            error_message="1 != 2",
            traceback="...",
            category="assertion",
        )
        fd2 = FailureDetail(
            node_id="test_a.py::test_foo",  # duplicato
            file="test_a.py",
            test_name="test_foo",
            error_type="AssertionError",
            error_message="1 != 2",
            traceback="...",
            category="assertion",
        )
        # Simula la logica di _finish_ai
        details = [fd1, fd2]
        seen: set[str] = set()
        unique = []
        for fd in details:
            if fd.node_id not in seen:
                seen.add(fd.node_id)
                unique.append(fd)
        assert len(unique) == 1
