#!bin/bash

dir="/home/dinab/Documents/rss_feed/paper-watch-dog-master/PaperWatchDog/files/"
general_seen="${dir}general_science_seen.log"
cscl_seen="${dir}cscl_seen.log"
explainability_seen="${dir}explainability_seen.log"

echo "Deleting log rss log files"
rm $general_seen $cscl_seen $explainability_seen
touch $general_seen $cscl_seen $explainability_seen

