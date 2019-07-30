#!/bin/bash

# Mount point of NFS export.
TARGDIR="/mnt/fs/smallfiles"
# All file sizes are in bytes.
MINFILESIZE=4096
MAXFILESIZE=131072

# ========== DO NOT CHANGE ANYTHING UNDER THIS LINE ========
RANGE=$(($MAXFILESIZE-$MINFILESIZE+1));

if [ $# -ne 1 ]
then
  echo "<Usage>: <$0> <Number of files to generate in $TARGDIR. File sizes between $MINFILESIZE and $MAXFILESIZE.>"
  exit
fi

numfiles=$1

i=0
while [ $i -lt $numfiles ]
do
  filesize=$RANDOM
  let "filesize %= $RANGE"
  let filesize=filesize+$MINFILESIZE
  if [ $(($i % 1000)) -eq 0 ]
  then
    echo "$i: $filesize"
    date
  fi
  head -c $filesize /dev/urandom > $TARGDIR/$i
  let i=i+1
done
