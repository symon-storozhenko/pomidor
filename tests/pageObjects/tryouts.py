from pomidor.pomidor_runner import Pomidor

page_obj = Pomidor.get_page_objects("page_objects.csv")
print(page_obj)
print(page_obj.get("practice_page")[1])
