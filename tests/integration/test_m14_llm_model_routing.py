from __future__ import annotations

from tests.integration.test_m6_policy_routing import assemble


def test_coding_role_model_reaches_claude_code_adapter_command() -> None:
    """Milestone 14 DoD 4번: `docs/llm_policy.example.yaml`의 실제 정책
    (coding→anthropic/opus)에 따라 CodingAgent가 실제 `ClaudeCodeEngineAdapter`
    에 `model="opus"`를 전달하고, 그 결과 실제 명령에 `--model opus`가
    포함됨을 증명한다. M6 test_m6_policy_routing.assemble()을 그대로
    재사용한다(Provider 라우팅은 이미 M6에서 검증됨, M14는 그 위에
    Model까지 실제로 반영되는지만 추가로 확인)."""
    pipeline = assemble()

    pipeline["planning_agent"].plan_mission("p1", "구현하기")

    claude_commands = [
        command
        for command in pipeline["execution_environment"].executed_commands
        if command[0] == "claude"
    ]
    assert len(claude_commands) == 1
    assert "--model" in claude_commands[0]
    assert "opus" in claude_commands[0]
