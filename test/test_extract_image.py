import os
import sys

try:
    from src.utils.helper_functions import (
        extract_images_from_video, 
        extract_images_from_mp4
    )
except ImportError:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_root = os.path.abspath(os.path.join(current_dir, "../"))
    sys.path.insert(0, src_root)
    from src.utils.helper_functions import (
        extract_images_from_video, 
        extract_images_from_mp4
    ) 

import uuid

extract_images_from_video(id=str(uuid.uuid4()), 
                          path_link='http://youtube.com/watch?v=2lAe1cqCOXo')