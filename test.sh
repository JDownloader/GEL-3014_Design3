# /bin/bash
rm -drf GEL*
rm -drf env/lib/python2.7/site-packages/GEL*
curl http://127.0.0.1:8000/start
curl http://127.0.0.1:8001/
