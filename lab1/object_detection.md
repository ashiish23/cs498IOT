# Setup for getting Object Detection running on your Raspberry Pi using Tensorflow v2 and Python 3
## Get the latest system packages
```
sudo apt-get update
sudo apt-get dist-upgrade
```
## Enable the Camera on your Pi by updating options for camera
```
sudo raspi-config
```
## Install requirements for OpenCV
```
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-100
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
```
## You can create a virtual environment for Python to isolate your packages but it's not necessary

## Install OpenCV via pip
```
pip3 install opencv-python
```
# Install requirements for TensorFlow v2
```
sudo apt-get install gfortran
sudo apt-get install libhdf5-dev libc-ares-dev libeigen3-dev
sudo apt-get install libatlas-base-dev libopenblas-dev libblas-dev
sudo apt-get install liblapack-dev cython
sudo pip3 install pybind11
sudo pip3 install h5py
sudo pip3 install --upgrade setuptools
pip3 install gdown
sudo cp /home/pi/.local/bin/gdown /usr/local/bin/gdown
gdown https://drive.google.com/uc?id=11mujzVaFqa7R1_lB7q0kVPW22Ol51MPg
```
# Install TensorFlow v2 using the the downloaded wheel
```
pip3 install tensorflow-2.2.0-cp37-cp37m-linux_armv7l.whl
```
## The download and installation for all the packages should take about 10-15 minutes

## Clone models repo from tensorflow
Within in the lab1 directory
```
git clone https://github.com/tensorflow/models.git
```
## Install Protobuf compiler for Raspberry Pi support
```
sudo apt-get install protobuf-compiler
```
## Compile Protos
```
cd models/research
protoc object_detection/protos/*.proto --python_out=.
```
## Update PYTHONPATH to import object_detection module or update ~/.bashrc with PYTHONPPATH to where /models/research is located
In models/research
```
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```
## Download a pre-trained TensorFlow model that works well on a Raspberry Pi
Within lab1 directory
```
wget http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz
tar -xzvf ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz
```
## Install matplotlib for labeling
```
pip3 install matplotlib
```
## Run the model by executing run_model.py script which is based on https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/TFLite_detection_webcam.py
It should take about 3-5 minutes before the camera feed appears. The model, labels, and threshold can be modified from the default if provided as args
```
python3 run_model.py
```
# Q&A - TBD
- Why are quantized models better for resource-constrained devices? 
- Would hardware acceleration help in image processing? Have the packages mentioned above leveraged it? If not, how could you properly leverage hardware acceleration?
- Would multithreading help increase (or hurt) the performance of your program?
- How would you choose the trade-off between frame rate and detection accuracy?
