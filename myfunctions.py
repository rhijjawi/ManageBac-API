import requests as req
from bs4 import BeautifulSoup
from rich import print
cal = {"Jan": 1,"Feb": 2,"Mar": 3,"Apr": 4,"May": 5,"Jun": 6,"Jul": 7,"Aug": 8,"Sep": 9,"Oct": 10,"Nov": 11,"Dec": 12,}

class NoDomain(Exception):
    def __init__(self, message="""Make sure you defined the domain in the function. main("domain", "cookie")\nEx:run("myschool",cookie) OR run("myschool.managebac.com",cookie)"""):
        self.message = message
        super().__init__(self.message)

class NoCookie(Exception):
    def __init__(self, message="""Make sure you defined the cookie in the function. main("domain", "cookie")\nEx:run(domain,"0sjd8cho1oasd98afashvas9qryt8q3845iqengfiehr")"""):
        self.message = message
        super().__init__(self.message)

def run(domain:str=None, cookie:str=None):
    """
    Param DOMAIN: the subdomain of your FariaOne ManageBac site (The ****. part of ****.managebac.com)
    Param COOKIE: Your MB authentication cookie (it's called _managebac_session) that you can find by pressing F12, then clicking Storage, and Cookies. (Only the value!)
    """
    def cookiecheck(cookie):
        if len(cookie)>30:
            print("all good")
            
    def domaincheck(domain):
        if domain.endswith("""managebac.com"""):
            domain = domain.replace(".managebac.com",'')
    if domain == None and cookie == None:
        domain = input("""What is the subdomain of your school's ManageBac site?\nEnter ONLY the subdomain (****).managebac.com""")
    elif domain != None and cookie == None:
        raise NoCookie
    elif domain == None and cookie != None:
        raise NoDomain
    cookiecheck(cookie)
    try:
        cook = {"_managebac_session": f"{cookie}", "hide_osc_announcement_modal" : "true"}
        tasks = {}
        for i in range(1,4):
            r = req.get(f"https://{domain}.managebac.com/student/tasks_and_deadlines?upcoming_page={i}",cookies=cook)
            soup = BeautifulSoup(r.content, "html.parser")
            results = soup.find(class_="upcoming-tasks")

            #print(results)
            try:
                tasks = results.find_all("div", class_="line task-node anchor js-presentation")
                deadlines = results.find_all("div", class_="line")
            except Exception as e:
                print(e)
                tasks = results.find_all("div", class_="line")
            #tasks = soup.find_all("div", data-id=lambda value: value and value.startswith("#core-task"))
            for task in tasks:
                day = task.find("div", class_="day").text
                month = task.find("div", class_="month").text
                title = task.find("h3", class_="title")
                title = title.find("a").text
                print(f"[red]Task due: {day}/{cal[f'{month}']}/2021[/red]")
                print(f"[yellow]{title}[/yellow]")
                print()
            for task in deadlines:
                title = task.find("h4", class_="title")
                if title != None:
                    title = title.find("a").text
                    datebadge = task.find("div", class_="date-badge")
                    day = datebadge.find("div", class_="day").text
                    month = datebadge.find("div", class_="month").text
                    print(f"[green]Task due: {day}/{cal[f'{month}']}/2021[/green]")
                    print(f"[yellow]{title}[/yellow]")
                    print()
            del(tasks, soup, results, r)
    except Exception as e:
        print(e)        
run(domain, cookie)