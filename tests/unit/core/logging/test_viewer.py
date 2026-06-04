import json
from pathlib import Path

import pytest

from src.application.services.logging.viewer import LogQuery


@pytest.fixture
def temp_log_file(tmp_path):
    log_file = tmp_path / "test.log"
    data = [
        {"level": "INFO", "message": "Test message 1", "context": {"bot_type": "PrenotaBP"}},
        {"level": "ERROR", "message": "Test error", "context": {"trace_id": "123"}},
        {"level": "INFO", "message": "Other message", "context": {"bot_type": "ScaricoTS"}},
    ]
    with open(log_file, "w") as f:
        f.writelines(json.dumps(entry) + "\n" for entry in data)
    return log_file


def test_log_query_execute_and_count(temp_log_file):
    query = LogQuery(temp_log_file)
    results = query.level("INFO").execute()
    assert len(results) == 2
    assert query.count() == 2


def test_log_query_pagination(temp_log_file):
    query = LogQuery(temp_log_file)
    # Test offset
    results = query.offset(1).execute()
    assert len(results) == 2  # Escludendo il primo, ne restano 2 (1 info, 1 error)

    # Test limit
    query2 = LogQuery(temp_log_file)
    results2 = query2.limit(1).execute()
    assert len(results2) == 1


def test_log_query_no_file():
    query = LogQuery(Path("non_existent.log"))
    assert query.execute() == []
    assert query.count() == 0
