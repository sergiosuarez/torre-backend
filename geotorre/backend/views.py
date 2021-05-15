# -*- coding: utf-8 -*-
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import urllib.request, json 

import time

@csrf_exempt
def get_location_username(request): 
    geojson = {}
    username = '' + str(request.POST['usern'])
    url_data = 'https://torre.bio/api/bios/'+username
    data=get_request(url_data)['person']['location']

    feature = {}
    feature['geometry'] ={ 'type':"Point" , 'coordinates':[float(data['longitude']) ,float(data['latitude']) ]}
    feature['geometry_name'] = "the_geom"
    feature['type'] = "Feature"
    feature['id'] = "ID"
    
    properties = {}
    properties['Lat'] = float(data['latitude'])
    properties['Long'] = float(data['longitude'])

    feature['properties'] = properties
    #features.append(feature)
    geojson['features'] = data
    geojson['crs'] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}}
    #return json.dumps(geojson)

    return JsonResponse(geojson, safe=False)


@csrf_exempt
def get_allmembers_xopportunity(request): 
    opport_id = '' + str(request.POST['opport_id'])
    url_data = 'https://torre.co/api/opportunities/'+opport_id
    data=get_request(url_data)['members']
    listmails=[]
    for result in data:
        print(result['person']['username'])
        listmails.append(str(result['person']['username']))
    return JsonResponse(listmails, safe=False)


#https://arda.torre.co/connections/torreSubjectId:1052454/highlights?limit=500


''' #if i have login
@csrf_exempt
def get_allmembers_xopportunity(request): 
    opport_id = '' + str(request.POST['opport_id'])
    url_data = 'https://torre.co/api/suite/opportunities/'+opport_id+'/candidates-rank/me?page=0&pageSize=1000'
    data=get_request(url_data)['person']['username']
    return JsonResponse(data, safe=False)

def get_totalcandidates(opport_id):
    url_data = 'https://torre.co/api/suite/opportunities/'+opport_id+'/candidates-rank/me?page=0&pageSize=1'
    num=get_request(url_data)['total']
    ten = num[:-1]
    print(str(int(ten)+1))
    num=int(ten)+1
    return num'''

def get_request(url_data):
    with urllib.request.urlopen(url_data) as url:
        data = json.loads(url.read().decode())
        return data
