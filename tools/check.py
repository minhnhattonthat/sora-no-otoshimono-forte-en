"""One-command check (pre-commit runs this): all tests."""
import subprocess
import sys

sys.exit(subprocess.call([sys.executable, '-X', 'utf8', '-m', 'pytest', '-q', 'tests']))
