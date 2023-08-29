@echo off
setlocal

call conda activate Yolov8Env

python Extract.py
python FilterFrames.py
jupyter nbconvert --execute --to notebook EDA.ipynb
set "AUGMENT=0"
if "%AUGMENT%" == "1" (
    python BalanceClasses.py
    python MergeAugment.py
)
python CreateYolov8Data.py
python TrainYolov8.py

call conda deactivate

endlocal
