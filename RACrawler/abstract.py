class RAAbstract(object):

    """
    Abstração das funções básicas para o Crawler
    """

    __user_agent = None
    from proxy_requests import ProxyRequests
    import json

    def get(self, url):
        headers = {"User-Agent": self.user_agent}

        req = self.ProxyRequests(url)
        req.set_headers(headers)
        req.get_with_headers()

        return self.json.loads(req.get_raw().decode())

    @property
    def user_agent(self) -> str:
        from fake_useragent import UserAgent

        if self.__user_agent is None:
            self.__user_agent = UserAgent().random

        return self.__user_agent