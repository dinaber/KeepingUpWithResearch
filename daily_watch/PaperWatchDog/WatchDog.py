# Written by Sadamori Kojaku and modified by Dina Berenbaum
# References:
# https://qiita.com/TatsuyaMizuguchi17/items/35dd3dd1396864006031
# https://github.com/dinaber/KeepingUpWithResearch

from .Paper import Paper
import os
import yaml

import feedparser
import time
import slackweb


class WatchDog:
    def __init__(self, seen_files_name, webhook_url, files_dir_path=None):
        """
        Initializer of the WatchDog class

        Parameters
        ----------
        WEBHOOK URL: the url for the target slack channel (string)
                     To get the url, see https://api.slack.com/messaging/webhooks 
        """
        self.webhook_url = webhook_url
        self.seen_files_name = "paper-watch-dog.log"
        if seen_files_name is not None:
            self.seen_files_name = seen_files_name  # Intermediately file
        if files_dir_path is None:
            self.files_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files')

        self.seen_files_path = os.path.join(self.files_dir_path, self.seen_files_name)

    def run(self, watch_list_file_name, filter_keys_file_name=None):
        """
        Check the RSS and send the update to your slack channel.

        Parameters
        ----------
        :param watch_list_file_name: The name of the file holding watch_list
            watch_list is a list of dictionaries composed of following pairs of keys and values:
                - "url": The URL for the RSS feed. 
                - "journal": Name of journals. The name will be appeared in the slack channel.
                - "color": Hex code. The colour will be used for decolating the post.
                - "thumb": URL for the thumbnail. The picture will be shown with the post.
                The example of watch_list is included in the package (PaperWatchDog/watch_list.py)
        :param filter_keys_file_name: The name of the file holding the words to filter by
        :param max_url_log: the maximum urls saved in the log file, more than that will be truncated from the head
        """
        if os.path.exists(self.seen_files_path):
            url_registered = [line.rstrip('\n') for line in open(self.seen_files_path)]
        else:
            url_registered = []
        file_registered_url = open(self.seen_files_path, "a")
        slack = slackweb.Slack(url=self.webhook_url)
        if watch_list_file_name is None:
            watch_list_file_name = 'watch_list.py'
        watch_list_path = os.path.join(self.files_dir_path, watch_list_file_name)
        with open(watch_list_path, 'rb') as file:
            watch_list = yaml.load(file, Loader=yaml.FullLoader)
        if filter_keys_file_name is not None:
            filter_keys_path = os.path.join(self.files_dir_path, filter_keys_file_name)
            with open(filter_keys_path) as fk_file:
                fk_list = fk_file.readlines()
                fk_list = [line.rstrip('\n') for line in fk_list]
                fk_list_out, fk_list_in = [], []
                for fk in fk_list:
                    if fk[0] == '-':
                        fk_list_out.append(fk[1:])
                    elif fk[0] == '+':
                        fk_list_in.append(fk[1:])
        for n, dict_journal in watch_list.items():
            name = dict_journal["journal"]
            url_q = dict_journal["url"]
            col = dict_journal["colour"]
            thumb = dict_journal["thumb"]
            max_len = dict_journal["max_len"]
            max_msg = dict_journal["max_msg"]
            rss = feedparser.parse(url_q)
            if len(rss.entries) <= 1:
                break
            num = 0
            for one_paper in rss.entries:
                send = True
                try:
                    paper = Paper(one_paper)
                    if paper.url in url_registered:
                        continue
                    if filter_keys_file_name is not None:
                        ltitle = paper.title.lower()
                        if (not any([ltitle.rfind(k) >= 0 for k in fk_list_in]) and fk_list_in) or any(
                                [ltitle.rfind(k) >= 0 for k in fk_list_out]):
                            send = False
                    if send:
                        num += 1
                        paper.arrange_attachment(journal=name, colour=col, thumbnail=thumb, max_len=max_len)
                        attachments = paper.attachments.copy()
                        slack.notify(attachments=attachments)
                    # Save
                    file_registered_url.write("\n" + paper.url)
                    url_registered.append(paper.url)
                except:
                    break
                if num >= max_msg:
                    break
                time.sleep(1.2)
        file_registered_url.close()
