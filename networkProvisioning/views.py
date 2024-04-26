import json
import pprint
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.http import HttpResponseNotAllowed, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from networkProvisioning.scripts.actions import show_version
from networkProvisioning.util import Util

from .models import SerialNumber, Router, Site, DeviceModel

import csv
from django.shortcuts import render
from .forms import UploadFileForm




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
                    if device.ztp_enable:
                        config = Util.build_configuration_alternate(device)
                    else:
                        config = 'Device not enabled for ZTP'
                else:
                    config = 'Device not found'
            else:
                config = 'No serial number provided'
            #AL: Trim leading whitespace
            #trimmed_conf = '\n'.join(line.lstrip() for line in config.splitlines())

            return HttpResponse(config, content_type='text/plain')
        else:
            return HttpResponseNotAllowed('Get Only')
    else:
        return HttpResponseForbidden('Nope, dont think so..')
"""
hostname,serial, model, loopback_ip,domain,site_name,template_name
router01, TEST123, C9500-40X, 192.168.1.1,example.com,Main Campus,Basic Setup
router02,TEST321, C9500-40X, 192.168.1.2,example.com,Remote Site,Advanced Setup
"""


def upload_router_data(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_in_memory = request.FILES['file'].read().decode('utf-8')
            reader = csv.reader(file_in_memory.splitlines())
            next(reader)  # Skip the header row

            #Iterate over all the rows in the CSV file (obviously :-)
            for row in reader:
                hostname, serial, model, loopback_ip, domain, site_name, template_name = row

                if Router.objects.filter(hostname=hostname).exists():
                    print(f"Router with hostname {hostname} already exists. Continuing to next row.")
                    continue
                if SerialNumber.objects.filter(number=serial).exists():
                    print(f"Serial number {serial} already exists. Continuing to next row.")
                    continue
                if not DeviceModel.objects.filter(part_number=model).exists():
                    print(f"Model {model} not found. Continuing to next row.")
                    continue
                if not Site.objects.filter(name=site_name).exists():
                    print(f"Site {site_name} not found. Adding")
                    
                    site = Site(name=site_name)
                    site.save()
                #if SerialNumber.objects.filter(number=serial).first().device_model:
                #    print("Serial number already assigned to a model. Continuing to next row.")

           

                site_obj = Site.objects.get(name=site_name)
                if not site_obj:
                    print("Site not found. Skipping row for now...")

                serial_obj = SerialNumber.objects.filter(number=serial).first()
                print(f"Serial number: {serial_obj}")

                if serial_obj:
                    print(f"Serial number {serial_obj} already exists.")

                    if not serial_obj.device_model:
                        print(f"Serial number {serial_obj} is not assigned to a model.")
                        continue
                    
                else:
                    print("Serial not found, as expected. Creating new serial number.")
                    print(f"Model from CSV:{model}")

                    model_obj = DeviceModel.objects.filter(part_number=model).first()

                    print(type(model_obj))

                    print (f"Model object: {model_obj}")
                    serial_obj = SerialNumber(number=serial, device_model=model_obj)

                    print (f"s  {serial_obj}")
                    if serial_obj:
                        print(f"Serial number created successfully. {serial_obj}")
                        serial_obj.save()
                    else:
                        print("Serial number not created.")

                print(f"Serial number object: {serial_obj}")
                router_obj = Router(
                    hostname=hostname,
                    loopback_ip=loopback_ip,
                    site=site_obj,
                    serial_number=serial_obj,

                )

                print (f"Router: {router_obj}")

                print (f"Rotuter model: {router_obj.serial_number.device_model}")
                router_obj.save()
                print(f"Router {hostname} added successfully.")
    



            return HttpResponse("File processed successfully")
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})