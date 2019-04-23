from RACrawler.abstract import RAAbstract


class RASearch(RAAbstract):
    from RACrawler import RA_SEARCH

    __response = None

    def __init__(self, query: str):
        from urllib.parse import quote
        from proxy_requests import ProxyRequests
        import json

        headers = {"User-Agent": self.user_agent}

        req = ProxyRequests(self.RA_SEARCH.format(quote(query.encode("utf-8"))))
        req.set_headers(headers)
        req.get_with_headers()

        self.__response = json.loads(req.get_raw().decode())

    @property
    def companies(self):
        data = self.__response
        for company in data.get("companies", []):
            yield self.__fix_company(company)

    def __fix_company(self, data: dict):

        def fix_company_index(index: str):
            data = {}
            index = index[1:-1]
            indexes = index.split(",")

            for indx in indexes:
                indx = str(indx).strip()
                vals = indx.split("=")
                data[vals[0]] = vals[1]

            return data

        data["companyIndex6Months"] = fix_company_index(data.get("companyIndex6Months", ""))

        return data


search = RASearch("Youse Caixa Seguradora")
for company in search.companies:
    print(company)
