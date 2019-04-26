from RACrawler.search import RASearch

search = RASearch(query="Bradesco")

for company in search.companies:
    print(company)