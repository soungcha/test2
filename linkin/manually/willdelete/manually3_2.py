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

def getJobLinks(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if '/jobs' in url:
                links.append(url)
    return links

def AddTalents(t):
    # print "insert into t_talents values(?,?,?,?,?,?,?,?,?,?)",t
    con = sqlite3.connect("d:/temp/test.db")
    con.execute("insert into t_talents (id,name,title,locality,industry,curposition,education,email,imgurl,profile) values(?,?,?,?,?,?,?,?,?,?)",t)
    con.commit()
    con.close()
    print "done"

def getJobLink2(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        links.append(url)
    return links

def getID(url):
    pUrl = urlparse.urlparse(url)
    return urlparse.parse_qs(pUrl.query)['id'][0]

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

def ViewBot(browser):
    visited = getAlreadyID()
    pList = []
    people = []
    count = 0
    ret = True
    i = 1
    maxcount = 2

    # time.sleep(random.uniform(12.6,15.9))
    sc = "http://localhost:8080/talentscentral/sc.htm?type=12&id=test3"
    visited["test3"] = 1
    pList.append(sc)
    szl = "http://localhost:8080/talentscentral/chq.htm?type=12&id=test4"
    visited["test4"] = 1
    pList.append(szl)
    i = 2


    while ret:
        if(count >= maxcount):
            ret = False
        count += 1

        

        if people:
            print "total people in the page:"+str(len(people))
            for person in people: 
                ID = getID(person)
                if ID not in visited:
                    i += 1
                    if(i < maxcount):
                        pList.append(person)
                        visited[ID] = 1

        if pList:#If there is people to look at, then look at them
            person = pList.pop()
            ID = getID(person)
            print person
            browser.get(person)
            #sleep to make sure everything loads.
            #add random to make us look human.
            try:
                time.sleep(random.uniform(15.6,20.9))
                
                page = BeautifulSoup(browser.page_source,"html.parser")
                for script in page.find_all('script'):
                    script.decompose()
                #print "page:"+str(page)
                # title = page.find("title").string
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
                t = (ID,name,title,locality,industry,curposition,education,email,imgurl,profile)
                AddTalents(t)
                people = getPeopleLinks(page)
            except:
                print "something went wrong"
        '''
        else:  #otherwise find people via the job pages
            jobs = getJobLinks(page)
            if jobs:
                job = random.choice(jobs)
                root = 'http://www.linkedin.com'
                root2 = 'http://www.linkedin.com'
                if root not in job or roots not in jobs:
                    job = 'https://www.linkedin.com'+job
                browser.get(job)
            else:
                print "I'm lost Exiting"
                break
        #Output make option for this
        print "[+] "+browser.title+" Visited! \n("\
            +str(count) +"/" +str(len(pList))+") Visited queure"
        '''


def Main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('email',help = "linkedin email")
    # parser.add_argument("password",help = "linkedin password")
    # args = parser.parse_args()

    # profile = webdriver.FirefoxProfile()
    # profile.set_preference('browser.startup.homepage_override.mstone', 'ignore')
    # profile.set_preference('startup.homepage_welcome_url.additional', '')
    # browser = webdriver.Firefox(profile)
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

