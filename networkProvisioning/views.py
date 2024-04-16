import json

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from networkProvisioning.scripts.actions import show_version

# Create your views here.

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