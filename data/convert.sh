#!/bin/bash

for f in `ls raw`
do
	html2text raw/$f > text/${f:0:$((${#f}-5))}.txt
done
