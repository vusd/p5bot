#!/bin/bash

# this is just an example wrapper which also handles logging

# here is an example crontab line
# 5 * * * * cd /develop/bots/p5bot && ./do_once.sh

PATH=$PATH:/usr/local/bin

echo "--> RUNNING "`date` >> run_log.txt

/usr/bin/unbuffer /usr/local/anaconda2/envs/p5bot/bin/python \
	tweet.py -s current/index.html --swaplist choice.json \
    >> run_log.txt 2>&1
