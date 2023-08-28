import os
import zipfile as z

if not os.path.exists('AllImagesAndLabels'):
    os.mkdir('AllImagesAndLabels')
if not os.path.exists('Images'):
    os.mkdir('Images')
if not os.path.exists('Labels'):
    os.mkdir('Labels')

with z.ZipFile('ShreyasAnnotations.zip', 'r') as zip_file:
    zip_file.extractall('AllImagesAndLabels')
with z.ZipFile('GayatriAnnotations.zip', 'r') as zip_file:
    zip_file.extractall('AllImagesAndLabels')

for f in sorted(os.listdir(r'AllImagesAndLabels\annotations_new')):
    old_path = os.path.join('AllImagesAndLabels', 'annotations_new', f)
    if os.path.splitext(f)[-1] == '.PNG' or os.path.splitext(f)[-1] == '.png' or os.path.splitext(f)[-1] == '.JPG' or os.path.splitext(f)[-1] == '.jpg' or os.path.splitext(f)[-1] == '.JPEG' or os.path.splitext(f)[-1] == '.jpeg':
        new_path = os.path.join('Images', f)
        os.rename(old_path, new_path)
    elif os.path.splitext(f)[-1] == '.txt':
        os.rename(old_path, os.path.join('Labels', f))

for f in sorted(os.listdir(r'AllImagesAndLabels\annotationsForVideos')):
    old_path = os.path.join('AllImagesAndLabels', 'annotationsForVideos', f)
    if os.path.splitext(f)[-1] == '.PNG' or os.path.splitext(f)[-1] == '.png' or os.path.splitext(f)[-1] == '.JPG' or os.path.splitext(f)[-1] == '.jpg' or os.path.splitext(f)[-1] == '.JPEG' or os.path.splitext(f)[-1] == '.jpeg':
        new_path = os.path.join('Images', f)
        os.rename(old_path, new_path)
    elif os.path.splitext(f)[-1] == '.txt':
        os.rename(old_path, os.path.join('Labels', f))

os.rmdir(r'AllImagesAndLabels\annotations_new')
os.rmdir(r'AllImagesAndLabels\annotationsForVideos')
os.rmdir(r'AllImagesAndLabels')
