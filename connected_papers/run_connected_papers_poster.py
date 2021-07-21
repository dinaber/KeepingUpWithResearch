import ConnectedPapers as cp
import argparse

parser = argparse.ArgumentParser(description='Process arguments for rss feed reader')
parser.add_argument("-wl", "--watch_list", dest='watch_list', help="give the name of the yml with the urls details",
                    action="store", default=None)
parser.add_argument("-whook", "--webhook", dest='webhook', help="give a webhook url to your slack channel",
                    action="store", default=None)

args = parser.parse_args()

connect = cp.ConnectedPapers(args.watch_list, args.webhook)

connect.run()
