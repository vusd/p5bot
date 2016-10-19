#!/bin/bash

# this is just an example wrapper which also handles logging

# here is an example crontab line
# 5 * * * * cd /develop/bots/p5bot && ./do_once.sh

# phantomjs needs to be in path
PATH=$PATH:/usr/local/bin

echo "--> RUNNING "`date` >> run_log.txt

/usr/bin/unbuffer /usr/local/anaconda2/envs/p5bot/bin/python \
	tweet.py -t 60 -s current --swaplist choice.json \
    >> run_log.txt 2>&1

# check exit code, rerun if timeout
rc=$?; if [[ $rc != 0 ]]; then
  echo "RERUNNING FROM TIMEOUT" >> run_log.txt
  /usr/bin/unbuffer /usr/local/anaconda2/envs/p5bot/bin/python \
	tweet.py -t 60 -s current \
    >> run_log.txt 2>&1
fi
