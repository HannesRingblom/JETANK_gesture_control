# JETANK Gesture Control

This project lets the user control a JETANK remotely using hand gestures and the video feed of the Jetson Nano. Using a computer connected to the same network as the Jetson, the JETANK interface can be connected to through its IP-adress. Jupyter there displays Notebooks possible to run and where the one of this project can be added. 

The notebook in this project uses a TCP socket hosted on the Jetson, making it possible for a client to connect and send command on how to steer the robot. Camera feed from the Jetson is also shown through the Notebook using a widget display.

## Table of Contents
    
    - Purpose of Project
    - Hardware Requirements
    - Setup / Software Requirements
    - Usage Instructions
    - Maintainers

## Purpose of Project

    Through the use of computer vision and machine learning, many interesting and important things can be 
    made and problems can be solved. This Project uses the computer vision of a Jetson Nano combined with
    Machine learning from Mediapipe. Mediapipe provides the possibility for gesture controlling and with 
    the Jetson Nano integrated in a JETANK the computer vision can be used in many ways. This Project was 
    done to highlight a certain way that these embedded solutions can be utilized, namely for remotely 
    control a robot from a distance. This could be especially helpful in places such as warehouses or in 
    places where the conditions might make it indurable for a human. The concept can also be used as a sort
    of helper robot for people with impaired movement, giving a interactive way of retrieving objects of 
    any kind. This project specifically uses quite simple commands and a limited robot to showcase the 
    potential use as well as the easy to learnand adapt concept.

## Hardware Requirements

    NVIDIA Jetson Nano Developer Kit
    JETANK AI Kit
    18650 Batteries (length less than 67mm)
    USB A to micro USB cable

## Setup / Software Requirements 
    
### JETANK:
    The following guide should be followed to assemble the Jetson Nano and JETANK
    https://www.youtube.com/watch?v=qNy1hulFk6I
    The guide also describes how to flash the required Jetbot image onto an SD card used for the project.
    
### Client computer: 
    The project was built and ran in Pycharm on the client side using the packages: 
    opencv-python and mediapipe that can be downloaded for the project interpreter
    
    Mediapipe documentation used in this project: https://google.github.io/mediapipe/solutions/hands.html 
## Usage Instructions
    
### JETANK: 
    - By following the guide in Setup, a wifi connection can be established. The IP-address of the Jetson Nano should then be displayed on the lcd. 
    - The guide further shows that having the client being connected to the same network enables easy access to the JETANK interface through entering its IP-adress     and port 8888 in a web browser.
    - With the interface open, upload the notebook 'jetank_side.ipynb' and run the cells to open the TCP socket and start the camera feed. (The last cell will stop     the camera) 
    
### Client PC:
    - Clone the project and open it in Pycharm, there in project settings download the packages opencv-python and mediapipe
    - Now make sure the IP-address stated in 'client_side.py' is that of the Jetson, with the same port as in 'jetank_side.ipynb'
    - Running this script when the JETANK server is running and connect to the server.
    - The camera for gesture commands should open, the JETANK is ready to be controlled.
    
### Commands:
    - The Program is controlled using thumb gestures by comparing the thumbs to the base of the palms.
    - One thumb up: Changes mode from moving to arm control or vice versa
    - Moving mode: 
        Two thumbs up: Move a short bit forward
        Two thumbs down: Move a short bit backwards
        Left thumb up, right thumb down: Turn right
        Right thumb up, left thumb down: Turn left
    - Arm control mode: 
        Two thumbs up: Move arm slightly forward/down
        Two thumbs down: Move arm slightly backwards/up
        Left thumb up, right thumb down: Move arm slightly forward/down
        Right thumb up, left thumb down: Move arm slightly backwards/up
        
Project video snapshot (video link: https://youtu.be/xWZBrWb5XTI)
![)](Example_image.JPG)

## Maintainers
    
[Hannes @HannesRingblom](https://github.com/HannesRingblom)
