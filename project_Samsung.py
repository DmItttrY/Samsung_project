# -*- coding: utf-8 -*-
"""training_samsung.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c-Oo6e9Y6lA4ecjocM5T8DSvCsA0HxOa
"""

#mount gdrive
from google.colab import drive
drive.mount('/content/drive')

#mount mdrive
!ln -s /content/drive/My\ Drive/ /mdrive

#test
!ls /mdrive/YoloV4

# clone darknet repo
!git clone https://github.com/AlexeyAB/darknet

# Commented out IPython magic to ensure Python compatibility.
# change makefile to have GPU and OPENCV enabled
# %cd darknet
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile
!sed -i 's/GPU=0/GPU=1/' Makefile
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile
!sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile

# verify CUDA
!/usr/local/cuda/bin/nvcc --version

# make darknet 
!make

# get yolov4 pretrained coco dataset weights
!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights

# Commented out IPython magic to ensure Python compatibility.
# define helper functions
def imShow(path):
  import cv2
  import matplotlib.pyplot as plt
#   %matplotlib inline

  image = cv2.imread(path)
  height, width = image.shape[:2]
  resized_image = cv2.resize(image,(3*width, 3*height), interpolation = cv2.INTER_CUBIC)

  fig = plt.gcf()
  fig.set_size_inches(18, 10)
  plt.axis("off")
  plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
  plt.show()

# use this to upload files
def upload():
  from google.colab import files
  uploaded = files.upload() 
  for name, data in uploaded.items():
    with open(name, 'wb') as f:
      f.write(data)
      print ('saved file', name)

# use this to download a file  
def download(path):
  from google.colab import files
  files.download(path)

# copy over both datasets into the root directory of the Colab VM
!cp /mdrive/YoloV4/obj.zip ../
!cp /mdrive/YoloV4/test.zip ../

# unzip the datasets and their contents so that they are now in /darknet/data/ folder
!unzip ../obj.zip -d data/
!unzip ../test.zip -d data/

# to download to local machine (change its name to yolov4-obj.cfg once you download)
download('cfg/yolov4-custom.cfg')

# upload the custom .cfg back to cloud VM from Google Drive
!cp /mdrive/YoloV4/yolov4-obj.cfg ./cfg

# upload the obj.names and obj.data files to cloud VM from Google Drive
!cp /mdrive/YoloV4/obj.names ./data
!cp /mdrive/YoloV4/obj.data  ./data

# upload the generate_train.py and generate_test.py script to cloud VM from Google Drive
!cp /mdrive/YoloV4/generate_train.py ./
!cp /mdrive/YoloV4/generate_test.py ./

!python generate_train.py
!python generate_test.py

# verify that the newly generated train.txt and test.txt can be seen in our darknet/data folder
!ls data/

!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137

"""# Learning"""

# train custom detector 
!./darknet detector train data/obj.data cfg/yolov4-obj.cfg yolov4.conv.137 -dont_show -map

# show chart.png of how custom object detector did with training
imShow('chart.png')

# kick off training from where it last saved
!./darknet detector train data/obj.data cfg/yolov4-obj.cfg /mdrive/YoloV4/backup/yolov4-obj_last.weights -dont_show

# Commented out IPython magic to ensure Python compatibility.
# set custom cfg to test mode 
# %cd cfg
!sed -i 's/batch=64/batch=1/' yolov4-obj.cfg
!sed -i 's/subdivisions=16/subdivisions=1/' yolov4-obj.cfg
# %cd ..

# run custom detector
!./darknet detector test data/obj.data cfg/yolov4-obj.cfg /mdrive/YoloV4/backup/yolov4-obj_last.weights /mdrive/YoloV4/test1.jpg -thresh 0.3
imShow('predictions.jpg')

# run custom detector
!./darknet detector test data/obj.data cfg/yolov4-obj.cfg /mdrive/YoloV4/backup/yolov4-obj_last.weights /mdrive/YoloV4/test2.jpg -thresh 0.3
imShow('predictions.jpg')

# run custom detector
!./darknet detector test data/obj.data cfg/yolov4-obj.cfg /mdrive/YoloV4/backup/yolov4-obj_last.weights /mdrive/YoloV4/test3.jpg -thresh 0.3
imShow('predictions.jpg')

!./darknet detector demo data/obj.data cfg/yolov4-obj.cfg /mdrive/YoloV4/backup/yolov4-obj_last.weights -dont_show /mdrive/YoloV4/test.mp4 -i 0 -out_filename /mdrive/YoloV4/results4.avi