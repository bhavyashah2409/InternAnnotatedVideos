@echo off
setlocal

call conda activate Yolov8Env

python ExtractFromZip.py
jupyter nbconvert --execute --to pdf EDA.ipynb
set "AUGMENT=0"
if %AUGMENT% == "1"
(
    python BalanceClasses.py
    python MergeAugment.py
)
python CreateYolov8Data.py
python TrainYolov8.py

endlocal
