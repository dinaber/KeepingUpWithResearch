import PaperWatchDog as pwd
import argparse

parser = argparse.ArgumentParser(description='Process arguments for rss feed reader')
parser.add_argument("-sf", "--seen_files", dest='seen_files', help="give a path to a log with all the previously seen files",
                    action="store", default=None)
parser.add_argument("-wl", "--watch_list", dest='watch_list', help="give a path to a py file with the journals watch list",
                    action="store", default=None)
parser.add_argument("-fkeys", "--filter_keys", dest='filter_keys', help="give a path to a txt with all the words that are used for filtration",
                    action="store", default=None)
parser.add_argument("-whook", "--webhook", dest='webhook', help="give a webhook url to your slack channel",
                    action="store", default=None)

args = parser.parse_args()

dog = pwd.WatchDog(args.seen_files, args.webhook)

dog.run(args.watch_list, args.filter_keys)
