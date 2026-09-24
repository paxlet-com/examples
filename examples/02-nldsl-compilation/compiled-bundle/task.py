#!/usr/bin/env python3
# Standalone nl-dsl-sh bundle. No nl-dsl-sh or LiteLLM installation required.
import base64
import json
import os
import signal
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    payload = json.loads(base64.b64decode('eyJibG9icyI6eyI5NTcxNjYxZDc3ZDllN2QyNTM2ODc1NTdmOTAyNjkwMzljZDE0MDIyYjY2OTJkNzJhZDlkNmU2ZTUxMzBkMjAwIjoiIyEvdXNyL2Jpbi9lbnYgYmFzaFxuc2V0IC1ldW8gcGlwZWZhaWxcbnByaW50ZiAnV2l0YWosICVzIVxcbicgXCIkezE6LcWbd2llY2llfVwiXG4iLCJkMTY5ZTg0N2E5NWM5NWJiZGRjZjZiYjIzNjViZDkxODk3MTFjYjBiMzc2MTBlODU0M2IwZDNkOTE5MDY0Y2RiIjoiaW1wb3J0IGpzb25cbnByaW50KGpzb24uZHVtcHMoeydzdGF0dXMnOiAnb2snLCAnc291cmNlJzogJ3B5dGhvbid9KSlcbiJ9LCJwYWNrYWdlcyI6eyIwZDQ3ODczOTI3N2U1NzBhYmY1NWE5ZDU3OTJjMmQ0NzdmYmYzYmUxMDEwNjcyYjc5MDMwYzIwYjU5Mzg3ZTY1Ijp7ImhlbGxvLnNoIjoiOTU3MTY2MWQ3N2Q5ZTdkMjUzNjg3NTU3ZjkwMjY5MDM5Y2QxNDAyMmI2NjkyZDcyYWQ5ZDZlNmU1MTMwZDIwMCJ9LCI3MTllYWFhMmQzYzNkYmNjOGQ2ZGM3ZWUxNzBjZGU5MWM0ZWRmMzhkOWRlOTYxYzFjYjdlMGE4MTA3N2Q5YTQ4Ijp7Im1haW4ucHkiOiJkMTY5ZTg0N2E5NWM5NWJiZGRjZjZiYjIzNjViZDkxODk3MTFjYjBiMzc2MTBlODU0M2IwZDNkOTE5MDY0Y2RiIn19LCJzdGVwcyI6W3siYXJncyI6WyJUb20iXSwiYXJndiI6WyJiYXNoIl0sImN3ZCI6bnVsbCwiZW50cnkiOiJoZWxsby5zaCIsImVudiI6e30sImlkIjoiaGVsbG8iLCJwYWNrYWdlIjoiMGQ0Nzg3MzkyNzdlNTcwYWJmNTVhOWQ1NzkyYzJkNDc3ZmJmM2JlMTAxMDY3MmI3OTAzMGMyMGI1OTM4N2U2NSJ9LHsiYXJncyI6W10sImFyZ3YiOlsicHl0aG9uMyJdLCJjd2QiOm51bGwsImVudHJ5IjoibWFpbi5weSIsImVudiI6e30sImlkIjoicmVwb3J0IiwicGFja2FnZSI6IjcxOWVhYWEyZDNjM2RiY2M4ZDZkYzdlZTE3MGNkZTkxYzRlZGYzOGQ5ZGU5NjFjMWNiN2UwYTgxMDc3ZDlhNDgifV19'))
    caller = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="nl-dsl-sh-") as temp:
        root = Path(temp)
        for tree, files in payload["packages"].items():
            for name, key in files.items():
                path = root / tree / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(payload["blobs"][key].encode("utf-8"))
                path.chmod(0o700)
        for step in payload["steps"]:
            directory = root / step["package"]
            cwd = step["cwd"]
            cwd = directory if cwd == "@bundle" else caller / cwd if cwd else caller
            env = dict(os.environ, **step["env"])
            argv = list(step["argv"])
            if argv[0] == "python3":
                argv[0] = sys.executable
            result = subprocess.run([*argv, str(directory / step["entry"]), *step["args"]],
                                    cwd=cwd, env=env)
            if result.returncode:
                return result.returncode if result.returncode > 0 else 128 - result.returncode
    return 0


if __name__ == "__main__":
    def stop(signum, frame):
        # Unwind TemporaryDirectory and subprocess.run on cooperative termination.
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        sys.exit(main())
    except OSError as exc:
        print("nl-dsl-sh runtime:", exc, file=sys.stderr)
        sys.exit(127)
