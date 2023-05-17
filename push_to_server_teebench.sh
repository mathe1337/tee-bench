#!/usr/bin/env bash
push_to_server() {
  cp .gitignore tmp_rsync_ignore
  echo "" >> tmp_rsync_ignore
  echo ".git" >> tmp_rsync_ignore
  echo "graphs" >> tmp_rsync_ignore
  echo "Paper" >> tmp_rsync_ignore
  echo "*.png" >> tmp_rsync_ignore
  echo "*.PNG" >> tmp_rsync_ignore
  echo "tmp_rsync_ignore" >> tmp_rsync_ignore
  for HOSTNAME in "$@"; do
    # push code
    echo "Pushing code to $HOSTNAME"
    rsync -rzvh --filter=':- tmp_rsync_ignore'  --progress . $HOSTNAME:~/tee-bench
  done;
  rm tmp_rsync_ignore
}

#####################################################################
## main script starts here
#####################################################################

#### Usage:
# invoke script and pass hostnames (as configured in your .ssh/config) as array to the script
# the script will copy the code to each server you pass as an argument
# e.g.: ./push_to_server node01 node02 node03
  
push_to_server "$@"
