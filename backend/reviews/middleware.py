class StudentIdMiddleware:
    """Populates request.student_id for every request (dev stub)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.student_id = 1
        return self.get_response(request)
