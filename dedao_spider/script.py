import json
import pymongo
from mitmproxy import ctx
from urllib.parse import unquote

def response(flow):
    client = pymongo.MongoClient('localhost')
    db = client['igetget']
    collection = db['books']
    url = 'https://dedao.igetget.com/v3//discover/bookList'
    if flow.request.url.startswith(url):
        text = flow.response.text
        print(text)
        # 返回的结果是json格式
        data = json.loads(text)
        print(data)
        books = data.get('c').get('list')
        for book in books:
            # 部分内容使用quote转化了
            data = {
                'title': unquote(book.get('operating_title')),
                'cover': unquote(book.get('cover')),
                'summary': unquote(book.get('other_share_summary')),
                'price': book.get('price')
            }
            ctx.log.info(str(data))
            collection.insert(data)