from django.shortcuts import render
from forests.models import Server, HBA, HbaPort, Switch, SwitchPort
from django.views.generic import View
from forests.lib import get_server_info, get_connection_info
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
    def _hba_sync(server):
        info_list = get_server_info(server)

        if not info_list:
            return False

        server.hba_set.all().delete()
        for hba_port_info in info_list:
            if hba_port_info.get('SerialNumber'):
                hba = HBA.objects.get_or_create(
                    serial_number=hba_port_info.get('SerialNumber'),
                    server=server)[0]
            else:
                hba = HBA.objects.get_or_create(
                    serial_number=hba_port_info.get('ModelDescription'),
                    server=server)[0]
            hba.description = hba_port_info.get('ModelDescription')
            hba.driver_name = hba_port_info.get('DriverName')
            hba.driver_version = hba_port_info.get('DriverVersion')
            hba.firmware_version = hba_port_info.get('FirmwareVersion')
            hba.model = hba_port_info.get('Model')
            hba.server = server
            hba.save()
            port = HbaPort.objects.get_or_create(
                wwpn=hba_port_info.get('WWPN'),
                hba_card=hba)[0]
            if hba_port_info.get('Active'):
                port.link_down = 0
            else:
                port.link_down = 1
            port.save()
            server.save()

        return True

    def _connection_sync(server):
        wwpns = []
        for port in HbaPort.objects.filter(hba_card__server=server):
            wwpns.append(port.wwpn)

        port_info_list = get_connection_info(wwpns)

        if not port_info_list:
            return False

        for port_info in port_info_list:
            switch = Switch.objects.get_or_create(
                ip_addr=port_info.get('SW_IP'),
                vf_vsan=port_info.get('VSAN'))[0]
            switch_port = SwitchPort.objects.get_or_create(
                port_index=port_info.get('Port'),
                switch=switch)[0]
            switch.save()
            switch_port.save()
            hba_port = HbaPort.objects.get(wwpn=port_info.get('WWPN'))
            hba_port.connection = switch_port
            hba_port.save()

        return True

    try:
        server = Server.objects.get(pk=server_id)
    except Server.DoesnotExist:
        return render(request, '404.html')

    if _hba_sync(server):
        _connection_sync(server)
        return JsonResponse({'updated': 'true'})
    else:
        return JsonResponse(
            {
                'updated': 'false',
                'message': 'Failed to get Server Information',
            }
        )
