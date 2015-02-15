GEL-3014_Design3
================

Description
-----------
...

Setup
-----
Be sure to have openCv 2.4.10, openNI and numpy, also all this repository is tested with fedora 20 and nothing else.
    
    $ yum install numpy
    
    $ git clone -b unstable https://github.com/OpenNI/OpenNI.git OpenNI_install
    $ cd OpenNI_install/Platform/Linux/CreateRedist
    $ ./RedistMaker # Sur ArchLinux, il faut d'abord modifier « python » pour « python2 » dans ce fichier
    $ cd ../Redist/OpenNI-Bin-Dev-Linux-x64-v1.5.8.5 # Le chemin variera selon votre architecture, x86 ou x64
    $ sudo ./install.sh
    $ cd
    $ git clone -b unstable https://github.com/ph4m/SensorKinect.git KinectDriver
    $ cd KinectDriver/Platform/Linux/CreateRedist
    $ ./RedistMaker # Peut prendre un certain temps
    $ cd ../Redist/Sensor-Bin-Linux-x64-v5.1.2.1 # Le chemin variera selon votre architecture, x86 ou x64
    $ sudo ./install.sh
    
    $ wget http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.10/opencv-2.4.10.zip?r=http%3A%2F%2Fopencv.org%2Fdownloads.html&ts=1423634867&use_mirror=hivelocity
    $ unzip opencv-2.4.10.zip
    $ cd opencv-2.4.10/
    $ mkdir build && cd build
    $ cmake .. -DWITH_OPENNI=ON
    # Vous pouvez vous assurer que la configuration est correcte en vérifiant si les lignes
    # OpenNI : YES (ver 1.5.8, build 5)
    # et OpenNI PrimeSensor Modules : YES # (/usr/lib/libXnCore.so)
    # sont présentes
    # Si vous souhaitez utiliser Python, vous pouvez également vous assurer que la
    # configuration est correcte en observant si les lignes suivantes sont présentes (peut légèrement différer)
    # -- Python:
    # -- Interpreter: /usr/bin/python2 (ver 2.7.5)
    # -- Libraries: /usr/lib/x86_64-linux-gnu/libpython2.7.so (ver 2.7.5+)
    # -- numpy: /usr/lib/python2.7/dist-packages/numpy/core/include (ver 1.7.1)
    $ make -j 2 # Ajustez le chiffre selon le nombre de cœurs de votre ordinateur et patientez, ce sera long!
    $ sudo make install
    # Credit at Marc-André Gardner and Yannick Hold-Geoffroy for those instructions

Setup your virtualenv before touching anything:

    $ cd <the-projet-folder>
    $ virtualenv  --no-site-packages env
    $ //On mac or linux
    $ source env/bin/activate
    $ //On windows
    $ env/Scripts/activate.bat
    
    for more information, refer here: http://docs.python-guide.org/en/latest/dev/virtualenvs/
    

Usage
-----
    $ python setup.py install
    
Run project
-----------
    $ python sample

Run tests
---------
    $ python setup.py test
