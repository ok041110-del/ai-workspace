from ai_workspace.domain.consensus_agreement import ConsensusAgreementStat


def test_record_agree_increments_total_and_agree_count() -> None:
    stat = ConsensusAgreementStat().record(True)

    assert stat == ConsensusAgreementStat(total=1, agree_count=1, disagree_count=0)


def test_record_disagree_increments_total_and_disagree_count() -> None:
    stat = ConsensusAgreementStat().record(False)

    assert stat == ConsensusAgreementStat(total=1, agree_count=0, disagree_count=1)


def test_agreement_rate_none_when_no_records() -> None:
    assert ConsensusAgreementStat().agreement_rate() is None


def test_agreement_rate_none_when_sample_size_insufficient() -> None:
    stat = ConsensusAgreementStat()
    for _ in range(2):
        stat = stat.record(True)

    assert stat.agreement_rate() is None


def test_agreement_rate_computed_once_sample_size_sufficient() -> None:
    stat = ConsensusAgreementStat()
    for _ in range(3):
        stat = stat.record(True)
    stat = stat.record(False)

    assert stat.agreement_rate() == 0.75
