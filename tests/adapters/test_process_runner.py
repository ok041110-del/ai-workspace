from __future__ import annotations

import sys
import threading
import time

import pytest

from ai_workspace.adapters.process_runner import ProcessNotFoundError, ProcessRunner


def test_run_captures_stdout_and_success_returncode() -> None:
    runner = ProcessRunner()

    result = runner.run("p1", [sys.executable, "-c", "print('hello')"])

    assert result.returncode == 0
    assert result.stdout.strip() == "hello"


def test_run_captures_stderr_and_nonzero_returncode() -> None:
    runner = ProcessRunner()

    result = runner.run(
        "p1", [sys.executable, "-c", "import sys; print('boom', file=sys.stderr); sys.exit(3)"]
    )

    assert result.returncode == 3
    assert "boom" in result.stderr


def test_run_timeout_terminates_process_promptly() -> None:
    runner = ProcessRunner(termination_grace_seconds=1.0)

    start = time.monotonic()
    result = runner.run(
        "p1", [sys.executable, "-c", "import time; time.sleep(5)"], timeout=0.2
    )
    elapsed = time.monotonic() - start

    assert result.timed_out is True
    assert elapsed < 3.0  # 5초 sleep을 끝까지 기다리지 않고 강제 종료됐어야 한다


def test_cancel_unknown_process_raises_not_found() -> None:
    runner = ProcessRunner()

    with pytest.raises(ProcessNotFoundError):
        runner.cancel("unknown")


def test_cancel_while_running_terminates_promptly_and_marks_cancelled() -> None:
    runner = ProcessRunner()
    outcome: dict[str, object] = {}

    def _run() -> None:
        outcome["result"] = runner.run(
            "p1", [sys.executable, "-c", "import time; time.sleep(5)"], timeout=10.0
        )

    start = time.monotonic()
    runner_thread = threading.Thread(target=_run)
    runner_thread.start()
    time.sleep(0.2)
    runner.cancel("p1")
    runner_thread.join()
    elapsed = time.monotonic() - start

    assert outcome["result"].cancelled is True  # type: ignore[union-attr]
    assert elapsed < 3.0


def test_run_reuses_process_id_after_completion() -> None:
    runner = ProcessRunner()
    runner.run("p1", [sys.executable, "-c", "print('first')"])

    result = runner.run("p1", [sys.executable, "-c", "print('second')"])

    assert result.stdout.strip() == "second"
