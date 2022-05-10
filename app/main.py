"""
main.py でやりたいこと
スクレイピングする各サイトに対して更新があるか確認。(この時点でスクレイピングする)
あれば記事を取得して、apiにPOST
なければそのまま終了。
"""
from datetime import datetime, timedelta
from typing import List

from app.scraping import scrape_page
from app.post_data import post_data

from app.send_mail import send_mail

from app.url_map import Urls
from app.parser_map import soup_parser


def get_data(url, parser, group_name):
    """引数に渡されたページをスクレイピングして個々の記事を解析してdictにしたあと、まとめてリストにする。

    Parameters
    ----------
    url : str
        スクレイピング対象のURL
    parse_func : callback function
        bs4オブジェクトをdictに変換する関数。
        なにも処理せずそのままbs4オブジェクトを返したいなら以下を引数にする。
        lambda soup: soup

    Returns
    -------
    aricles : List[dict]
    """
    # スクレイピングして記事を取得&整形する。
    articles = scrape_page(url, parser, group_name)

    print("articles:", articles)
    return articles


# 記事の重複をなくす
def deduplicate(results: List[dict]) -> List[dict]:
    filtered_results_all = []
    article_title_set = set()
    for result in results:
        if not result['title'] in article_title_set:
            filtered_results_all.append(result)
            article_title_set.add(result['title'])
        else:
            for filtered_dic in filtered_results_all:
                if filtered_dic['title'] == result['title']:
                    filtered_dic['group'].append(result['group'][0])
                    filtered_dic['group_id'].append(result['group_id'][0])

    return filtered_results_all


def handler(args, context):
    groups = ['blackpink', 'aespa', 'ive', 'gi-dle', 'kep1er', 'nmixx']
    description = 'default message'
    results = []
    try:
        # n=site_num, m=group_num
        # O(n)*O(m)
        # グループごとにLoop
        for group in groups:
            print('group: ', group)
            urls = Urls(group)
            urls_instance_value: dict = urls.__dict__
            del urls_instance_value['group_name']

            # siteごとにLoop
            for site, url in urls_instance_value.items():
                print("site:", site, "  url:", url)
                parser = soup_parser(site)
                result: List[dict] = get_data(url, parser, group)
                if len(result) > 0:
                    for r in result:
                        results.append(r)

            print('\n')

        # 同記事複数グループのタグがある記事もあるので、それもフィルタリングする。
        # 一つの記事にA,Bというグループタグがあったときに2回同じ記事をリストに入れないようにする。
        filtered_results = deduplicate(results)
        print(filtered_results)
        print('記事数', len(filtered_results))

        description = 'success!'

        # APIに送信する。
        post_data(filtered_results)

        # 結果をメールで送信
        print(description)
        send_mail(title='scraping and API post result',
                  description=description)

    except Exception as e:
        print(e)
        description = str(e)
    return {
        "message": "success!"
    }


# handler('a', 'a')
"""
herokuがインシデントを起こしたので、これからのスクレイピング＋定期実行の不具合への対処、対策
・ heroku → aws lambdaに移行
・ 障害発生時に取得できなかった記事を取得しmonogodbにinsertするプログラムを書く。
    不具合の旨を記載したメールかLINEを自分に送信。
    手動でスクレイピング、アップロード ← このプログラムを書くのが優先。(日付指定で取得できればいいかな。)


コレを機会にmongodbとDjangoを連携させるかなぁ。。。。→ やめました
    mongodbへの接続をサポートしてるdjongoの動作がよくわからない。
"""
