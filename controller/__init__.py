import os
import glob

__all__ = [
    # 'user_controller', 'product_controller'

    os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*py")
]