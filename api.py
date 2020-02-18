#!/usr/bin/python
#coding=utf-8

import requests
from bs4 import BeautifulSoup
import json
import time
import web


url = "https://ncov.dxy.cn/ncovh5/view/pneumonia_peopleapp?from=timeline&isappinstalled=0"
urls = (
    '/init','Init',
    '/getAllList', 'GetAllList',
    '/getIndexRecommendList', 'GetIndexRecommendList',
    '/getWikiList', 'GetWikiList',
    '/getListByCountryTypeService2', 'GetListByCountryTypeService2',
    '/getIndexRumorList', 'GetIndexRumorList',
    '/getAreaStat', 'GetAreaStat',
    '/getTimelineService', 'GetTimelineService',
    '/getStatisticsService', 'GetStatisticsService',
    '/getListByCountryTypeService1', 'GetListByCountryTypeService1',

)
resp = {}

app = web.application(urls, globals())

# ------------------------------ web---------------------------------
class Init:
    def GET(self):
        web.header('Content-Type', 'text/json;charset=UTF-8')
        return initData(url)

class GetAllList:
    def GET(self):
        web.header('Content-Type', 'text/json;charset=UTF-8')
        if not(hasattr(resp, 'getAllList')):
            return getInitErrorResponse()
        return resp.getAllList()

class GetIndexRecommendList:
    def GET(self):
        web.header('Content-Type', 'text/json;charset=UTF-8')
        if not(hasattr(resp, 'getIndexRecommendList')):
            return getInitErrorResponse()
        return resp.getIndexRecommendList()

class GetWikiList:
    def GET(self):
        web.header('Content-Type', 'text/json;charset=UTF-8')
        if not(hasattr(resp, 'getWikiList')):
            return getInitErrorResponse()
        return resp.getWikiList()

class GetListByCountryTypeService2:
    def GET(self):
        web.header('Content-Type', 'text/json;charset=UTF-8')
        if not(hasattr(resp, 'getListByCountryTypeService2')):
            return getInitErrorResponse()
        return resp.getListByCountryTypeService2()

class GetIndexRumorList:
    def GET(self):
        web.header('Content-Type', 'text/json;charset=UTF-8')
        if not(hasattr(resp, 'GetIndexRumorList')):
            return getInitErrorResponse()
        return resp.getIndexRumorList()

class GetAreaStat:
    def GET(self):
        web.header('Content-Type', 'text/json;charset=UTF-8')
        if not(hasattr(resp, 'GetAreaStat')):
            return getInitErrorResponse()
        return resp.getAreaStat()

class GetTimelineService:
    def GET(self):
        web.header('Content-Type', 'text/json;charset=UTF-8')
        if not(hasattr(resp, 'getTimelineService')):
            return getInitErrorResponse()
        return resp.getTimelineService()

class GetStatisticsService:
    def GET(self):
        web.header('Content-Type', 'text/json;charset=UTF-8')
        if not(hasattr(resp, 'getStatisticsService')):
            return getInitErrorResponse()
        return resp.getStatisticsService()

class GetListByCountryTypeService1:
    def GET(self):
        web.header('Content-Type', 'text/json;charset=UTF-8')
        if not(hasattr(resp, 'getListByCountryTypeService1')):
            return getInitErrorResponse()
        return resp.getListByCountryTypeService1()


# ------------------------------ web---------------------------------

def getInitErrorResponse():
    respObj = {}
    respObj['code'] = 40001
    respObj['message'] = 'error'
    respObj['data'] = '请初始化数据，调用http://127.0.0.1:8080/init'
    # json
    return json.dumps(respObj,ensure_ascii=False)

def analysisHtml(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
    return soup

def json2Obj(soup,id):
    getIndexRecommendList = soup.find(id=id)
    text = getIndexRecommendList.get_text()
    if id == 'getStatisticsService':
        start = text.find('=') + 1
        end = text.find('catch') - 1
        jsonObject = text[start:end]
        return json.loads(jsonObject)

    else:
        start = text.find('[')
        end = text.rfind(']') + 1
        jsonArray = text[start:end]
        # print('-----------------------------')
        # print(id,jsonArray)
        
        #将Json转为对象
        return json.loads(jsonArray)
    
class ResponseObject():
    responseObj = {}

    def __init__(self,obj):
        self.responseObj = obj
    
    def buildResponseJson(self,data):
        respObj = {}
        respObj['code'] = 200
        respObj['message'] = 'success'
        respObj['data'] = data
        jsonStr = json.dumps(respObj,ensure_ascii=False)
        return jsonStr

    def getAllList(self):
        print('getAllList')
        return self.buildResponseJson(self.responseObj)
    
    def getIndexRecommendList(self):
        indexRecommendList = self.responseObj['getIndexRecommendList']
        return self.buildResponseJson(indexRecommendList)
    
    def getWikiList(self):
        wikiList = self.responseObj['getWikiList']
        return self.buildResponseJson(wikiList)

    def getListByCountryTypeService2(self):
        listByCountryTypeService2 = self.responseObj['getListByCountryTypeService2']
        return self.buildResponseJson(listByCountryTypeService2)

    def getIndexRumorList(self):
        indexRumorList = self.responseObj['getIndexRumorList']
        return self.buildResponseJson(indexRumorList)

    def getAreaStat(self):
        areaStat = self.responseObj['getAreaStat']
        return self.buildResponseJson(areaStat)

    def getTimelineService(self):
        timelineService = self.responseObj['getTimelineService']
        return self.buildResponseJson(timelineService)

    def getStatisticsService(self):
        statisticsService = self.responseObj['getStatisticsService']
        return self.buildResponseJson(statisticsService)

    def getListByCountryTypeService1(self):
        listByCountryTypeService1 = self.responseObj['getListByCountryTypeService1']
        return self.buildResponseJson(listByCountryTypeService1)


# getStatisticsService是首页数据
def initData(url):
    global resp
    
    soup = analysisHtml(url)
    obj = {}
    ids = ['getIndexRecommendList','getWikiList','getListByCountryTypeService2','getIndexRumorList',
        'getAreaStat','getTimelineService','getStatisticsService','getListByCountryTypeService1']
    for id in ids:
        idObj = json2Obj(soup, id)
        obj[id] = idObj
    
    resp = ResponseObject(obj)
    jsonStr = resp.buildResponseJson(ids)
    return jsonStr

if __name__ == "__main__":
    app.run()
