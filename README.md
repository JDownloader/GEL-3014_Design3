GEL-3014_Design3
================

Description
-----------
...

Setup
-----
Be sure to have openCv 2.4.7 and numpy, also all this repository is tested with fedora 20 and nothing else
    $ yum install numpy opencv*
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
