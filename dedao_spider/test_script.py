from mitmproxy import ctx
import json

def response(flow):
    url = 'https://dedao.igetget.com/v3//discover/bookList'
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        books = data.get('c').get('list')
        for book in books:
            ctx.log.info(str(data))



