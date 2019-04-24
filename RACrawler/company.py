from RACrawler.abstract import RAAbstract
from urllib.parse import quote


class InvalidCompanyIdentification(Exception):
    """
    Exception para uma identificação de empresa inválida
    """
    pass


class RACompany(RAAbstract):
    from RACrawler import RA_SHORT_NAME, RA_MARKETPLACE_RANKINGS, RA_COMPANY_COMPLAINS, RA_COMPLAIN_PUBLIC

    __short_name = ""
    __cid = ""
    __response = None

    # Thread Workers
    workers = 10

    def __init__(self, short: str = "", id: str = ""):
        """
        No init caso o usuário não passe ID vamos usar o Short-name para obter a id, e caso não
        passe o short-name usaremos a ID para identificar.
        :param short:
        :param id:
        """
        self.__short_name = short
        self.__cid = id

        if id:
            self.__short_name = self.company_complains(1).get("suggestion", {}).get("shortname", "")
            self.__short_call()
        elif short:
            self.__short_call()
            self.__cid = self.company_info.get("id", "")
        else:
            raise InvalidCompanyIdentification("You need provide short-name or company id")

    def __short_call(self):
        """
        Dados da empresa a partir do short-name
        :return:
        """
        self.__response = self.get(self.RA_SHORT_NAME.format(quote(self.__short_name.encode("utf-8"))))

    @property
    def company_info(self):
        return self.__response

    def marketplace_rankings(self, index=0, offset=9):
        return self.get(self.RA_MARKETPLACE_RANKINGS.format(self.__cid, index, offset))

    def company_complains(self, p1=10, p2=0):
        data = self.get(self.RA_COMPANY_COMPLAINS.format(self.__cid, p1, p2))
        return data

    def read_complain(self, complain_code: str):
        return self.get(self.RA_COMPLAIN_PUBLIC.format(complain_code))

    @property
    def all_company_complains(self):
        from concurrent.futures import ThreadPoolExecutor, as_completed
        data = self.company_complains()
        count = data.get("complainResult", {}).get("complains", {}).get("count", 0)
        yield data

        def counter(count):
            """
            Gerador de counter para paginação
            :param count:
            :return:
            """
            i = 0

            while i < count:
                i += 10

                if i > count:
                    i = count

                yield i

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {executor.submit(self.company_complains, 10, i): i for i in counter(count)}

            for future in as_completed(futures):
                yield {
                    "index": futures[future],
                    'count': count,
                    "data": future.result()
                }
