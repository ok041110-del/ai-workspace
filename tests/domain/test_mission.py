from ai_workspace.domain.mission import Mission


def test_mission_holds_goal_and_project_reference() -> None:
    mission = Mission(mission_id="m1", project_id="p1", goal="문서 체계 완성")

    assert mission.project_id == "p1"
    assert mission.goal == "문서 체계 완성"
