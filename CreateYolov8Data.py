import os
import pandas as pd
from sklearn.model_selection import train_test_split

print('CREATION OF YOLO V8 DATA STARTED')

# MAKE TRAINING AND VALIDATION FOLDERS
if not os.path.exists(r'data'):
    os.mkdir('data')
if not os.path.exists(r'data\train'):
    os.mkdir(r'data\train')
if not os.path.exists(r'data\train\images'):
    os.mkdir(r'data\train\images')
if not os.path.exists(r'data\train\labels'):
    os.mkdir(r'data\train\labels')
if not os.path.exists(r'data\val'):
    os.mkdir(r'data\val')
if not os.path.exists(r'data\val\images'):
    os.mkdir(r'data\val\images')
if not os.path.exists(r'data\val\labels'):
    os.mkdir(r'data\val\labels')

# CREATE custom_data.yaml FOR YOLO TRAINING
with open(r'custom_data.yaml', 'w') as f:
    f.write("path: 'data\\'\n")
    f.write("train: 'train\images'\n")
    f.write("val: 'val\images'\n")
    f.write("\n")
    f.write("nc: 11\n")
    f.write("\n")
    f.write("names: ['Boat', 'Cargoship', 'Cruiseship', 'Ferry', 'Militaryship', 'Miscboat', 'Miscellaneous', 'Motorboat', 'Passengership', 'Sailboat', 'Seamark']")
    f.close()

# READ DATAFRAME
df = pd.read_csv('train_df.csv')
df = pd.DataFrame(df)
print('TOTAL IMAGES:', df.shape[0])

# SPLIT DATAFRAME
TEST_SIZE = 0.2
train_df, val_df = train_test_split(df, test_size=TEST_SIZE, random_state=24)
train_df.reset_index(drop=True, inplace=True)
val_df.reset_index(drop=True, inplace=True)

print('TRAIN IMAGES:', train_df.shape[0])
print('VALIDATION IMAGES', val_df.shape[0])

# READ LABELS AND COUNT CLASSES
classes = open('classes.txt', 'r').read().split('\n')
classes.remove('')
train_count = {c: 0 for c in classes}
val_count = {c: 0 for c in classes}

def read_labels_and_count_bboxes(a, count):
    with open(a, 'r') as f:
        bboxes = f.read().split('\n')
        bboxes.remove('')
        bboxes = [bbox.split(' ') for bbox in bboxes]
        bboxes = [[int(c), float(x), float(y), float(w), float(h)] for c, x, y, w, h in bboxes]
        f.close()
    for c, x, y, w, h in bboxes:
        count[classes[c]] = count[classes[c]] + 1
    return bboxes

train_df['bbox'] = train_df['label'].apply(lambda a: read_labels_and_count_bboxes(a, train_count))
val_df['bbox'] = val_df['label'].apply(lambda a: read_labels_and_count_bboxes(a, val_count))

print('TRAIN CLASS COUNTS:', train_count)
print('VALIDATION CLASS COUNTS', val_count)

train_df = train_df.drop(columns=['bbox'])
val_df = val_df.drop(columns=['bbox'])
print(train_df.head())

# MOVE FILES TO RESPECTIVE FOLDER
def move_files(a, folder):
    os.rename(a, os.path.join(folder, os.path.basename(a)))
    return os.path.join(folder, os.path.basename(a))

train_df['image'] = train_df['image'].apply(lambda a: move_files(a, r'data\train\images'))
train_df['label'] = train_df['label'].apply(lambda a: move_files(a, r'data\train\labels'))
val_df['image'] = val_df['image'].apply(lambda a: move_files(a, r'data\val\images'))
val_df['label'] = val_df['label'].apply(lambda a: move_files(a, r'data\val\labels'))

# SAVE TRAINING AND TESTING DATAFRAMES
train_df.to_csv('train_df.csv', index=False)
val_df.to_csv('val_df.csv', index=False)

# REMOVE OLD DATAFRAME AND FOLDERS
os.remove('df.csv')
os.rmdir('Images')
os.rmdir('Labels')

print('CREATION OF YOLO V8 DATA DONE')
