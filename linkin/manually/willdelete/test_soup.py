import urllib2
from bs4 import BeautifulSoup
import sqlite3
import re

def AddTalents(t):
    # print "insert into t_talents values(?,?,?,?,?,?,?,?,?,?)",t
    con = sqlite3.connect("d:/temp/test.db")
    con.execute("insert into t_talents (id,name,title,locality,industry,curposition,education,email,imgurl,profile) values(?,?,?,?,?,?,?,?,?,?)",t)
    con.commit()
    con.close()
    print "done"

def getAlreadyID():
    # print "insert into t_talents values(?,?,?,?,?,?,?,?,?,?)",t
    visited = {}
    con = sqlite3.connect("d:/temp/test.db")
    cursor = con.cursor()
    cursor.execute("select id from t_talents")
    rows = cursor.fetchall()
    for row in rows:
        a = row[0]
        visited[a] = 1
    con.close()
    return visited

def Main():
    visited = getAlreadyID()
    print visited
    # print "aaa"
    # url = urllib2.urlopen("http://localhost:8080/talentscentral/mht.htm")
    # #soup = BeautifulSoup(url,"lxml")
    # page = BeautifulSoup(url,"html.parser")
    # # for script in soup.find_all('script'):
    # #     script.decompose()
    # #print soup.prettify().encode("utf-8")
    # ID = "id272"
    # name = page.find('span',"full-name").string
    # title = page.find('p',"title").string
    # locality = page.find('span',"locality").string
    # industry = page.find('dd',"industry").string
    # curposition = page.find('span',"new-miniprofile-container").string
    # education = ""
    # email = ""
    # imgurl = ""
    # profile = page.find(id="background").get_text()

    # t = (ID,name,title,locality,industry,curposition,education,email,imgurl,profile)
    # AddTalents(t)


if __name__ == "__main__":
    Main()



