import os
import pandas as pd

IMAGE_DIR = 'Images'
LABEL_DIR = 'Labels'

df = pd.read_csv('train_df.csv')
df = pd.DataFrame(df)

if os.path.exists('aug_df.csv'):
    aug_df = pd.read_csv('aug_df.csv')
    aug_df = pd.DataFrame(aug_df)

    def move_augment_images_and_labels(a, img_dir, label_dir):
        img_path = a['image']
        os.rename(img_path, os.path.join(img_dir, os.path.basename(img_path)))
        label_path = a['label']
        os.rename(img_path, os.path.join(label_dir, os.path.basename(label_path)))

    aug_df.apply(lambda a: move_augment_images_and_labels(a, IMAGE_DIR, LABEL_DIR), axis=1, result_type=None)
    df = pd.concat([df, aug_df], axis=0, ignore_index=True)

df.to_csv('train_df.csv', index=False)
