from ai_workspace.domain.workflow_order_memory import WorkflowOrderStat


def test_record_success_increments_total_and_success_count() -> None:
    stat = WorkflowOrderStat().record(True)

    assert stat == WorkflowOrderStat(total=1, success_count=1, failure_count=0)


def test_record_failure_increments_total_and_failure_count() -> None:
    stat = WorkflowOrderStat().record(False)

    assert stat == WorkflowOrderStat(total=1, success_count=0, failure_count=1)


def test_success_rate_none_when_no_records() -> None:
    assert WorkflowOrderStat().success_rate() is None


def test_success_rate_none_when_sample_size_insufficient() -> None:
    stat = WorkflowOrderStat()
    for _ in range(2):
        stat = stat.record(True)

    assert stat.success_rate() is None


def test_success_rate_computed_once_sample_size_sufficient() -> None:
    stat = WorkflowOrderStat()
    for _ in range(3):
        stat = stat.record(True)
    stat = stat.record(False)

    assert stat.success_rate() == 0.75
