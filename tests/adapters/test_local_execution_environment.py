from __future__ import annotations

import sys
import threading
import time

import pytest

from ai_workspace.adapters.local_execution_environment import LocalExecutionEnvironment
from ai_workspace.interfaces.execution_environment import ExecutionNotFoundError


def test_execute_captures_stdout_and_success_returncode() -> None:
    environment = LocalExecutionEnvironment()

    result = environment.execute("e1", [sys.executable, "-c", "print('hello')"])

    assert result.returncode == 0
    assert result.stdout.strip() == "hello"


def test_execute_captures_stderr_and_nonzero_returncode() -> None:
    environment = LocalExecutionEnvironment()

    result = environment.execute(
        "e1", [sys.executable, "-c", "import sys; print('boom', file=sys.stderr); sys.exit(3)"]
    )

    assert result.returncode == 3
    assert "boom" in result.stderr


def test_execute_timeout_terminates_process_promptly() -> None:
    environment = LocalExecutionEnvironment()

    start = time.monotonic()
    result = environment.execute(
        "e1", [sys.executable, "-c", "import time; time.sleep(5)"], timeout=0.2
    )
    elapsed = time.monotonic() - start

    assert result.timed_out is True
    assert elapsed < 3.0  # 5초 sleep을 끝까지 기다리지 않고 강제 종료됐어야 한다


def test_cancel_unknown_execution_id_raises_not_found() -> None:
    environment = LocalExecutionEnvironment()

    with pytest.raises(ExecutionNotFoundError):
        environment.cancel("unknown")


def test_cancel_while_running_terminates_promptly_and_marks_cancelled() -> None:
    environment = LocalExecutionEnvironment()
    outcome: dict[str, object] = {}

    def _run() -> None:
        outcome["result"] = environment.execute(
            "e1", [sys.executable, "-c", "import time; time.sleep(5)"], timeout=10.0
        )

    start = time.monotonic()
    execution_thread = threading.Thread(target=_run)
    execution_thread.start()
    time.sleep(0.2)
    environment.cancel("e1")
    execution_thread.join()
    elapsed = time.monotonic() - start

    assert outcome["result"].cancelled is True  # type: ignore[union-attr]
    assert elapsed < 3.0
