class HealthHandler:

    @staticmethod
    def handle(request):
        return 200 ,{
            "Status": "UP",
            "Message": "Complaint Management System is running"
        }