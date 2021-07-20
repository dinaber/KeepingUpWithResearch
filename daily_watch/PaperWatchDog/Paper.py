import re


# Paper class
class Paper:

    def __init__(self, paper):
        """
        Extract the attributes of the paper from the RSS. 
        """
        isarXiv = False
        if paper.id.find("arxiv") >= 0:  # archive requires an exceptional parsing logics
            isarXiv = True
        if isarXiv:
            authors = [re.sub("<.+?>", "", a) for a in paper.author.split(", ")]
            self.author = authors[0]
            for i in range(1, len(authors)):
                self.author = "%s, %s" % (self.author, authors[i])

        else:
            if "authors" in paper:
                if len(paper.authors[0]) == 0:
                    self.author = "author unknown"
                else:
                    self.author = paper.authors[0]["name"]
                    for i in range(1, len(paper.authors)):
                        self.author = "%s, %s" % (self.author, paper.authors[i]["name"])
            else:
                self.author = "author unknown"
        try:
            self.summary = paper.summary
            if paper.id.find("medium") >= 0:
                if paper.title.find('Latest picks') < 0:
                    self.summary = re.findall(r'class="medium-feed-snippet">(.*?)</p>', paper.summary)[0]
            if paper.id.find("nature") >= 0:
                self.summary = re.findall(r'</a></p>(.*?)<img alt', paper.summary)[0]
            self.summary = self.summary.replace('<p>', '').replace('\n', ' ').replace('</p>', '')
        except:
            try:
                self.summary = paper.description
            except:
                self.summary = ' '
        try:
            self.url = paper.link
        except:
            self.url = paper.id
        self.title = re.sub(" \(arXiv:.+\)$", "", paper.title)

        self.author_info = {}
        self.attachments = []

    def print(self):
        print("{author} {title} {url}".format(author=self.author, title=self.title, url=self.url))

    def arrange_attachment(self, journal="", colour="#ffffff", thumbnail="", max_len=550):
        summary = self.smart_truncate(self.summary, max_len)
        self.attachments = [
            {
                "fallback": "{author} {title} {journal}".format(author=self.author, title=self.title, journal=journal),
                "color": colour,
                "fields": [
                    {
                        "value": journal + "\n" + '*' + self.title + '*' + "\n" + "[" + self.author + "]" + "\n" + summary + "\n" + self.url,
                        "short": False
                    }
                ],
                "image_url": "",
                "thumb_url": thumbnail
            }
        ]

    @staticmethod
    def smart_truncate(text, max_len):
        suffix = '...'
        if len(text) > max_len:
            p = re.compile(r"[?.!]")
            for m in p.finditer(text):
                if m.start() > max_len:
                    text = text[:m.start() + 1]
                    break
        if len(text) > max_len * 1.1:
            text = ' '.join(text[:max_len + 1].split(' ')[0:-1]) + suffix
        return text
