"""支持 ``python -m statline`` 直接运行。"""

import sys

from statline.cli import main

if __name__ == "__main__":
    sys.exit(main())
