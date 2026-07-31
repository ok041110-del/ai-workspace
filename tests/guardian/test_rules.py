import dataclasses

import pytest

from ai_workspace.guardian.rules import GUARDIAN_RULES, ForbiddenPackageImportRule


def test_guardian_rules_is_an_immutable_tuple() -> None:
    assert isinstance(GUARDIAN_RULES, tuple)


def test_guardian_rules_has_unique_names() -> None:
    names = [rule.name for rule in GUARDIAN_RULES]
    assert len(names) == len(set(names)), f"중복된 규칙 이름: {names}"


def test_rule_instances_are_frozen() -> None:
    rule = ForbiddenPackageImportRule(
        name="x", source_packages=("domain",), forbidden_packages=("vault",)
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        rule.name = "y"  # type: ignore[misc]
