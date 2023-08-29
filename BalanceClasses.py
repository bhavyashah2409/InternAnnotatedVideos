import os
import math
import cv2 as cv
import pandas as pd
import datetime as dt
import albumentations as a

AREA_THRESHOLD = 200
TRANSFORM = a.Compose([
    a.HorizontalFlip(p=0.2),
    a.ColorJitter(brightness=(0.8, 1.2), contrast=(0.8, 1.2), saturation=(0.9, 1.1), hue=(-0.1, 0.1), p=0.2),
    # a.Emboss(alpha=(0.1, 0.3), strength=(0.1, 0.5), p=0.1),
    a.Equalize(p=0.2),
    a.HueSaturationValue(hue_shift_limit=(-5, 5), sat_shift_limit=(-5, 5), val_shift_limit=(-1, 1), p=0.2),
    # a.RGBShift(r_shift_limit=(-5, 5), g_shift_limit=(-5, 5), b_shift_limit=(-5, 5), p=0.1),
    a.Sharpen(alpha=(0.1, 0.3), p=0.2),
    # a.GaussianBlur(blur_limit=(1, 5), sigma_limit=(0.1, 0.3), p=0.1),
    # a.Rotate(limit=(-45, 45), interpolation=cv.INTER_CUBIC, value=0, p=0.1),
    # a.SafeRotate(limit=(-45, 45), interpolation=cv.INTER_CUBIC, border_mode=cv.BORDER_REFLECT_101),
    # a.ShiftScaleRotate(shift_limit=(0.01, 0.05), scale_limit=(-0.2, 0.2), rotate_limit=(0.0, 0.0), interpolation=cv.INTER_CUBIC, border_mode=cv.BORDER_REFLECT_101, p=0.1),
    # a.NoOp(p=0.1),
    ], bbox_params=a.BboxParams(format='yolo', min_area=AREA_THRESHOLD))

df = pd.read_csv('train_df.csv')
df = pd.DataFrame(df)
print(df.head())
print(df.shape[0])

def read_labels(a):
    with open(a, 'r') as f:
        bboxes = f.read().split('\n')
        bboxes.remove('')
        bboxes = [bbox.split(' ') for bbox in bboxes]
        bboxes = [[int(c), float(x), float(y), float(w), float(h)] for c, x, y, w, h in bboxes]
        f.close()
    b = []
    for c, x, y, w, h in bboxes:
        xmin = x - (w / 2.0)
        ymin = y - (h / 2.0)
        xmax = x + (w / 2.0)
        ymax = y + (h / 2.0)
        if xmin < 0.0:
            xmin = 0.0
        elif xmin > 1.0:
            xmin = 1.0
        if ymin < 0.0:
            ymin = 0.0
        elif ymin > 1.0:
            ymin = 1.0
        if xmax < 0.0:
            xmax = 0.0
        elif xmax > 1.0:
            xmax = 1.0
        if ymax < 0.0:
            ymax = 0.0
        elif ymax > 1.0:
            ymax = 1.0
        x = (xmax + xmin) / 2.0
        y = (ymax + ymin) / 2.0
        w = xmax - xmin
        h = ymax - ymin
        b.append([c, x, y, w, h])
    return b
df['bbox'] = df['label'].apply(lambda a: read_labels(a))
print(df.head())

classes = open('classes.txt', 'r').read().split('\n')
classes.remove('')

def count_classes(a, count):
    for c, _, _, _, _ in a:
        count[classes[c]] = count[classes[c]] + 1
    return a

class_count = {c: 0 for c in classes}
df['bbox'] = df['bbox'].apply(lambda a: count_classes(a, class_count))
print(class_count)

counts = list(class_count.values())
max_count = max(counts)
min_count = min(counts)
iterations = math.ceil(max_count / min_count)

if not os.path.exists('augment'):
    os.mkdir('augment')
if not os.path.exists(os.path.join('augment', 'images')):
    os.mkdir(os.path.join('augment', 'images'))
if not os.path.exists(os.path.join('augment', 'labels')):
    os.mkdir(os.path.join('augment', 'labels'))

def augment_and_balance_class(a, transform, img_folder, label_folder, stamp, m):
    img_path = a['image']
    img = cv.imread(img_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    bboxes = a['bbox']
    bboxes = [[x, y, w, h, c] for c, x, y, w, h in bboxes]
    aug = transform(image=img, bboxes=bboxes)
    aug_bboxes = aug['bboxes']
    b = []
    for x, y, w, h, c in aug_bboxes:
        if class_count[classes[c]] < m:
            b.append([x, y, w, h, c])
            class_count[classes[c]] = class_count[classes[c]] + 1
    aug_img = aug['image']
    cv.imwrite(os.path.join(img_folder, stamp + f'_{a.name}.png'), aug_img)
    with open(os.path.join(label_folder, stamp + f'_{a.name}.txt'), 'w') as f:
        for x, y, w, h, c in b:
            f.write(f'{c} {x} {y} {w} {h}\n')
        f.close()
    return os.path.join(img_folder, stamp + f'_{a.name}.PNG'), os.path.join(label_folder, stamp + f'_{a.name}.txt'), b

def remove_blank_images_and_labels(a):
    if not a['keep']:
        os.remove(a['image'])
        os.remove(a['label'])

all_aug = pd.DataFrame({'image': [], 'label': [], 'bbox': []})
for i in range(iterations):
    now = dt.datetime.now()
    now = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}'
    aug_df = df.apply(lambda a: augment_and_balance_class(a, TRANSFORM, 'augment\images', 'augment\labels', now, max_count), axis=1, result_type='expand')
    aug_df.columns = ['image', 'label', 'bbox']
    aug_df['keep'] = aug_df['bbox'].apply(lambda a: True if len(a) > 0 else False)
    aug_df.apply(lambda a: remove_blank_images_and_labels(a), axis=1, result_type=None)
    aug_df = aug_df[aug_df['keep'] == True]
    aug_df.reset_index(drop=True, inplace=True)
    aug_df = aug_df.drop(columns=['keep'])
    all_aug = pd.concat([all_aug, aug_df], axis=0, ignore_index=True)
    print(f'ITERATION {i} DONE')
all_aug = all_aug.drop(columns=['bbox'])
all_aug.to_csv('aug_df.csv', index=False)
