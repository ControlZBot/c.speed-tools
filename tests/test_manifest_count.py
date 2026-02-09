from pathlib import Path
import yaml

def test_manifest_count() -> None:
    path = Path("src/cspeed_tools/manifest/commands_manifest.yaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert len(data["endpoints"]) == 574
