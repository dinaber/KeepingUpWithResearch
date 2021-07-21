#!/bin/bash
conda activate rss_feed

python ~/full/path/to/connected_papers/run_connected_papers_poster.py -wl urls_to_follow.yml -whook <webhook_url>

conda deactivate
