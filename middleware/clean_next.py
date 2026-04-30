# middleware/clean_next.py
from urllib.parse import unquote

class CleanNextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        next_param = request.GET.get('next')
        if next_param:
            for _ in range(10):
                new = unquote(next_param)
                if new == next_param:
                    break
                next_param = new
            if 'next=' in next_param or '/login' in next_param:
                request.GET = request.GET.copy()
                request.GET['next'] = ''
        return self.get_response(request)
