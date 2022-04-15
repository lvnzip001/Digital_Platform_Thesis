
import sys

# adding Folder_2 to the system patm
sys.path.insert(0, 'C:/Digital_Platform_Thesis/app/app')
from settings import AUDIO_ROOT
print(AUDIO_ROOT)



from pathlib import Path
import os

dir_int = Path(__file__).resolve().parent.parent 
setting_dir = (
    os.path.join(dir_int, 'app'),
)