# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 19:13:20 2021

@author: USER
"""
import requests
import json

def queryAir(name):

    content = json.loads(requests.get('http://opendata2.epa.gov.tw/AQI.json').text)
    
    air = {}
    
    for item in content:
        
        air[item['SiteName']] = item['AQI']

    ans = air.get(name,'找不到')
    return ans


def getWeather(area):
    url='https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=rdec-key-123-45678-011121314'
    allWeather = json.loads(requests.get(url).text)
    weather = {}
    
    item = allWeather['records']['location']
    for city in item:
        cityname = city['locationName']
        info = city['weatherElement']
        w = info[0]['time'][0]['parameter']
        ans = w['parameterName']
        weather[cityname] = ans
    return weather.get(area,'找不到')
        
