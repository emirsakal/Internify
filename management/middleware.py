from django.shortcuts import redirect
from django.urls import reverse

class AuthRequiredMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if not request.user.is_authenticated and request.path != '/login/' and request.path != '/login/staff' and not request.path.startswith('/admin/'):
			return redirect('/login/')
		response = self.get_response(request)
		response['Content-Security-Policy'] = "frame-ancestors 'self' http://localhost"
		return response