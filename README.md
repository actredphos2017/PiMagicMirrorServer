# Pi Magic Mirror Server

> This project is designed for the *Pi Magic Mirror*, and should be detected together with it.

## Requirement

This Project recommended to be deployed on **Linux Platform** or other Unix-like os.

Ensure that a `python (3.10^)` with `pip` and `pipenv` is installed.

Most of the time you can use following shell script to install above.

``` sh
apt install python3 python3-pip
pip install pipenv
apt install pipenv
```

Ensure the following packages are installed:

```
libasound-dev portaudio19-dev libportaudio2 libportaudocpp0 pulseaudio swig libatlas-base-dev libglib2.0-dev
```

> You can use your any favorite package manager to install above packages.

Following requirements are only for test and not mandatory to be installed.

```
sox
```

## Deploy

Navigate to the directory containing PiMagicMirrorServer and update dependencies using pipenv:

``` sh
cd path/to/PiMagicMirrorServer
pipenv update
```

If you encounter an error stating that pipenv cannot find the path to Python, configure it using:

``` sh
pipenv --python python3
pipenv update
```

Then use following command to activate the pipenv shell:

``` sh
pipenv shell
```

Start the server:

``` sh
python main.py
```