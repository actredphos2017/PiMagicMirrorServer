# Pi Magic Mirror Server

> This project is designed for the [**Pi Magic Mirror**](https://github.com/actredphos2017/PiMagicMirror), and should be deployed together with it.

## Requirement

This Project recommended to be deployed on **Linux Platform** or other Unix-like os.

Ensure that a `python (3.9^)` with `pip` and `pipenv` is installed.

Most of the time you can use following shell script to install above.

``` sh
apt install python3 python3-pip
```

Ensure the following packages are installed:

```
libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 pulseaudio swig libatlas-base-dev libglib2.0-dev libbluetooth-dev
```

> You can use your any favorite package manager to install above packages.

Following requirements are only for test and not mandatory to be installed.

```
sox
```

## Deploy

### Directly or With Virtual Environment

Make sure your python version is at least **v3.9**:

``` sh
python --version
```

#### Clone the repository

Some of the requirements packages are not available in pip repository. So need to clone their repository and build ourselves.

``` sh
cd path/to/deploy/projects

git clone https://github.com/actredphos2017/PiMagicMirrorServer.git

# This repository's cloning just to build and install package "pybluez"
# You can remove after install
git clone https://github.com/pybluez/pybluez.git
```

#### Build and Install PyBluez

``` sh
cd pybluez

python setup.py install
pip list | grep PyBluez

cd ..
```

#### Install Other Packages

Install the requirement packages:

``` sh
cd PiMagicMirrorServer
pip install -r requirements.txt
```

Start the Server:

``` sh
python main.py
```
