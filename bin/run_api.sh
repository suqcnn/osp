# /bin/bash

wsgi_name=wsgi
if [[ $# -ge 1 ]]; then
    if [[ $1 != 'pro' ]] && [[ $1 != 'pre' ]] && [[ $1 != 'test' ]] && [[ $1 != 'dev' ]]; then
        echo 'usage: ./run_api.sh [pro|pre|dev|test]'
    fi
    if [[ $1 == 'dev' ]]; then
        wsgi_name=wsgi_dev
    fi
    if [[ $1 == 'pre' ]]; then
        wsgi_name=wsgi_pre
    fi
    if [[ $1 == 'pro' ]]; then
        wsgi_name=wsgi_pro
    fi
fi

wsgi_path=`dirname $0`/../osp
cd ${wsgi_path} && gunicorn -w 4 --threads 1 -b 0.0.0.0:80 ${wsgi_name}:application
