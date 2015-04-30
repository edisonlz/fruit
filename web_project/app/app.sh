#!/bin/bash

PROJDIR="/opt/app/python/m-cms-new/app"
PIDFILE="$PROJDIR/app.cms.new.pid"
ERRORLOG="/opt/logs/cms_error.log"
OUTLOG="/opt/logs/cms_std_out.log"
APP_EXEC="python manage.py runfcgi method=prefork daemonize=true host=127.0.0.1"
NUM_PROC=21005
NUM_PROCS=200
MIN_SPARE=20
MAX_SPARE=50

cd $PROJDIR


function start_server() {
    cd $PROJDIR
    ulimit -n 65535
    $APP_EXEC port=$NUM_PROC minspare=$MIN_SPARE maxspare=$MAX_SPARE maxchildren=$NUM_PROCS  outlog=$OUTLOG errlog=$ERRORLOG
}

function stop_server() {
    ps aux | grep "$APP_EXEC" | grep "$NUM_PROC" | awk '{print $2}' | xargs kill -9
}

case "$1" in
start)
    start_server
;;
stop)
    stop_server
;;
restart)
    stop_server
    start_server
;;
*)
    echo 'Usage: app.sh [start|stop|restart]'
esac

