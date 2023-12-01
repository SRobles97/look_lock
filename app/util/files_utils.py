import os
import uuid


# Rename file to have a naming convention
def rename_file(original_filename):
    ext = os.path.splitext(original_filename)[1]
    new_filename = f"locklock-face[{uuid.uuid4()}]{ext}"
    return new_filename
