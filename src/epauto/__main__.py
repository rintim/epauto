"""
Entrypoint for epauto.
"""

import sys
from epauto import cli


if __name__ == "__main__":
    sys.exit(cli.main())
