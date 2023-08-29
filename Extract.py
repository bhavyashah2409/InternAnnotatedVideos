import os
import shutil as s

print('EXTRACTION STARTED')

# CREATE FOLDERS TO MOVE FILES
if not os.path.exists('Images'):
    os.mkdir('Images')
if not os.path.exists('Labels'):
    os.mkdir('Labels')

# MOVE FILES TO RESPECTIVE FOLDERS
for f in sorted(os.listdir(r'Shreyas1\annotations_new')):
    old_path = os.path.join('Shreyas1', 'annotations_new', f)
    if os.path.splitext(f)[-1] == '.PNG' or os.path.splitext(f)[-1] == '.png' or os.path.splitext(f)[-1] == '.JPG' or os.path.splitext(f)[-1] == '.jpg' or os.path.splitext(f)[-1] == '.JPEG' or os.path.splitext(f)[-1] == '.jpeg':
        new_path = os.path.join('Images', f)
        os.rename(old_path, new_path)
    elif os.path.splitext(f)[-1] == '.txt':
        os.rename(old_path, os.path.join('Labels', f))

for f in sorted(os.listdir(r'Shreyas2\new_annotations_shreyas')):
    old_path = os.path.join('Shreyas2', 'new_annotations_shreyas', f)
    if os.path.splitext(f)[-1] == '.PNG' or os.path.splitext(f)[-1] == '.png' or os.path.splitext(f)[-1] == '.JPG' or os.path.splitext(f)[-1] == '.jpg' or os.path.splitext(f)[-1] == '.JPEG' or os.path.splitext(f)[-1] == '.jpeg':
        new_path = os.path.join('Images', f)
        os.rename(old_path, new_path)
    elif os.path.splitext(f)[-1] == '.txt':
        os.rename(old_path, os.path.join('Labels', f))

for f in sorted(os.listdir(r'Gayatri1\annotationsForVideos')):
    old_path = os.path.join('Gayatri1', 'annotationsForVideos', f)
    if os.path.splitext(f)[-1] == '.PNG' or os.path.splitext(f)[-1] == '.png' or os.path.splitext(f)[-1] == '.JPG' or os.path.splitext(f)[-1] == '.jpg' or os.path.splitext(f)[-1] == '.JPEG' or os.path.splitext(f)[-1] == '.jpeg':
        new_path = os.path.join('Images', f)
        os.rename(old_path, new_path)
    elif os.path.splitext(f)[-1] == '.txt':
        os.rename(old_path, os.path.join('Labels', f))

for f in sorted(os.listdir(r'Gayatri2\annotatedVideos')):
    old_path = os.path.join('Gayatri2', 'annotatedVideos', f)
    if os.path.splitext(f)[-1] == '.PNG' or os.path.splitext(f)[-1] == '.png' or os.path.splitext(f)[-1] == '.JPG' or os.path.splitext(f)[-1] == '.jpg' or os.path.splitext(f)[-1] == '.JPEG' or os.path.splitext(f)[-1] == '.jpeg':
        new_path = os.path.join('Images', f)
        os.rename(old_path, new_path)
    elif os.path.splitext(f)[-1] == '.txt':
        os.rename(old_path, os.path.join('Labels', f))

# REMOVE UNNECESSARY FOLDERS
s.rmtree(r'Shreyas1')
s.rmtree(r'Shreyas2')
s.rmtree(r'Gayatri1')
s.rmtree(r'Gayatri2')

print('EXTRACTION DONE')
