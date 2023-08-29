import cv2 as cv

for i in range(1, 43):
    v = cv.VideoCapture(fr'C:\Users\aicpl\ShipsDatasets\VideoDataset\videos\video_{i}.mp4')
    print(i, v.get(cv.CAP_PROP_FPS), v.get(cv.CAP_PROP_FRAME_COUNT) / v.get(cv.CAP_PROP_FPS))
