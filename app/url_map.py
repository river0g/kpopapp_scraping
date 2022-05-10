class Urls:
    def __init__(self, group_name):
        self.group_name = group_name
        self.kstyle = self.kstyle_url()
        self.kpopmonster = self.kpopmonster_url()

    def kstyle_url(self) -> str:
        url_list = {
            'blackpink': "https://news.kstyle.com/topicNews.ksn?topicNo=10584",  # blackpink
            'aespa': "https://news.kstyle.com/topicNews.ksn?topicNo=13161",  # aespa
            'ive': "https://news.kstyle.com/topicNews.ksn?topicNo=46748",  # ive
            'gi-dle': "https://news.kstyle.com/topicNews.ksn?topicNo=11382",  # gi-dle
            'kep1er': "https://news.kstyle.com/topicNews.ksn?topicNo=47400",  # kep1er
            'nmixx': "https://news.kstyle.com/topicNews.ksn?topicNo=99771",  # nmixx
        }

        return url_list[self.group_name]

    def kpopmonster_url(self) -> str:
        base_url = "https://www.kpopmonster.jp/"
        url = f'{base_url}?tag={self.group_name}'
        return url


if __name__ == '__main__':
    group_name = 'blackpink'
    urls = Urls(group_name)
    url_dict = urls.__dict__
    del url_dict['group_name']
    print(url_dict)

    print(list(url_dict.keys()))
