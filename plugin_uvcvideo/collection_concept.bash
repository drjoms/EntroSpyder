#!/bin/bash


if test -z $@ ; then 
echo no arguments given. give ammount of frames to analyse.
exit;
fi
webcamframes=$@
counter=0

echo this will collect $webcamframes frames from the camera
for ((i=0; i<$webcamframes; i++)); do
v4l2-ctl -d /dev/video0 --stream-mmap --stream-count=1 --stream-to=- | openssl dgst -blake2b512 - 
echo times done: $i

done
