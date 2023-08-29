import os
import re
import math
import cv2 as cv
import pandas as pd

# FILTER FRAMES
FRAMES_IN_EACH_SEC = 4
videos = [4.0, 5.0, 6.0, 7.0, 9.0, 10.0, 12.1, 12.2, 12.3, 12.4, 31.1, 31.2, 31.3, 32.1, 32.2, 33.1, 33.2, 33.3, 33.4, 33.5, 35.1, 35.2, 35.3, 35.4, 35.5, 35.6, 35.7, 35.8, 36.1, 36.2, 36.3, 36.4, 36.5, 37.1, 37.2, 37.3, 39.1, 39.2, 40.0, 40.2, 40.3]

def get_fps(f):
    c = cv.VideoCapture(fr'C:\Users\aicpl\ShipsDatasets\VideoDataset\videos\video_{math.floor(f)}.mp4')
    return c.get(cv.CAP_PROP_FPS)

fps_dict = {v: math.floor(get_fps(v)) for v in videos}

images = sorted(os.listdir('Images'))
labels = sorted(os.listdir('Labels'))

df = pd.DataFrame({'image': images, 'label': labels})

print('TOTAL IMAGES IN DATASET:', df.shape[0])

def change_keep(a, video):
    fname = os.path.splitext(a)[0]
    b, f = re.split('_frame_', fname)
    b = float(b[5:])
    f = int(f)
    if b in fps_dict and f % int(fps_dict[video] / FRAMES_IN_EACH_SEC) == 0:
        return True
    elif b in fps_dict and f % int(fps_dict[video] / FRAMES_IN_EACH_SEC) != 0:
        return False
    else:
        return True

for v in fps_dict:
    df['keep'] = df['image'].apply(lambda a: change_keep(a, v))
df = df[df['keep'] == True]
df.reset_index(drop=True, inplace=True)
df = df.drop(columns=['keep'])

print('FRAMES TAKEN FROM EACH SECOND OF VIDEO:', FRAMES_IN_EACH_SEC)

print('TOTAL IMAGES AFTER FILTERING:', df.shape[0])

df.to_csv('df.csv', index=False)
