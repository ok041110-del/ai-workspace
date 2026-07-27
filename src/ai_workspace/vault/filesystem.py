"""M24-T02: Filesystem Adapter.

`vault/writer.py`/`vault/sync.py`는 처음부터 Mock 없이 실제
`pathlib`/`os` 호출로 동작해 왔다(단위 테스트가 쓰는 `tmp_path`도
진짜 파일시스템이다 — Fake가 아니다). 이 모듈은 그 7개 기본 연산
(Create/Read/Update/Delete/Exists/Rename/Move)을 명시적인 이름으로
한 곳에 모아, "이 시스템에 별도 Mock 파일시스템 계층이 없다"는
사실과 각 연산의 경계를 분명히 한다."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.vault.atomic import atomic_write_text


class VaultFileSystem:
    """실제 Vault 위에서 동작하는 기본 파일 연산."""

    def create(self, path: Path, content: str) -> None:
        if path.exists():
            raise FileExistsError(f"이미 존재하는 파일입니다: {path}")
        atomic_write_text(path, content)

    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def update(self, path: Path, content: str) -> None:
        if not path.exists():
            raise FileNotFoundError(path)
        atomic_write_text(path, content)

    def delete(self, path: Path) -> None:
        path.unlink()

    def exists(self, path: Path) -> bool:
        return path.exists()

    def rename(self, path: Path, new_name: str) -> Path:
        target = path.with_name(new_name)
        path.rename(target)
        return target

    def move(self, path: Path, target_dir: Path) -> Path:
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / path.name
        path.rename(target)
        return target
