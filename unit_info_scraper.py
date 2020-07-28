from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import date
import time
import sys
import pandas as pd

def getUnitPage(unit_code):
    today = date.today()
    year = today.strftime("%Y") # Get the current year
    driver.get("https://handbook.monash.edu/" + year + "/units/" + unit_code)
    
def getUnitTitle():  # Fetch unit name and code
    introContainer = driver.find_element_by_id('intro-container').text  # Get unit code and title info
    introContainerLines = introContainer.split('\n') 
    # Assumes all unit codes are 7 characters
    unitCode = introContainerLines[2][0:7]  
    unitName = introContainerLines[2][10:]
    return(unitCode, unitName)

def getSemestersOffered():
    offerings = driver.find_element_by_id('Offerings').text  # Get semesters offered info
    offeringsLines = offerings.split('\n')
    semesters = sorted({line[:2] for line in offeringsLines if line[0] == 'S'}) 
    return semesters


def getUnitCoordinatorsDetails(): 
    unitCoordinator = driver.find_element_by_id('UnitCoordinator(s)').text  # Get unit coordinator info
    unitCoordinatorLines = unitCoordinator.split('\n') 
     # Doesn't work for unit coordinators with no title, e.g. works for Mr John Doe, but not John Doe
     # Doesn't really matter too much, most have titles, and if not can copy from email anyway
    unitCoordinatorNames = [line for line in unitCoordinatorLines if line.count(' ') > 1]
    unitCoordatorEmails = [line for line in unitCoordinatorLines if "@" in line]
    return(unitCoordinatorNames, unitCoordatorEmails)

def getinfo(fileName):
    file = open(fileName,'r')
    array=[]
    for line in file:
        try:
            unitCode = line.strip()
            print("Getting Record for " + unitCode)
            print("Waiting a few seconds, don't want to overload the servers now do we?")
            time.sleep(10)

            getUnitPage(unitCode)
            # print(driver.page_source)  # Uncomment this to view the html of the unit page
            unitCode, unitName = getUnitTitle()
            semesters = getSemestersOffered()
            semesters = ", ".join(semesters)
            unitCoordinatorNames, unitCoordatorEmails = getUnitCoordinatorsDetails()
            unitCoordinatorNames = ", ".join(unitCoordinatorNames)
            unitCoordatorEmails = ", ".join(unitCoordatorEmails)
            pair=[unitCode,semesters,unitName,unitCoordinatorNames,unitCoordatorEmails]
            array.append(pair)
        except:
            print("Error retrieving info for: ", line)
            continue
    return array


if __name__ == "__main__":
    # Initialise webscraper
    unitCodeFile = sys.argv[1]
    options = Options()
    options.add_argument("--headless")  # Make browser headless, that is don't show graphical interface.
    driver = webdriver.Firefox(options=options)  # Firefox gecko driver located in /usr/bin
    driver.implicitly_wait(20) # Ensure don't scrape for elements before page has loaded fully in

    # Extract unit info and output in csv file
    unitInfo = getinfo(f"/home/lo/Desktop/webscraper/{unitCodeFile}")
    df = pd.DataFrame(unitInfo, columns = ['Unit Code', 'Semester(s) offered', 'Unit Name', 'Unit Coordinator(s)', 'Contact(s)'])
    df.to_csv(unitCodeFile.split(".")[0] + ".csv")

    driver.quit()
    
   

