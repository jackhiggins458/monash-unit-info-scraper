from selenium import webdriver
from selenium.webdriver.firefox.options import Options


options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)  # Firefox gecko driver located in /usr/bin
driver.implicitly_wait(20)  # Make sure don't extract elements before page finished loading


faculties = ["sci", "eng", "it", "arts"]

for faculty in faculties:
    # Uses 2019 unit guide, its in a much easier access format than the new 2020 one. 
    driver.get("https://www3.monash.edu/pubs/2019handbooks/units/index-byfaculty-" + faculty + ".html")
    #print(driver.page_source)
    facultyUnitCodesElements = driver.find_elements_by_class_name("fixed")
    facultyUnitCodesList = []
    f = open(f"{faculty}.txt", "w+")
    for unit in facultyUnitCodesElements:
        facultyUnitCodesList.append(unit.text)
        f.write(unit.text + "\n")

    #print(facultyUnitCodesList)
    #print(len(facultyUnitCodesList))

f.close()
driver.quit()