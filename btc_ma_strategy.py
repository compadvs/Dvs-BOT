import sys
from pathlib import Path
import runpy

# Add cloned libraries to path if available
MCPT_DIR = Path(__file__).resolve().parent / 'libs' / 'mcpt'
SCRIPT_PATH = MCPT_DIR / 'moving_average.py'


def run():
    if not SCRIPT_PATH.exists():
        print('Libraries not found. Run fetch_dependencies.sh first.')
        return
    sys.path.insert(0, str(MCPT_DIR))
    runpy.run_path(str(SCRIPT_PATH), run_name='__main__')


if __name__ == '__main__':
    run()

