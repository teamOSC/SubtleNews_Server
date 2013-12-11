#!/bin/bash

rm /home/sauravtom/public_html/subtlenews-log.txt
touch /home/sauravtom/public_html/subtlenews-log.txt

if [ -n "${FROMCRON}" ]
then
	echo "Run mode : CRON" >> /home/sauravtom/public_html/subtlenews-log.txt
else
	echo "Run mode : MANUAL" >> /home/sauravtom/public_html/subtlenews-log.txt
fi
DATE=$( TZ='Asia/Kolkata' date  +DATE:%F\ TIME:%T\(IST\) )
echo "Start $DATE" >> /home/sauravtom/public_html/subtlenews-log.txt
python /home/sauravtom/subtlenews/main.py >> /home/sauravtom/public_html/subtlenews-log.txt
DATE=$( TZ='Asia/Kolkata' date  +DATE:%F\ TIME:%T\(IST\) )
echo "End $DATE" >> /home/sauravtom/public_html/subtlenews-log.txt
