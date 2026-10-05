import subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
def test_all_engines_exit_zero():
    for f in sorted((ROOT/"src/slge").glob("*.py")):
        assert subprocess.run([sys.executable, str(f)], capture_output=True).returncode == 0, f.name
