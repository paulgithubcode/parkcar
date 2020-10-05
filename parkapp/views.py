from django.shortcuts import render
from django.utils.translation import ugettext as _
import types
import datetime
import time
import json
from django.views.decorators.csrf import csrf_exempt
from parkapp.models import *
from django.contrib.sites.models import Site
from django.http import HttpResponse

def park(request):
    req_plate_number = request.GET.get('plate_number')
    req_park_name = request.GET.get('park_name')
    response_data = {}
    response_data['code'] = 0
    response_data['message'] = ""
    response_data['data'] = {}

    if(accessed(request) > 10):
        response_data['code'] = 200
        response_data['message'] = "Your Acccess more than 10 request in 10 second"
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    rs_park = Park.objects.get_or_create(name=req_park_name)

    rs_parking_ticket_check_max = ParkingTicket.objects.filter(
        park_id=rs_park[0].id)
    if rs_parking_ticket_check_max.count() >= rs_park[0].maximum_no_cars:
        response_data['code'] = 200
        response_data['message'] = "Park "+rs_park[0].name+' has already full with '+str(rs_park[0].maximum_no_cars)+' cars'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    rs_parking_ticket_check = ParkingTicket.objects.filter(
        plate_number=req_plate_number,
        park_id=rs_park[0].id)
    if rs_parking_ticket_check.count() > 0:
        if rs_parking_ticket_check[0].exit_time != None or rs_parking_ticket_check[0].status == 'exited':
            rs_parking_ticket_check.update(entry_time=datetime.datetime.now(), exit_time=None, status='parked')
            response_data['code'] = 200
            response_data['message'] = "Car plate Number " + req_plate_number + ' entered parking area at ' + str(
                rs_parking_ticket_check[0].entry_time)
        else:
            response_data['code'] = 200
            response_data['message'] = "Car plate Number "+req_plate_number+' has already parked at '+str(rs_parking_ticket_check[0].entry_time)
    else:
        rs_parking_ticket = ParkingTicket(
            plate_number=req_plate_number,
            park_id=rs_park[0].id,
            exit_time=None,
            status='parked')
        rs_parking_ticket.save()
        response_data['code'] = 200
        response_data['message'] = "Car plate Number "+req_plate_number+' entered parking area at '+str(rs_parking_ticket.entry_time)
    response_data['data']['parking_ticket_id'] = rs_parking_ticket_check[0].id
    response_data['data']['plate_number'] = rs_parking_ticket_check[0].plate_number
    response_data['data']['entry_time'] = str(rs_parking_ticket_check[0].entry_time)
    response_data['data']['exit_time'] = str(rs_parking_ticket_check[0].exit_time)
    response_data['data']['fee_paid'] = rs_parking_ticket_check[0].fee_paid
    response_data['data']['status'] = rs_parking_ticket_check[0].status
    response_data['data']['park_id'] = rs_parking_ticket_check[0].park_id
    response_data['data']['park_name'] = rs_park[0].name
    response_data['data']['maximum_no_cars'] = rs_park[0].maximum_no_cars

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def unpark(request):
    req_plate_number = request.GET.get('plate_number')
    response_data = {}
    response_data['code'] = 0
    response_data['message'] = ""
    response_data['data'] = {}

    if(accessed(request) > 10):
        response_data['code'] = 200
        response_data['message'] = "Your Acccess more than 10 request in 10 second"
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    rs_parking_ticket_check = ParkingTicket.objects.filter(
        plate_number=req_plate_number,
        status='parked',
        exit_time=None)
    if rs_parking_ticket_check.count() == 0:
        response_data['code'] = 200
        response_data['message'] = "Car with Plate number : "+req_plate_number+' is not parked'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    ParkingTicket.objects.filter(
        plate_number=req_plate_number,
        status='parked',
        exit_time=None
    ).update(
        exit_time=datetime.datetime.now(),
        status='exited'
    )
    rs_parking_ticket_check = ParkingTicket.objects.filter(
        plate_number=req_plate_number)
    rs_park = Park.objects.filter(id=rs_parking_ticket_check[0].park_id)
    response_data['code'] = 200
    response_data['message'] = "Car plate Number " + req_plate_number + ' exit from parking '+rs_park[0].name+' area at ' + str(
        rs_parking_ticket_check[0].exit_time)
    response_data['data']['parking_ticket_id'] = rs_parking_ticket_check[0].id
    response_data['data']['plate_number'] = rs_parking_ticket_check[0].plate_number
    response_data['data']['entry_time'] = str(rs_parking_ticket_check[0].entry_time)
    response_data['data']['exit_time'] = str(rs_parking_ticket_check[0].exit_time)
    response_data['data']['fee_paid'] = rs_parking_ticket_check[0].fee_paid
    response_data['data']['status'] = rs_parking_ticket_check[0].status
    response_data['data']['park_id'] = rs_parking_ticket_check[0].park_id
    response_data['data']['park_name'] = rs_park[0].name
    response_data['data']['maximum_no_cars'] = rs_park[0].maximum_no_cars
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_car_information(request):
    req_plate_number = request.GET.get('plate_number')
    response_data = {}
    response_data['code'] = 0
    response_data['message'] = ""
    response_data['data'] = []

    if(accessed(request) > 10):
        response_data['code'] = 200
        response_data['message'] = "Your Acccess more than 10 request in 10 second"
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    rs_parking_ticket_check = ParkingTicket.objects.filter(
        plate_number=req_plate_number)
#    rs_park = Park.objects.filter(id=rs_parking_ticket_check[0].park_id)
    response_data['code'] = 200
    response_data['message'] = "Car plate Number " + req_plate_number + " informations"

    for result in rs_parking_ticket_check:
        fields = {}
        fields["parking_ticket_id"] = str(result.id)
        fields["plate_number"] = str(result.plate_number)
        fields["entry_time"] = str(result.entry_time)
        fields["exit_time"] = str(result.exit_time)
        fields["fee_paid"] = str(result.fee_paid)
        fields["park_id"] = str(result.park_id)
        rs_park = Park.objects.filter(id=result.park_id)
        fields['park_name'] = rs_park[0].name
        fields['maximum_no_cars'] = rs_park[0].maximum_no_cars
        response_data['data'].append(fields)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_slot_information(request):
    req_park_name = request.GET.get('park_name')
    response_data = {}
    response_data['code'] = 0
    response_data['message'] = ""
    response_data['data'] = {}

    if(accessed(request) > 10):
        response_data['code'] = 200
        response_data['message'] = "Your Acccess more than 10 request in 10 second"
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    rs_park = Park.objects.filter(
        name=req_park_name)
    response_data['code'] = 200
    response_data['message'] = "Park information " + req_park_name
    response_data['data']['park_id'] = rs_park[0].id
    response_data['data']['park_name'] = rs_park[0].name
    response_data['data']['maximum_no_cars'] = rs_park[0].maximum_no_cars
    rs_parking_ticket_check_max = ParkingTicket.objects.filter(
        park_id=rs_park[0].id)
    response_data['data']['available_space_for_cars'] = rs_park[0].maximum_no_cars - rs_parking_ticket_check_max.count()
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def accessed(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_detected = x_forwarded_for.split(',')[0]
    else:
        ip_detected = request.META.get('REMOTE_ADDR')

    date_now = datetime.datetime.now()
    num_access = 1

    rs_access = Access.objects.filter(
        ip=ip_detected)
    if rs_access.count() == 0:
        rs_parking_ticket = Access(
            ip=ip_detected,
            num_of_access=num_access,
            last_accessed=date_now,
        )
        rs_parking_ticket.save()
    else:
        timediff = (time.mktime(datetime.datetime.strptime(str(date_now), "%Y-%m-%d %H:%M:%S.%f").timetuple())) - (
            time.mktime(datetime.datetime.strptime(str(rs_access[0].last_accessed.replace(tzinfo=None)),
                                                   "%Y-%m-%d %H:%M:%S.%f").timetuple()))
        if timediff < 10:
            num_access = rs_access[0].num_of_access + 1
            rs_access.update(
                ip=ip_detected,
                num_of_access=num_access,
                last_accessed=date_now,
            )
        else:
            rs_access.update(
                ip=ip_detected,
                num_of_access=num_access,
                last_accessed=date_now,
            )

    return num_access
