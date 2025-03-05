import os, sys
sys.path.append("..")
from segment_anything import sam_model_registry, SamPredictor

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

sam_checkpoint = "CorSA 2 1.0.0/sam_vit_b_01ec64.pth"
# sam_checkpoint = resource_path("sam_vit_b_01ec64.pth")
model_type = "vit_b"

# sam_checkpoint = "CorSA_v2.1.1/sam_vit_h_4b8939.pth"
# sam_checkpoint = resource_path("sam_vit_h_4b8939.pth")
# model_type = "vit_h"

device = "cuda"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)

predictor = SamPredictor(sam)

