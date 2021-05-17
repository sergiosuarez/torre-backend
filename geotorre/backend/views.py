# -*- coding: utf-8 -*-
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import urllib.request, json 
import requests
import time

##PRODUCTION
@csrf_exempt
def get_location_username(request): 
    username = '' + str(request.POST['usern'])
    url_data = 'https://torre.bio/api/bios/'+username
    data=get_request(url_data)['person']['location']
    geojson=convert_geojson_user(data)
    return JsonResponse(geojson, safe=False)

@csrf_exempt
def get_allmembers_xopportunity(request): 
    opport_id = '' + str(request.POST['opport_id'])
    url_data = 'https://torre.co/api/opportunities/'+opport_id
    data=get_request(url_data)['members']
    listusers_loc=[]
    for result in data:
        member=str(result['person']['username'])
        url_data = 'https://torre.bio/api/bios/'+member
        listusers_loc.append(get_request(url_data)['person'])
    datageojson=get_geojson_membersloc(listusers_loc)
    return JsonResponse(datageojson, safe=False)

#Search Opportunities for skills
@csrf_exempt
def get_request_opportxskill(request):
    skill = '' + str(request.POST['skill'])
    url = "https://search.torre.co/opportunities/_search"

    payload = "{\"skill/role\":{\"text\":\""+skill+"\",\"experience\":\"potential-to-develop\"}}"
    headers = {
    'authority': 'search.torre.co',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'accept': 'application/json, text/plain, */*',
    'x-torre-subject': '1052454',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://torre.co',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://torre.co/',
    'accept-language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data=response.text
    return JsonResponse(json.loads(data), safe=False)

#Search Peoples for skills
@csrf_exempt
def get_request_peoplexskill(request):
    skill = '' + str(request.GET['parameters']).split(',')[0]
    size = '' + str(request.GET['parameters']).split(',')[1]
    url = "https://search.torre.co/people/_search?page=0&size="+size

    payload = "{\"skill/role\":{\"text\":\""+skill+"\",\"experience\":\"potential-to-develop\"}}"
    headers = {
    'authority': 'search.torre.co',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'accept': 'application/json, text/plain, */*',
    'x-torre-subject': '1052454',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://torre.co',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://torre.co/',
    'accept-language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data_fromtorre=json.loads(response.text)['results']
    #processing to geojson
    data=get_geojson_usersloc(data_fromtorre)
    return JsonResponse(data, safe=False)



###UTILITIES

def get_geojson_user(username): 
    url_data = 'https://torre.bio/api/bios/'+username
    data=get_request(url_data)['person']['location']
    return convert_geojson_user(data)

def get_onlyjson_user(username): 
    url_data = 'https://torre.bio/api/bios/'+username
    data=get_request(url_data)['person']
    return data

def get_request(url_data):
    with urllib.request.urlopen(url_data) as url:
        data = json.loads(url.read().decode())
        return data

def convert_geojson_user(data):
    geojson = {}
    features = []
    
    feature = {}
    feature['geometry'] ={ 'type':"Point" , 'coordinates':[float(data['longitude']) ,float(data['latitude']) ]}
    feature['geometry_name'] = "the_geom"
    feature['type'] = "Feature"
    feature['id'] = "ID" 
    properties = {}
    properties['Lat'] = float(data['latitude'])
    properties['Long'] = float(data['longitude'])
 
    feature['properties'] = properties
    features.append(feature)
    geojson['features'] = features
    geojson['crs'] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}}

    return geojson

def get_geojson_membersloc(listmembers_loc):
    listdata=  listmembers_loc['location']
    geojson = {}
    features = []
    
    for data in listmembers_loc:
        feature = {}
        feature['geometry'] ={ 'type':"Point" , 'coordinates':[float(data['longitude']) ,float(data['latitude']) ]}
        feature['geometry_name'] = "the_geom"
        feature['type'] = "Feature"
        feature['id'] = "ID" 
        properties = {}
        properties['Lat'] = float(data['latitude'])
        properties['Long'] = float(data['longitude'])
        #properties['shortName'] = str(data['shortName'])
        feature['properties'] = properties

        features.append(feature)

    geojson['features'] = features
    geojson['crs'] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}}

    return geojson

def get_geojson_usersloc(listusers):
    geojson = {}
    features = []
    
    for data in listusers:
        #get the coordinates of username
        location_user=get_onlyjson_user(data['username'])
        long_user=location_user['location']['longitude']
        lat_user=location_user['location']['latitude']
        created=location_user['created']
        
        feature = {}
        feature['geometry'] ={ 'type':"Point" , 'coordinates':[float(long_user) ,float(lat_user) ]}
        feature['geometry_name'] = "the_geom"
        feature['type'] = "Feature"
        feature['id'] = "ID" 
        properties = {}
        properties['Lat'] = float(lat_user)
        properties['Long'] = float(long_user)
        properties['locationName'] = data['locationName']
        properties['name'] = data['name']
        properties['openTo'] = data['openTo']
        properties['picture'] = data['picture']
        properties['verified'] = data['verified']
        properties['weight'] = data['weight']
        properties['compensations'] = data['compensations']
        properties['created']=str(created).replace('T',' ').replace('Z','')
        feature['properties'] = properties

        features.append(feature)

    geojson['features'] = features
    geojson['crs'] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}}

    return geojson

