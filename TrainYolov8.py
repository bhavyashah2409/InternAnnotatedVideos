from ultralytics import YOLO

if __name__ == '__main__':
    model_type = 'yolov8m.pt'
    model = YOLO(model_type)
    model.train(data='custom_data.yaml', batch=4, workers=4, imgsz=640, epochs=500, name='yolov8m_500epochs', device=0, patience=50, verbose=True)
