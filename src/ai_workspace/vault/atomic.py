"""M24-T03: Atomic Write.

저장 도중 프로세스가 중단돼도 대상 파일이 반쪽짜리 상태로 남지
않도록, 같은 디렉터리에 임시 파일을 먼저 쓰고 `os.replace()`로
원자적으로 교체한다(POSIX/Windows 모두 `os.replace`가 원자적 교체를
보장)."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(tmp_name, path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise
