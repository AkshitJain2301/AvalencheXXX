from pathlib import Path
import subprocess
import sys

project_dir = Path(__file__).resolve().parent
app_path = project_dir / "app.py"

if not app_path.exists():
    raise FileNotFoundError(f"Application file not found: {app_path}")

cmd = [sys.executable, "-m", "streamlit", "run", str(app_path), "--server.headless", "true"]
print(f"Running: {' '.join(cmd)}")
subprocess.run(cmd, cwd=str(project_dir))
