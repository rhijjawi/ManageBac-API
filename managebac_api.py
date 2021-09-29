import requests as req
from bs4 import BeautifulSoup
cal = {"Jan": 1,"Feb": 2,"Mar": 3,"Apr": 4,"May": 5,"Jun": 6,"Jul": 7,"Aug": 8,"Sep": 9,"Oct": 10,"Nov": 11,"Dec": 12,}
fdict = {"studentname": "", "deadlines": [], "tasks": []}
cookiestart = ["_managebac_session", "managebac_session", "_managebac_session: "]
class NoDomain(Exception):
    def __init__(self, message="""Make sure you defined the domain in the function. main("domain", "cookie")\nEx:run("myschool",cookie) OR run("myschool.managebac.com",cookie)"""):
        self.message = message
        super().__init__(self.message)

class NoCookie(Exception):
    def __init__(self, message="""Make sure you defined the cookie in the function. main("domain", "cookie")\nEx:run(domain,"0sjd8cho1oasd98afashvas9qryt8q3845iqengfiehr")"""):
        self.message = message
        super().__init__(self.message)

class InvalidURL(Exception):
    def __init__(self, domain, url, message="""INVALID URL: Make sure you defined the domain PROPERLY in the function. main("domain", "cookie")\nEx:run("myschool",cookie) OR run("myschool.managebac.com",cookie)"""):
        self.message = message
        self.url = url
        self.domain = domain
    
    def __str__(self):
        print(f"https://[red]{domain}[/red].managebac.com")
        return  "is an invalid domain, please verify information and retry"

def mbapi(domain:str=None, cookie:str=None):
    """
    Param DOMAIN: the subdomain of your FariaOne ManageBac site (The ****. part of ****.managebac.com)
    Param COOKIE: Your MB authentication cookie (it's called _managebac_session) that you can find by pressing F12, then clicking Storage, and Cookies. (Only the value!)
    """
    fdict = {"studentname": "", "deadlines": [], "tasks": []}
    domain = domain or None
    cookie = cookie or None
    if domain == None and cookie == None:
        domain = input("""What is the subdomain of your school's ManageBac site?\nEnter ONLY the subdomain (****).managebac.com:\n""")
        cookie = input("""What is the session cookie of your ManageBac login?\nEnter ONLY the subdomain value, not the name of the cookie:\n""")
    elif domain != None and cookie == None:
        raise NoCookie
    elif domain == None and cookie != None:
        raise NoDomain

    def cookiecheck(cookie):
        if len(cookie)<30:
            raise NoCookie
        for i in cookiestart:
            if cookie.startswith(i):
                cookie = cookie.replace(i, "")
    def domaincheck(domain):
        if domain.endswith("""managebac.com"""):
            domain = domain.replace(".managebac.com",'')
    cookiecheck(cookie)
    domaincheck(domain)
    try:
        cook = {"_managebac_session": f"{cookie}", "hide_osc_announcement_modal" : "true"}
        ddeadline = []
        dtask = []
        url = f"https://{domain}.managebac.com/student/tasks_and_deadlines?upcoming_page="
        for i in range(1,4):
            try:
                r = req.get(url+f"{i}",cookies=cook)
            except Exception as e:
                print(f"https://[red]{domain}[/red].managebac.com/student/tasks_and_deadlines?upcoming_page=")
                raise InvalidURL(domain, url)
            soup = BeautifulSoup(r.content, "html.parser")
            results = soup.find(class_="upcoming-tasks")
            try:
                name = soup.find("title").text
                name = name.split('| ')[1]
                tasks = results.find_all("div", class_="line task-node anchor js-presentation")
                deadlines = results.find_all("div", class_="line")
            except Exception as e:
                print(e)
            try:
                tasks = results.find_all("div", class_="line task-node anchor js-presentation")
                deadlines = results.find_all("div", class_="line")
            except Exception as e:
                raise InvalidURL(domain, url)
            for task in tasks:
                day = task.find("div", class_="day").text
                month = task.find("div", class_="month").text
                title = task.find("h3", class_="title")
                title = title.find("a").text
                link = task.find("a", href=True)
                link = link['href']
                id = link.split('core_tasks/',1)[1]
                tdict = {"id": id, "link" : f"https://{domain}.managebac.com{str(link)}","title": title, "due-date": f"{day}/{cal[f'{month}']}"}
                dtask.append(tdict)
            for task in deadlines:
                title = task.find("h4", class_="title")
                if title != None:
                    title = title.find("a").text
                    datebadge = task.find("div", class_="date-badge")
                    day = datebadge.find("div", class_="day").text
                    month = datebadge.find("div", class_="month").text
                    link = task.find("a", href=True)
                    link = link['href']
                    id = link.split('events/',1)[1]
                    ddict = {"id": id, "link" : f"https://{domain}.managebac.com{str(link)}","title": title, "due-date": f"""{datebadge.find("div", class_="day").text}/{cal[f'{datebadge.find("div", class_="month").text}']}"""}
                    ddeadline.append(ddict)
            del(tasks, soup, results, r)
        fdict['studentname'] = name
        fdict['deadlines'] = ddeadline
        fdict['tasks'] = dtask
    except Exception as e:
        print(e)
    return fdict
