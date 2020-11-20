from pomidor.pomidor_init import BrowserInit, PomidorObjAndURL, Pom

# pomi = BrowserInit("Chrome", 'https://pomidor-automation.com/')
# driver = pomi.define_browser()
# with driver as d:
#     d.get('https://pomidor-automation.com/practice/')

d = {}
d["ff"] = "eferf", "fvdvfdv"
print(d)

pomi = PomidorObjAndURL("page_objects.csv", urls_file="ok.csv")
print(pomi.get_obj_param("practice_page"))
print(pomi.addt_urls())

po2 = Pom("Chrome", 'https://pomidor-automation.com/', "page_objects.csv",
          urls="ok.csv")


