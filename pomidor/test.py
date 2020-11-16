from pomidor.pomidor_init import BrowserInit, PomidorObjAndURL

pomi = BrowserInit("Chrome", 'https://pomidor-automation.com/')
# driver = pomi.define_browser()
# with driver as d:
#     d.get('https://pomidor-automation.com/practice/')

d = {}
d["ff"] = "eferf", "fvdvfdv"
print(d)

pom_obj = PomidorObjAndURL("page_objects.csv")

print(pom_obj.get_page_objects())