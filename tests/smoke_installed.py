import json
import os
import subprocess
import sys
import sysconfig
import tempfile
from importlib.metadata import distribution
from pathlib import Path

import statline
from statline._vendor.cjktable import width


dist = distribution("statline")
assert dist.version == statline.__version__ == "1.0.1"
assert dist.metadata["Requires-Python"] == ">=3.9"
assert not dist.requires
assert dist.read_text("top_level.txt").split() == ["statline"]
assert Path(statline.__file__).resolve() == Path(
    dist.locate_file("statline/__init__.py")).resolve()
files = {str(path).replace("\\", "/") for path in dist.files or []}
assert "statline/_vendor/cjktable/__init__.py" in files
assert "statline/_vendor/cjktable/core.py" in files
assert "statline/_vendor/cjktable/render.py" in files
assert not any(path.startswith("cjktable/") for path in files)
assert width("中文") == 4
assert any(
    ep.group == "console_scripts"
    and ep.name == "statline"
    and ep.value == "statline.cli:main"
    for ep in dist.entry_points
)

with tempfile.TemporaryDirectory() as tmp:
    env = {**os.environ, "PYTHONIOENCODING": "cp1252", "PYTHONUTF8": "0"}
    env.pop("PYTHONPATH", None)
    data = b"12\n98\n45\n67"

    result = subprocess.run(
        [sys.executable, "-m", "statline", "--help"],
        cwd=tmp, capture_output=True, env=env,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8")
    assert "零运行时依赖" in result.stdout.decode("utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "statline", "--version"],
        cwd=tmp, capture_output=True, env=env,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8")
    assert "statline 1.0.1" in result.stdout.decode("utf-8")

    script = Path(sysconfig.get_path("scripts")) / (
        "statline.exe" if os.name == "nt" else "statline")
    assert script.is_file(), script
    result = subprocess.run([str(script), "--version"], cwd=tmp,
                            capture_output=True, env=env)
    assert result.returncode == 0, result.stderr.decode("utf-8")
    assert "statline 1.0.1" in result.stdout.decode("utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "statline", "--no-hist"],
        input=data, cwd=tmp, capture_output=True, env=env,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8")
    output = result.stdout.decode("utf-8")
    assert "样本数" in output
    assert "中位数" in output
    assert "55.5" in output
    assert "█" not in output

    result = subprocess.run(
        [sys.executable, "-m", "statline", "--json"],
        input=data, cwd=tmp, capture_output=True, env=env,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8")
    payload = json.loads(result.stdout.decode("utf-8"))
    assert payload["count"] == 4
    assert payload["mean"] == 55.5
    assert "histogram" in payload

    data_file = Path(tmp) / "数据.txt"
    data_file.write_text("1,2\n3,4", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "statline", str(data_file), "--json", "--no-hist"],
        cwd=tmp, capture_output=True, env=env,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8")
    payload = json.loads(result.stdout.decode("utf-8"))
    assert payload["count"] == 4
    assert payload["mean"] == 2.5

print("installed smoke: OK")
