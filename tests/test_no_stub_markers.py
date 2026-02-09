from pathlib import Path
import re


FORBIDDEN = re.compile(r"\bpass\b|TODO|not implemented|NotImplementedError|stub", re.IGNORECASE)


def test_no_forbidden_stub_markers_in_src() -> None:
    failures: list[str] = []
    for path in Path("src").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if FORBIDDEN.search(text):
            failures.append(str(path))
    assert not failures, f"Forbidden markers found in: {failures}"
