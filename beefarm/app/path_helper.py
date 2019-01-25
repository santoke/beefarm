from app.config import Config

class PathHelper():
    language = 'en'

    def __init__(self, language):
        self.language = language

    # 링크 url에 언어 접미사를 붙여준다
    def make_sub_path(self, url):
        if url[:2] == './': # 링크가 현재 페이지인경우
            return url[2:]

        if url[:4] == f'/{self.language}/':
            return url

        return f'/{self.language}/' + url

    # 프록시 URL이 있는 경우 proxy 주소를 조합한 주소를 전달
    def page_url(self, url):
        return Config.d['proxy'] + Config.d['domain'] + self.make_sub_uri(url)