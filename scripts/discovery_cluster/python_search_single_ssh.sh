#!/bin/bash
nodename=$1
corpus=$2
ssh $nodename 'bash -s' < python_search_single_ssh_python_run.sh $nodename $corpus