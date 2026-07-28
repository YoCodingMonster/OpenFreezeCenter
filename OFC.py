#!/usr/bin/env python3
"""Open Freeze Center launcher.

    sudo ./OFC.py              control the real embedded controller
    ./OFC.py --simulate        run the interface against a fake EC
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ofc.app import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
