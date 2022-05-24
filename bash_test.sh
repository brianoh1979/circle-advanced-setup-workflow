#!/bin/bash
PR_NUM=${CIRCLE_PULL_REQUEST##*/}
echo $PR_NUM
if [ ! -z "$PR_NUM" ]
then
 echo '{ "EXEC_WF1": true }' >> /home/circleci/test.json
else
 echo '{ "EXEC_WF2": true }' >> /home/circleci/test.json
fi
