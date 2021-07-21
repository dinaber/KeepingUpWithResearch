
import os
import yaml


import time
import slackweb


class ConnectedPapers:
    def __init__(self, urls_display_name, webhook_url, files_dir_path=None):
        """
        Initializer of the WatchDog class

        Parameters
        ----------
        WEBHOOK URL: the url for the target slack channel (string)
                     To get the url, see https://api.slack.com/messaging/webhooks 
        """

        self.webhook_url = webhook_url
        if files_dir_path is None:
            self.files_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files')
        self.urls_display_path = os.path.join(self.files_dir_path, urls_display_name)
        self.attachments = [{
                                "color": "#0C5EF6",
                                "fields": [
                                    {
                                        "value": '*This is a monthly reminder to discover new papers related to our core in ConnectedPapers*',
                                        "short": False
                                    }]
                           }]

    def run(self):
        slack = slackweb.Slack(url=self.webhook_url)
        with open(self.urls_display_path , 'rb') as file:
            watch_list = yaml.load(file, Loader=yaml.FullLoader)
        for n, url_details in watch_list.items():
            name = url_details['name']
            author = url_details['author']
            url = url_details['url']
            self._arrange_attachment(name=name, author=author, url=url)
        slack.notify(attachments=self.attachments)

    def _arrange_attachment(self, name="", author="", url="", colour="#ffffff", thumbnail=""):
        self.attachments.append(
            {
                "fallback": "{name} {author}".format(name=name, author=author),
                "color": colour,
                "fields": [
                    {
                        "value": '*' + name + '*' + " (" + author + ")" + "\n" + url,
                        "short": False
                    }
                ],
                "image_url": "",
                "thumb_url": thumbnail
            })
