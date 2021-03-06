 #-*- coding: utf-8 -*-
import  argparse,os,time
import urlparse,random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sqlite3

def getPeopleLinks(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if 'profile/view?id=' in url:
                links.append(url)
    return links


def AddTalents(t):
    # print "insert into t_talents values(?,?,?,?,?,?,?,?,?,?)",t
    con = sqlite3.connect("d:/temp/test.db")
    con.execute("insert into t_talents (id,name,title,locality,industry,curposition,education,email,imgurl,profile,url) values(?,?,?,?,?,?,?,?,?,?,?)",t)
    con.commit()
    con.close()
    print "done"

def getNextLink():
    con = sqlite3.connect("d:/temp/test.db")
    cursor = con.cursor()
    cursor.execute("select id,link from t_links_test where badflag='F' and id not in (select id from t_talents) limit 1")
    row = cursor.fetchone()
    # nextlink = row[0]
    con.close()
    if row:
        return row[1]
    else:
        return ""

def addLinks(d):
    con = sqlite3.connect("d:/temp/test.db")
    con.execute("REPLACE INTO t_links (id, link,badflag ) VALUES (?,?,'F' )",d)
    con.commit()
    con.close()

def setBadLink(id):
    con = sqlite3.connect("d:/temp/test.db")
    con.execute("update t_links_test set badflag='T' where id = '"+id+"'")
    con.commit()
    con.close()

def getID(url):
    pUrl = urlparse.urlparse(url)
    return urlparse.parse_qs(pUrl.query)['id'][0]

def ViewBot(browser):
    #visited = getAlreadyID()
    #pList = []
    people = []
    ret = True
    count = 0
    maxcount = 5


    while ret:
        #exit if has reached the max count defined in maxcount
        #so we can control each time, how many talents to fetch
        count += 1
        if(count > maxcount):
            print "max count reached and exit"
            return

        #exit if no more next link there, however is not possible in produciton env
        curLink = getNextLink();
        if curLink:
            print curLink
        else:
            print "Done for no next link"
            return        

        if people:
            print "total people in the page:"+str(len(people))
            for person in people: 
                ID = getID(person)
                d = (ID,person)
                addLinks(d)

        if curLink:
            #If there is people to look at, then look at them
            ID = getID(curLink)
            browser.get(curLink)
            try:
                #sleep to make sure everything loads.
                #add random to make us look human.
                time.sleep(random.uniform(15.6,20.9))
                
                page = BeautifulSoup(browser.page_source,"html.parser")
                # for script in page.find_all('script'):
                #     script.decompose()

                print "browser.title:"+browser.title

                name = page.find('span',"full-name").string
                title = page.find('p',"title").string
                locality = page.find('span',"locality").string
                industry = page.find('dd',"industry").string
                curposition = page.find('span',"new-miniprofile-container").string
                #education = page.find(id="overview-summary-education").find(title="More details for this school").string
                education = ""
                #email = page.find(id="email-view").string
                email = ""
                imgurl = ""
                profile = page.find(id="background").get_text()

                print "Person %s is: %s" % (count,name.encode("utf-8"))
                # print "Person %s is: %s" % (count,name.encode("utf-8"))
                t = (ID,name,title,locality,industry,curposition,education,email,imgurl,profile,curLink)
                AddTalents(t)
                #people = getPeopleLinks(page)
            except:
                print "something went wrong"
                import traceback,sys
                traceback.print_exception(*sys.exc_info())#将异常信息打印在解释器上
                #以下是写入文件
                fp=open("d:\\error.txt","a")
                traceback.print_exception(*sys.exc_info(),file=fp)
                fp.close()
                setBadLink(ID)

def Main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('email',help = "linkedin email")
    # parser.add_argument("password",help = "linkedin password")
    # args = parser.parse_args()

    # profile = webdriver.FirefoxProfile()
    # profile.set_preference('browser.startup.homepage_override.mstone', 'ignore')
    # profile.set_preference('startup.homepage_welcome_url.additional', '')
    # browser = webdriver.Firefox(profile)

    # link = getNextLink();
    # if link:
    #     print link
    # else:
    #     print "noresult2"
    # return
    browser = webdriver.Firefox()
    #browser = webdriver.Chrome()
    #browser.get("http://www.talentscentral.com/Members/user/login.php")
    # browser.get("http://localhost:8080/talentscentral/chq.htm")
    # browser = webdriver.Firefox()
    # browser.get("http://somedomain/url_that_delays_loading")
    # try:
    #     element = WebDriverWait(browser, 10).until(
    #         EC.presence_of_element_located((By.ID, "email"))
    #     )
    # finally:
    #     emailElement = browser.find_element_by_id("email")
    #     emailElement.send_keys(args.email)

    #     passElement = browser.find_element_by_id("password")
    #     passElement.send_keys(args.password)
    #     passElement.submit()

    # os.system('clear')
    os.system('cls')
    print "Sucess!Logined IN, Bot Starting!"
    #time.sleep(random.uniform(10.6,16.9))
    # browser.get("https://www.linkedin.com/wvmx/profile?trk=nav_responsive_sub_nav_wvmp")
    # try:

	#     element2 = WebDriverWait(browser, 10).until(
	#         EC.presence_of_element_located((By.ID, "pymk-container"))
	#     )
	# finally:
	#     ViewBot(browser)
    ViewBot(browser)
	# # browser.close()

if __name__ == "__main__":
    Main()

