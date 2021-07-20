#!/bin/bash

conda activate rss_feed

python full/path/to/run_rss_reader.py -sf explainability_seen.log -wl explainability_watch_list.yml -fkeys explainability_filter_keys.txt -whook <webhook_url>

conda deactivate
