#!/bin/bash

# this is just an example wrapper which also handles logging

# here is an example crontab line
# 5 * * * * cd /develop/bots/p5bot && ./do_once.sh

SLUG=${1:-"ben"}
RUNDIR=current_"$SLUG"
SWAPLIST=choice_"$SLUG".json
CREDS=creds_"$SLUG".json
DATE=`date +%Y_%m_%d`
LOGFILE=logs/"$SLUG"_"$DATE".txt

# phantomjs needs to be in path
PATH=$PATH:/usr/local/bin

echo "--> RUNNING "`date` >> $LOGFILE

/usr/bin/unbuffer /usr/local/anaconda2/envs/p5bot/bin/python \
        tweet.py -s $RUNDIR --swaplist $SWAPLIST \
        --noname --creds $CREDS \
    >> $LOGFILE 2>&1

# check exit code, rerun if timeout
rc=$?; if [[ $rc != 0 ]]; then
  echo "RERUNNING FROM TIMEOUT" >> $LOGFILE
  /usr/bin/unbuffer /usr/local/anaconda2/envs/p5bot/bin/python \
        tweet.py -s $RUNDIR \
        -t 900 \
        --noname --creds $CREDS \
    >> $LOGFILE 2>&1
fi
