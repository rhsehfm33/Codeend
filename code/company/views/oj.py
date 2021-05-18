from utils.api import APIView

from company.models import Company

class CompanyAPI(APIView):
    def post(self, request):
        data = request.data
        try:
            Company.objects.create(name=data["name"],
                                    number_of_workers=data["number_of_workers"],
                                    salary_man=data["salary_man"])
        except Exception as e:
            return self.error("company creation fail")

        return self.success()
        
    def get(self, request):
        company_name = request.GET.get("name")
        if Company.objects.filter(name=company_name).exists():
            company = Company.objects.get(name=company_name)
            return self.success()
        else:
            return self.error("Account not found")