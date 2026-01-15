# 📈 Test Coverage Improvement Plan (Next Phase)

## 1. Analysis of Current State
- **Current Status:** Tests are present (1050+ items), but execution is hindered by environment issues (missing `markdown` dependency) and failing tests (`test_ai_sentinel_hardened.py`).
- **Estimated Coverage:** ~60% (based on `TESTING_SUMMARY_2026.md`).
- **Critical Gaps:**
  - `src/gui/settings_panel.py`: Complex configuration logic often missed.
  - `src/gui/notifications_panel.py`: User feedback mechanisms.
  - `src/core/contabilita_worker.py`: Critical async background processing.
  - `src/core/secrets_manager.py`: Security-sensitive code.

## 2. Goals
- **Short-term (1 week):** Fix valid test failures and achieve a clean test run.
- **Mid-term (1 month):** Increase overall coverage to **>85%**.
- **Long-term:** Establish automated E2E testing for critical user flows.

## 3. Detailed Strategy

### Phase 1: Stabilization & Baseline (Immediate)
- **Fix Dependencies:** Add `markdown` to `requirements.txt` / `pyproject.toml` and install.
- **Fix `test_ai_sentinel_hardened.py`:** Debug `PyQt6` mocking issues.
- **Generate Baseline Report:** Run `pytest --cov=src` and save HTML report.

### Phase 2: Core Logic Expansion
- **`src/core/contabilita_worker.py`:**
  - Test `run()` method with mocked `ContabilitaManager`.
  - Verify signal emissions (`progress`, `finished`, `error`).
- **`src/core/secrets_manager.py`:**
  - Test credential storage/retrieval with `keyring` mocks.
  - Verify encryption/decryption logic.

### Phase 3: GUI Hardening
- **`src/gui/settings_panel.py`:**
  - Test form validation logic.
  - Verify `save_config` triggers appropriate updates.
- **`src/gui/notifications_panel.py`:**
  - Verify adding/removing notifications.
  - Test persistence (if applicable).

### Phase 4: Integration & E2E
- **Database Migrations:** Create tests to verify schema updates.
- **Full Flow:** Simulate "Login -> Download Timbrature -> Check Anomalies" using `pytest-qt`.

## 4. Automation & Metrics
- **CI/CD:** Update `.github/workflows/ci.yml` to fail if coverage drops below 80%.
- **Pre-commit:** Add hook to run unit tests on changed files.
- **Review:** Weekly review of `htmlcov/index.html`.

## 5. Execution Script (`run_coverage_plan.bat`)
Create a script to:
1. Install missing deps.
2. Run tests with specific focus.
3. Generate report.
