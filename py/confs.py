'''
Created on 2012-3-7

@author: GeZiyang
'''
#########################
from urllib import urlopen
import urllib2
import cookielib
import re
import time
import thread
import threading

NAMELIST=[]
#get search by shortName result ids
def getLinks(shortName):    
    searchInterface = "http://ieeexplore.ieee.org/xpl/conferences.jsp?queryText="
    try:
        resultPage = urlopen(searchInterface + shortName)
    except:
        return False
    resultText = resultPage.read()       
    matchGroup = re.findall('/xpl/conhome\.jsp\?punumber=(\d+)',resultText,re.IGNORECASE)
    return matchGroup #list

#get search by shortName result full name list
def getConfName(shortName):
    global NAMELIST
    list = getLinks(shortName)
    if(list == False):
        return False
    if(list == None):
        print("No matched conference!")
        return [] 
    else:       
        namelist = []
        for id in list:
            try:
                confPage = urlopen("http://ieeexplore.ieee.org/xpl/conhome.jsp?punumber=" + id)
            except:
                return False
            confText = confPage.read()
            matchGroup = re.findall('<h1>(.*?)</h1>',confText,re.IGNORECASE)
            namelist.append((matchGroup[0],id))
        NAMELIST=namelist
        return namelist

#get all about the conference in history        
def getHisLinks(result_id):
    try:    
        confPage = urlopen("http://ieeexplore.ieee.org/xpl/conhome.jsp?punumber=" + str(result_id))
    except:
        return False
    confText = confPage.read()
    conf_ids = re.findall('mostRecentIssue\.jsp\?punumber=(\d+)',confText,re.IGNORECASE)
    return conf_ids
    
#
def getPaperLinks(conf_id):   
    
    #first request to get element oqs    
    firstreq = "http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?punumber=" + str(conf_id)
    try:
        firstPage = urlopen(firstreq)
    except:
        return False
    firstText = firstPage.read()
    oqs = re.findall('id=\"oqs\"\s*value=\"(.*?)\"',firstText,re.IGNORECASE)        
    secondreq = "http://ieeexplore.ieee.org/xpl/tocresult.jsp?" + oqs[0] + "&rowsPerPage=1000&pageNumber=1"    #suppose the number of paper is less than 1000
    try:
        paperListPage = urlopen(secondreq)
    except:
        return False
    paperText = paperListPage.read()
    paperlist = re.findall('/xpl/articleDetails\.jsp\?tp=&arnumber=(\d+)',paperText,re.IGNORECASE) 
    paperset = set(paperlist)
    paperlist = list(paperset) #delete the same      
        
    return paperlist #list

#place to catch exception
def getAbstract(paper_id):    
    requrl = "http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=" + str(paper_id)
    try:
        paperPage = urlopen(requrl)
        paperText = paperPage.read()        
    except Exception:
        paperText = ""
            
    title = re.findall('<h1>\s*(.+?)\s*</h1>',paperText,re.IGNORECASE)        
    abs = re.findall('<h2>Abstract</h2>\s*</a>\s*<p>(.+?)</p>',paperText,re.IGNORECASE)
    print abs #debug
    if title == [] or abs == []:#network exception
        return "empty###empty"
    abs[0] = title[0] + "###" + abs[0]
    return abs[0]

def getNameById(conf_home):
    try:
        confPage = urlopen("http://ieeexplore.ieee.org/xpl/conhome.jsp?punumber=" + str(conf_home))
    except:
        return False
    confText = confPage.read()
    matchGroup = re.findall('<h1>(.*?)</h1>',confText,re.IGNORECASE)
    return matchGroup[0]

def buildNewDb(conf_home):
    absDb = {} #dic
    
    conf_name = getNameById(conf_home)
    count = 1
    while conf_name == False:
        conf_name = getNameById(conf_home)
        count += 1
        if count > 5: # try to get full name 5 times
            return False
    
    conf_all = getHisLinks(conf_home)
    count = 1
    while conf_all == False:
        conf_all = getHisLinks(conf_home)
        count += 1
        if count > 5: # try to getHisLinks 5 times
            return False
        
    paper_all = []        
    for conf_id in conf_all:            
        paper_ids = getPaperLinks(conf_id)
        count = 1            
        while paper_ids == False:
            paper_ids = getPaperLinks(conf_id)
            count += 1
            if count > 5: # try to getPaperLinks 5 times
                return False
        paper_all += paper_ids                          
    for paper_id in paper_all:
        abs = getAbstract(paper_id)
        
        if(abs == "empty###empty"):#mostly caused by network error
            print "None Abstract :%d ,retrying..." % int(paper_id)
            count = 1
            while abs == "empty###empty":                        
                abs = getAbstract(paper_id)                
                count += 1
                if count > 5:
                    print "cann't get the abstract of %d" % int(paper_id) #mostly caused by no abstract
                    break
        
        absDb[paper_id] = abs
        print "%d:%s" % (int(paper_id),abs) #debug
    print "start writing file..." #debug    
    file = open("confs/"+ str(conf_home),'w')
    for conf_id in conf_all:
        file.write(conf_id + " ")
    file.write("\n")
    for paper_id in paper_all:
        if(absDb[paper_id] == "empty###empty"):
            continue
        file.write(paper_id + "\n")
        file.write(absDb[paper_id] + "\n")        
    file.close() 
    indexfile = open("confs/confindex",'a')
    indexfile.write(str(conf_home) + '\n')
    indexfile.write(str(conf_name) + '\n')
    indexfile.close()
    # add write to index   
    print "finished."
    return True


def getFileDb(conf_home):
    absDb = {}
    try:
        file = open("confs/" + str(conf_home))
        file.readline()
        while True:
            line = file.readline()
            if not line:break
            absDb[line.split()[0]] = file.readline()
        file.close()
        return absDb
    except Exception:
        print "No database file"
        return False

def checkUpdate(conf_home):
    conf_all = getHisLinks(conf_home)
    try:
        file = open("confs/" + str(conf_home))
        conflist = file.readline().split()
        if(set(conf_all) == set(conflist)):
            return True #can use
        else:
            return False # need for update
    except:
        print "no database yet"
        return False

def searchPaper(conf_id,keylist):
    print keylist
    time.sleep(5)
    resultdic = {}
    absDb = getFileDb(conf_id)
    if keylist == []:
        return absDb
    for paper_id,title_abs in absDb.items():
        match = True
        try:
            for key in keylist:
                if title_abs.find(key) >= 0:
                    continue
                else:
                    match = False
                    break
            if match:
                resultdic[paper_id] = title_abs
                print paper_id
                print resultdic[paper_id]
        except:
            continue
    return resultdic

#check for auth, if success,save to cookiefile    
def authCheck(cookiefile):    
    cookies = cookielib.MozillaCookieJar(cookiefile)
    cookiehand  = urllib2.HTTPCookieProcessor(cookies)
    opener = urllib2.build_opener(cookiehand)
    opener.addheaders = [("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"),
                         ("Host","ieeexplore.ieee.org")]
    try:
        opener.open("http://ieeexplore.ieee.org/xpl/conferences.jsp")
    except:
        print "network error"
        return False
    for item in cookies:
        if item.name == "xploreCookies":
            print "auth success!"
            cookies.save(cookiefile, ignore_discard=True, ignore_expires=True)
            return True
    return False

def downWithCookies(cookiefile,paper_id):
    abs = getAbstract(paper_id)
    if(abs == "empty###empty"):#mostly caused by network error
            print "None Abstract :%d ,retrying..." % int(paper_id)
            count = 1
            while abs == "empty###empty":                        
                abs = getAbstract(paper_id)                
                count += 1
                if count > 5:
                    print "cann't get the abstract of %d" % int(paper_id) #mostly caused by no abstract
                    break
    cookies = cookielib.MozillaCookieJar(cookiefile)
    cookies.load(cookiefile, ignore_discard=True, ignore_expires=True)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    page = opener.open("http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=" + str(paper_id))
    pagetext = page.read()
    matchGroup = re.findall('<frame src="(http.*?)"',pagetext,re.IGNORECASE)
    try:
        pdflink = matchGroup[0]   
    except IndexError:
        print "cookies outdated"
        return False 
    pdfpage = opener.open(pdflink)
    pdftext = pdfpage.read()
    f = open("papers/" + str(paper_id)+".pdf","wb")
    f.write(pdftext)
    f.close()
    index = open("papers/paperindex","a")
    index.write(str(paper_id) + "\n")
    index.write(str(abs) + "\n")
    index.close()
    return True

def getConfIndex():
    confIndex = {}
    try:
        file = open("confs/confindex")        
        while True:
            line = file.readline()
            if not line:break
            confIndex[line.split()[0]] = file.readline()
        file.close()
        return confIndex
    except Exception:
        print "No conference index file"
        return False
    
def getPaperIndex():
    paperIndex = {}
    try:
        file = open("papers/paperindex")        
        while True:
            line = file.readline()
            if not line:break
            paperIndex[line.split()[0]] = file.readline()
        file.close()
        return paperIndex
    except Exception:
        print "No paper index file"
        return False
    
def timingDown(seconds,paper_id):
    time.sleep(seconds)
    print "Starting download..."
    count = 1
    while True:        
        print "trying %d" % count
        if authCheck("cookies.txt") == True:
            print "auth success!"
            break
        count += 1
        time.sleep(5)
    if downWithCookies("cookies.txt",paper_id):
        print "download success!"
        return True
    return False

def threadDown(seconds,paper_id):
    thread.start_new_thread(timingDown,(seconds,paper_id)) 
    
    

def test():
    buildNewDb(1001307) 
    #threadDown(100,5279450)
    #downTest()
    
    #print u"test"
    #print "test".encode('utf-8')
    '''
    paper_id = raw_input("Input the id of the paper:")
    count = 1
    while True:        
        print "trying %d" % count
        if authCheck("cookies.txt") == True:
            print "auth success!"
            break
        count += 1
        time.sleep(5)
    if downWithCookies("cookies.txt",paper_id):
        print "download success!"
    buildNewDb(1001545)   
    time.sleep(300)
    '''
    pass
    
    
if __name__ == '__main__':test()
