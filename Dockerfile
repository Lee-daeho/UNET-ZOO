From pytorch/pytorch:1.7.0-cuda11.0-cudnn8-runtime
MAINTAINER moon920110@gmail.com

RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y libsm6 libxext6 libxrender-dev libglvnd0 libgl1 libglx0 libegl1 libxext6 libx11-6 
RUN apt-get install -y imagemagick
RUN apt-get install -y git
RUN apt-get install -y mesa-utils libgl1-mesa-glx libgl1-mesa-dev
RUN apt-get install -y zlib1g-dev libjpeg-dev xvfb ffmpeg xorg-dev python-opengl libboost-all-dev libsdl2-dev swig

RUN pip install six
RUN pip install pyglet==1.5.0
RUN pip install scikit-learn
RUN pip install scikit-image
RUN pip install matplotlib
RUN pip install pygame
RUN pip install pandas
RUN pip install python-dotenv
RUN pip install easydict
RUN pip install pyyaml
RUN pip install gym-retro
RUN pip install opencv-python
RUN pip install tensorboard
RUN pip install tensorflow-gpu==2.4.0
RUN pip install tqdm
RUN pip install pillow
RUN pip install jupyter

RUN useradd -ms /bin/bash user

USER user

WORKDIR /workspace

EXPOSE 2375

#ENV DISPLAY :1
#CMD Xvfb :1 -screen 0 1024x768x24 -ac +extension GLX +render -noreset & export DISPLAY=:1
