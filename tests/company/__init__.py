from RACrawler.company import RACompany

company = RACompany(id="8861")
print(company.company_info)
print(company.marketplace_rankings())
print(company.company_complains())

for complain in company.all_company_complains:
    print(complain)