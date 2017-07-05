#решить вопрос с поиском в начале текста!!!
import pymorphy2
from datetime import datetime, date, time

class News:
    
    def __init__(self, link, title, date, shortDescription, content, source):
        self.link = link
        self.title = title
        self.date = date
        self.shortDescription = shortDescription
        self.content = content        
        self.source = source
        
    
    def title(self):
        return self.title

    def date(self):
        return self.date

    def content(self):
        return self.content

    def link(self):
        return self.link

    def shortDescription(self):
        return self.shortDescription

    def source(self):
        return self.source

class Search:
    morph = pymorphy2.MorphAnalyzer()
    oldNews = []#массив jsonов
    news = []
    searchResults = []
    
    def newsList(self):
        self.oldNews = []        
        self.oldNews.append({"link":'vk.com',"title":'«Высокие ожидания сменились разочарованием»',"date":'03.07.2017',"shortDescription":'«Высокие ожидания',"content":'3–4 июля Москву посещает председатель КНР Си Цзиньпин. Президент Владимир Путин и глава Китая видятся в этом году уже третий раз, но именно официальный визит китайского коллеги российский лидер уже назвал «главным мероприятием двусторонних отношений» в 2017 году. На активное сотрудничество с Китаем в России возлагали много надежд все последние годы, но оказалось, что легких денег от Китая ждать не приходится.',"source":'ВКонтакте'})
        self.oldNews.append({"link":'ok.com',"title":'«Низкие ожидания сменились разочарованием»',"date":'04.08.2018',"shortDescription":'«Низкие ожидания',"source":'Одноклассники'})

        for new in self.oldNews:#создание списка объектов типа News
            if new.get('content') != None:
                self.news.append(News((new['link']), (new['title']), (new['date']), (new['shortDescription']), (new['content']), (new['source'])))
            else:
                self.news.append(News((new['link']), (new['title']), (new['date']), (new['shortDescription']), (None), (new['source'])))

    def addResult(self, result):#useless
        self.searchResults.append(result)
        
    def delDoubleSpace(self, string):#удаление лишних пробелов из запроса
        newstring = string.strip()
        if newstring.find("  ")==-1:
            return newstring
        else:
            newstring = newstring.replace("  "," ")
            return delDoubleSpace(newstring)
                
    def optimizedRequest(self, req):#оптимизация запроса(превращение в список минизапросов)
        request = self.delDoubleSpace(req)
        requestList = request.split(" ")
        optimizedRequestList = []
        miniReq = ""
        for request in requestList:
            if miniReq == "": 
                if request[0] == "|":             
                    if request[-1] == "|":
                        optimizedRequestList.append(request)
                    else:
                        miniReq = request
                else:
                    optimizedRequestList.append(request)
            else:
                miniReq = miniReq + " " + request
                if miniReq[-1] == "|":
                    optimizedRequestList.append(miniReq)
                    miniReq = ""

        if miniReq != "":            
            return "ERROR!!!"#сообщить о синтаксической ошибке!!! (есть открывающая "|", но нет закрывающей)
        else:
            return optimizedRequestList

    def search(self, request, mindate, maxdate, searchForTitle):
        if request == "ERROR!!!":
            return "ERROR!!!"
        if request == None:
            return self.news
        else:            
            self.newsList()
            miniRequests = self.optimizedRequest(request)#
            for new in self.news:
                check = 1
                if mindate != None:
                    if new.date < mindate:
                        check = 0
                if maxdate != None:
                    if new.date > maxdate:
                        check = 0
                for req in miniRequests:
                    if req[0] == "|" and req[-1] == '|':#строгий поиск
                        req = req.replace("|","")
                        reqList = self.optimizedRequest(req)
                        if searchForTitle == 1:
                            if new.title.find(" " + req + " ") == -1 and new.title.find(req.capitalize() + " ") == -1 and new.title.find("\n" + req.capitalize() + " ") == -1:
                                check = 0
                        else:
                            if new.content == None:
                                check = 0
                            elif new.content.find(" " + req + " ") == -1 and new.content.find(req.capitalize() + " ") == -1 and new.content.find("\n" + req.capitalize() + " ") == -1:
                                check = 0
                            
                    elif req[-1] == "*":#поиск со звёздочкой
                        req = req.replace("*","")
                        if searchForTitle == 1:
                            if new.title.find(" " + req) == -1 and new.title.find(" " + req.capitalize()) == -1 and new.title.find(req.capitalize()) == -1 and new.title.find("\n" + req.capitalize()) == -1:
                                check = 0
                        else:
                            if new.content == None:
                                check = 0
                            elif new.content.find(" " + req) == -1 and new.content.find(" " + req.capitalize) == -1 and new.content.find(req.capitalize()) == -1 and new.content.find("\n" + req.capitalize()) == -1:
                                check = 0
                            
                    elif req[0] == "[" and req[-1] == "]":#поиск всех форм слова
                        if len(req.split(" ")) == 1:
                            req = req.replace("[","")
                            req = req.replace("]","")
                            formCheck = 0
                            word = self.morph.parse(req)[0]
                            wordList = word.lexeme
                            for word in wordList:
                                if searchForTitle == 1:
                                    if new.title.find(" " + word.word + " ") != -1 or new.title.find(word.word.capitalize() + " ") != -1 or new.title.find("\n" + word.word.capitalize() + " ") != -1:
                                        formCheck = 1
                                else:
                                    if new.content == None:
                                        pass
                                    elif new.content.find(" " + word.word + " ") != -1 or new.content.find(word.word.capitalize() + " ") != -1 or new.content.find("\n" + word.word.capitalize() + " ") == -1:
                                        formCheck = 1
                            if formCheck == 0:
                                check = 0
                        else:
                            return ("ERROR!!!")#ошибка синтаксиса(несколько или 0 слов внутри []
                    
                    else:#обычный запрос
                        if searchForTitle == 1:
                            if new.title.find(" " + req + " ") == -1 and new.title.find(req.capitalize() + " ") == -1 and new.title.find("\n" + req.capitalize() + " ") == -1:
                                check = 0
                        else:
                            if new.content == None:
                                check = 0
                            elif new.content.find(" " + req + " ") == -1 and new.content.find(req.capitalize() + " ") == -1 and new.content.find("\n" + req.capitalize() + " ") == -1:
                                check = 0
                if check == 1:
                    self.searchResults.append(new)
            return self.searchResults
        
'''
s = Search()
for i in (s.search("|ожидания сменились|", None, None, 1)):
    print(i.title)
'''


#i = 0
#while i < len(news):
#    print (news[i].title)
#    i = i+1
