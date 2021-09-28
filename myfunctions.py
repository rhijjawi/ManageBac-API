import requests as req
from bs4 import BeautifulSoup
cal = {"Jan": 1,"Feb": 2,"Mar": 3,"Apr": 4,"May": 5,"Jun": 6,"Jul": 7,"Aug": 8,"Sep": 9,"Oct": 10,"Nov": 11,"Dec": 12,}
fdict = {"studentname": "", "deadlines": [], "tasks": []}
cookiestart = ["_managebac_session", "managebac_session", " "]
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

domain = """isuganda""" or None
cookie = r"""XDg9OWHX1FoqCuyN0mKtOUwicjs%2FNNvWkLktEv3lzMzXKb3eYbUE44WhG2rQ5JxQBFrwW62bd%2B2LdAfOvkRQ72LtzrU0dxq%2BQy3wkbQtx4CTuzLs%2BJRJupxAmGlndAW2dNNnfnctAPVFZx0igIfTu%2Brk6SmjMiw71LEd0CRMM%2FUtKucU89bflXQMKI6790CU3tZlSbi%2FUh9dURkDRYYNiyuGKVtYZYb6cBsE7fXv%2FEVzYptQstLv8w228Hy4jDphjscAH4W2%2Bhh5YmAno0CLBZrxvy6uoGgFwQWTjLoJRVJE5N93aSOnpqr68uSyjaDi993FjyaR7sbcxOhSSVznxlRn1sdcxLkFIpzHi0Z%2BAnFV%2FQi9%2BdJ3AfcrUyZIYzvubsJXDU5JeVqBOTAegZw3pLTM4jrizkuOr7mc1nhXXbxRBKbfuuMPxzP3oG0vmxD0SX8wVtaNTI4UT6FjxldrUIzW6nIAnVaEXComhBW7Jd7IX9soD7mGJ4epPKNzDMzf7cUjjMawdfpZdR%2BfSnbg59vcCdHNIqG1Uycsb55mdcRVobAPoUtUBSq6QuiMrknwWrI8GKkqndXDsZ3xLi3Z%2F6htPckWXWhiH2WCNE6AO4imGoCQ6zt7zk2GVoayp37DYwgbVQISFYA%3D--V1Q6owXXIRHv5ny1--SKLzWGWzt6kuvv5lethpXw%3D%3D; Expires=Mon, 26 Sep 2022 18:34:18 GMT; Path=/; Secure; HttpOnly; SameSite=Lax; Domain=isuganda.managebac.com""" or None

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
r = mbapi()
print(r)