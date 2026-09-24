import json
from pathlib import Path
import subprocess
import sys

request = json.load(sys.stdin)
if not isinstance(request, dict) or set(request) - {"stdin"} or not isinstance(request.get("stdin", ""), str):
    print("Expected object with optional string stdin", file=sys.stderr)
    sys.exit(2)
result = subprocess.run([sys.executable, str(Path(__file__).with_name("task.py"))],
                        input=request.get("stdin", ""), text=True, capture_output=True)
print(json.dumps({"exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}))
sys.exit(result.returncode if result.returncode >= 0 else 128 - result.returncode)
