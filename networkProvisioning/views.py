import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.http import HttpResponseNotAllowed, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from networkProvisioning.scripts.actions import show_version
from networkProvisioning.util import Util

from .models import SerialNumber, Router

@csrf_exempt
def actions(request):
    actions_dict = {
        'showVersion': show_version
    }
    if request.user.is_authenticated:
        if request.method == 'POST':
            params = json.loads(request.body.decode('utf-8'))
            action = params.get('action')
            args = params.get('args')
            result = actions_dict.get(action)(*args)
            return JsonResponse({'result': result})
        else:
            return HttpResponseNotAllowed('Post Only')
    else:
        return HttpResponseForbidden('Nope, dont think so..')

def getConfig(request):
    if request.user.is_authenticated or settings.DEBUG:
        if request.method == 'GET':
            #AL: Temp PoC to generate config until UUID endpoint is implemented
            config = ""
            if 'sn' in request.GET:
                serial_number = request.GET['sn']
                device = Router.objects.filter(serial_number__number=serial_number).first()
                print(type(device))
                if device:
                    config = Util.build_configuration(device)
                else:
                    config = 'Device not found'
            else:
                config = 'No serial number provided'
            #AL: Trim leading whitespace
            trimmed_conf = '\n'.join(line.lstrip() for line in config.splitlines())

            return HttpResponse(trimmed_conf, content_type='text/plain')
        else:
            return HttpResponseNotAllowed('Get Only')
    else:
        return HttpResponseForbidden('Nope, dont think so..')