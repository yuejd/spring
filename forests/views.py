from django.shortcuts import render
from forests.models import Server, HBA, HbaPort
from django.views.generic import View
from forests.lib import get_server_info
from django.http import JsonResponse


def server_list(request):
    servers = Server.objects.all()
    render_data = {
        'servers': servers
        }
    return render(request, "forests/server_list.html", render_data)


class ServerDetail(View):
    def get(self, request, server_id):
        try:
            server = Server.objects.get(pk=server_id)
        except Server.DoesnotExist:
            return render(request, '404.html')

        return render(
            request,
            "forests/server_detail.html",
            {'server': server}
            )

    def post(self, request):
        return None


def server_resync(request, server_id):
    def _sync(server, data):
        for hba_port_info in data:
            hba = HBA.objects.get_or_create(
                serial_number=hba_port_info['SerialNumber'],
                server=server)[0]
            hba.description = hba_port_info['ModelDescription']
            hba.driver_name = hba_port_info['DriverName']
            hba.driver_version = hba_port_info['DriverVersion']
            hba.firmware_version = hba_port_info['FirmwareVersion']
            hba.model = hba_port_info['Model']
            hba.server = server
            hba.save()
            port = HbaPort.objects.get_or_create(
                wwpn=hba_port_info['WWPN'],
                hba_card=hba)[0]
            if hba_port_info['Active']:
                port.link_down = 0
            else:
                port.link_down = 1
            port.save()
    try:
        server = Server.objects.get(pk=server_id)
    except Server.DoesnotExist:
        return render(request, '404.html')
    news = get_server_info(server)
    if news:
        # only one information object in the data returned
        _sync(server, news[0])
        return JsonResponse({'updated': 'true'})
    else:
        return JsonResponse({'updated': 'false'})
