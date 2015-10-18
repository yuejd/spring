from django.shortcuts import render
from forests.models import Server
from django.views.generic import View


def server_list(request):
    servers = Server.objects.all()
    render_data = {
        'servers': servers
        }
    return render(request, "forests/server_list.html", render_data)


class ServerDetail(View):
	def get(self, request):
		# TODO add more code here
		return None

	def post(self, request):
		# TODO add more code here
		return None
