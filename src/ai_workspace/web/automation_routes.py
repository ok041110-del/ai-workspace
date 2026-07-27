from __future__ import annotations

from dataclasses import dataclass

from fastapi import APIRouter, HTTPException, Request

from ai_workspace.domain.automation import Action, AutomationRule, Trigger
from ai_workspace.interfaces.automation_repository import AutomationRuleNotFoundError
from ai_workspace.runtime.automation.automation_scheduler import AutomationScheduler
from ai_workspace.runtime.automation.automation_service import AutomationService

router = APIRouter(prefix="/api/automation", tags=["automation"])


@dataclass
class AutomationRuleCreateRequest:
    """`POST /api/automation`의 요청 본문(M21-T05). Automation CRUD는
    이 라우터를 통해서만 이루어진다(사용자 승인 조건 3) — Web
    UI(M21-T06)도 이 API만 사용한다."""

    name: str
    description: str
    trigger: Trigger
    action: Action
    enabled: bool = True


@dataclass
class AutomationRuleUpdateRequest:
    """`PUT /api/automation/{id}`의 요청 본문. 넘긴 필드만 갱신한다
    (`AutomationService.update_rule`과 동일한 부분 갱신 의미론)."""

    name: str | None = None
    description: str | None = None
    trigger: Trigger | None = None
    action: Action | None = None


def _automation_service(request: Request) -> AutomationService:
    service: AutomationService = request.app.state.automation_service
    return service


def _automation_scheduler(request: Request) -> AutomationScheduler:
    scheduler: AutomationScheduler = request.app.state.automation_scheduler
    return scheduler


@router.get("", response_model=list[AutomationRule])
def list_rules(request: Request) -> list[AutomationRule]:
    return _automation_service(request).list_rules()


@router.get("/{rule_id}", response_model=AutomationRule)
def get_rule(rule_id: str, request: Request) -> AutomationRule:
    try:
        return _automation_service(request).get_rule(rule_id)
    except AutomationRuleNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("", response_model=AutomationRule, status_code=201)
def create_rule(body: AutomationRuleCreateRequest, request: Request) -> AutomationRule:
    return _automation_service(request).create_rule(
        name=body.name,
        description=body.description,
        trigger=body.trigger,
        action=body.action,
        enabled=body.enabled,
    )


@router.put("/{rule_id}", response_model=AutomationRule)
def update_rule(
    rule_id: str, body: AutomationRuleUpdateRequest, request: Request
) -> AutomationRule:
    try:
        return _automation_service(request).update_rule(
            rule_id,
            name=body.name,
            description=body.description,
            trigger=body.trigger,
            action=body.action,
        )
    except AutomationRuleNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/{rule_id}", status_code=204)
def delete_rule(rule_id: str, request: Request) -> None:
    try:
        _automation_service(request).delete_rule(rule_id)
    except AutomationRuleNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{rule_id}/enable", response_model=AutomationRule)
def enable_rule(rule_id: str, request: Request) -> AutomationRule:
    try:
        return _automation_service(request).enable_rule(rule_id)
    except AutomationRuleNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{rule_id}/disable", response_model=AutomationRule)
def disable_rule(rule_id: str, request: Request) -> AutomationRule:
    try:
        return _automation_service(request).disable_rule(rule_id)
    except AutomationRuleNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{rule_id}/run", status_code=202)
def run_rule(rule_id: str, request: Request) -> dict[str, str]:
    """Trigger 조건과 무관하게 즉시 실행한다(`AutomationScheduler.run_now`
    위임 — `ExecutionDispatcher`가 유일한 실행 진입점이라는 원칙은
    Scheduler 안에서 그대로 유지된다)."""
    try:
        _automation_scheduler(request).run_now(rule_id)
    except AutomationRuleNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"status": "accepted"}
