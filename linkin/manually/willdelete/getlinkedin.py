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

def getAlreadyID():
    # print "insert into t_talents values(?,?,?,?,?,?,?,?,?,?)",t
    pList = []
    con = sqlite3.connect("d:/temp/test.db")
    cursor = con.cursor()
    cursor.execute("select id from t_talents")
    rows = cursor.fetchall()
    for row in rows:
        pList[row[0]] = 1
    con.close()
    return pList

def getID(url):
    pUrl = urlparse.urlparse(url)
    return urlparse.parse_qs(pUrl.query)['id'][0]

def ViewBot(browser):
    visited = {}
    pList = []
    count = 0
    people = []
    ret = True
    i = 0
    maxcount = 12
    
    time.sleep(random.uniform(7.6,15.9))
    # browser.get("https://www.linkedin.com/in/loh-weihan-9720373b?authType=name&authToken=YiBr&trk=hp-feed-member-name")
    # browser.get("http://www.linkedin.com/in/forrest-sun-9a85567?authType=name&authToken=RuXm&trk=hp-feed-member-photo")
    #time.sleep(random.uniform(15.6,20.9))

    # time.sleep(random.uniform(6.6,12.9))
    # print "browser.title:"+browser.title
    # page = BeautifulSoup(browser.page_source,"html.parser")
    # people = getPeopleLinks(page)

    szl = "http://www.linkedin.com/in/forrest-sun-9a85567?authType=name&authToken=RuXm&trk=hp-feed-member-photo&id=root"
    visited["root"] = 1
    pList.append(szl)

    while ret:
        
        if(count >= maxcount):
            ret = False
        

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
            browser.get(person)
            count += 1
            #sleep to make sure everything loads.
            #add random to make us look human.
            time.sleep(random.uniform(7.6,20.9))
            print person
            print "browser.title:"+browser.title
            page = BeautifulSoup(browser.page_source,"html.parser")
            #print "page:"+str(page)

            name = page.find('span',"full-name").string
            title = page.find('p',"title").string
            locality = page.find('span',"locality").string
            industry = page.find('dd',"industry").string
            curposition = page.find('span',"new-miniprofile-container").string
            education = ""
            email = ""
            imgurl = ""
            profile = page.find(id="background").get_text()

            t = (ID,name,title,locality,industry,curposition,education,email,imgurl,profile)
            AddTalents(t)

            print "Person %s is: %s|%s|%s|%s" % (count,name,title,locality,industry)
            people = getPeopleLinks(page)
        else:
            print "I'm lost Exiting"
            break            

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
    parser = argparse.ArgumentParser()
    parser.add_argument('email',help = "linkedin email")
    parser.add_argument("password",help = "linkedin password")
    args = parser.parse_args()

    # profile = webdriver.FirefoxProfile()
    # profile.set_preference('browser.startup.homepage_override.mstone', 'ignore')
    # profile.set_preference('startup.homepage_welcome_url.additional', '')
    # browser = webdriver.Firefox(profile)
    browser = webdriver.Firefox()
    browser.get("https://linkedin.com/uas/login")
    # browser = webdriver.Firefox()
    # browser.get("http://somedomain/url_that_delays_loading")
    try:
        element = WebDriverWait(browser, 10).until(
            # EC.presence_of_element_located((By.ID, "session_key-login"))
            EC.presence_of_element_located((By.ID, "session_password-login"))
        )
    finally:
        emailElement = browser.find_element_by_id("session_key-login")
        emailElement.send_keys(args.email)

        passElement = browser.find_element_by_id("session_password-login")
        passElement.send_keys(args.password)
        passElement.submit()

    # os.system('clear')
    os.system('cls')
    print "Sucess!Logined IN, Bot Starting!"
    ViewBot(browser)
	# browser.close()

if __name__ == "__main__":
    Main()

