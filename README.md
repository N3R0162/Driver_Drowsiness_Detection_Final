# Driver Drowsiness Detection using Eye Landmarks

## Description
This application detects driver drowsiness based on the condition of their eyes. It utilizes eye landmarks to assess the level of drowsiness and provide alerts when necessary.

## Prerequisites
- Python 3.6 or higher
- pip (Python package installer)
- A virtual environment (recommended)
- c++ Build Tools (for building FaceBoxesV2)
- cuda (if using GPU acceleration)

## Auto Installation
The set up process can be done by running the following command after create a virtual environment:
```bash 
sh setup.sh
```
Or the manual installation can be done by following the steps below.

## Manual Installation
To install the required dependencies, use the following command:
```bash
pip3 install -r requirements.txt
```

#### FaceBoxesV2 build:
This project use FaceBoxV2 for detecting facial bounding box, in order for the app to run, first the FaceBoxV2 must be built:
- For Linux/MacOS:
```bash
cd ./FaceBoxesV2/utils/
sh make.sh
```

- For Windows:
```bash
cd ./FaceBoxesV2/utils/
python3 build.py build_ext --inplace
```

## Run:
To run the program, execute the following command:
```bash
streamlit run ./source/launcher.py
```

## License:
This project is licensed under the terms of the MIT License. See the LICENSE file for details.
