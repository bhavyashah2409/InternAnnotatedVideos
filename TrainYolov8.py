from ultralytics import YOLO

if __name__ == '__main__':
    print('TRAINING YOLO V8 STARTED')
    model_type = 'yolov8m.pt'
    model = YOLO(model_type)
    model.train(data='custom_data.yaml', batch=2, workers=2, imgsz=640, epochs=500, name='yolov8m_500epochs', device=0, patience=50, verbose=True)
    print('TRAINING YOLO V8 DONE')
