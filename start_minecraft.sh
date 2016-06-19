#!/bin/bash

LOG_DIR="/tmp/minecraft";

today=`date +'%Y%m%d'`;
logfile=${LOG_DIR}/minecraft_${today}.log;
python_exec=$HOME/.virtualenvs/datascience/bin/python
python_script=$HOME/repos/datascience/automation/minecraft/minecraft.py
python_args="--start"

echo "${python_exec} ${python_script} ${python_args} >> ${logfile} 2>&1";
${python_exec} ${python_script} ${python_args} >>${logfile} 2>&1;
date;
