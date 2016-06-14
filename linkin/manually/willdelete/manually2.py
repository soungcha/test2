import  argparse,os,time
import urlparse,random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

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

def getJobLink2(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        links.append(url)
    return links

def getID(url):
    pUrl = urlparse.urlparse(url)
    return urlparse.parse_qs(pUrl.query)['id'][0]

def ViewBot(browser):
    visited = {}
    pList = []
    count = 0
    ret = True
    i = 0
    time.sleep(random.uniform(5.6,6.9))
    #browser.get("http://localhost:8080/talentscentral/members/user/hunter_positionbank.php")
    browser.get("http://localhost:8080/talentscentral/wh.htm")
    time.sleep(random.uniform(5.6,6.9))
    while ret:
        i += 1
        if(i > 1):
            ret = False
        #sleep to make sure everything loads.
        #add random to make us look human.
        time.sleep(random.uniform(5.6,6.9))
        print "browser.title:"+browser.title
        page = BeautifulSoup(browser.page_source,"lxml")
        #print "page:"+str(page)
        people = getJobLink2(page)

        if people:
            print "total links in the page:"+str(len(people))
            for person in people: 
                print "person:"+ str(person)
                # ID = getID(person)
                # print "id:" + ID
                # if ID not in visited:
                #     print "person:"+ person
                #     pList.append(person)
                #     visited[ID] = 1
        else:
            ret = False
        '''
        if pList:#If there is people to look at, then look at them
            person = pList.pop()
            browser.get(person)
            count += 1
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
    #browser = webdriver.Chrome()
    #browser.get("http://www.talentscentral.com/Members/user/login.php")
    browser.get("http://localhost:8080/talentscentral/members/user/login.php")
    # browser = webdriver.Firefox()
    # browser.get("http://somedomain/url_that_delays_loading")
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
    finally:
        emailElement = browser.find_element_by_id("email")
        emailElement.send_keys(args.email)

        passElement = browser.find_element_by_id("password")
        passElement.send_keys(args.password)
        passElement.submit()

        # os.system('clear')
        os.system('cls')
        print "[+] Sucess!Logined IN, Bot Starting!"
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

