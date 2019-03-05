import pickle
import time
import sys
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from RouteParser import ParseProblem
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def checkForCookies(browser):
    # Check if cookies exist and load them if they do. Manually log in otherwise
    if (Path("Data/cookies2.pkl").exists()):
        print("HERE!")
        cookies = pickle.load(open("Data/cookies2.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
        browser.refresh()
        WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.ID, "Holdsetup")))
    else:
        WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.ID, "Holdsetup")))
        pickle.dump(browser.get_cookies(), open("Data/cookies2.pkl", "wb"))
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "lProblems")))

def navigateToProblemsPage(browser, holdsetupString):
    browser.find_element_by_id("lProblems").click()
    browser.find_element_by_id("m-viewproblem").click()
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "Holdsetup"))
    )
    select = Select(browser.find_element_by_id("Holdsetup"))
    select.select_by_visible_text(holdsetupString)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "moonboard")))

def checkValues(importantNumbers, file):
    if importantNumbers["problemsVisited"] == importantNumbers["totalProblemsNum"]:
        endProcess(file, importantNumbers)

    elif importantNumbers["problemsVisited"] + 15 > importantNumbers["totalProblemsNum"]:
        importantNumbers["problemsOnPage"] = totalProblemsNum - problemsVisited + 1

    if (importantNumbers["problemsVisited"] / importantNumbers["onePercent"] >= importantNumbers["previousPercentage"]
            and importantNumbers["previousPercentage"] != 100):
        print("{}% completed\n{} problems logged\n".format(importantNumbers["previousPercentage"], importantNumbers["problemsLogged"]))
        importantNumbers["previousPercentage"] += 1

def getAllProblems(range1, range2, importantNumbers, pathToProblem1,pathToProblem2, pathToMenuNumbers, updateNums = False, file = None):
    for i in range(range1, range2):
        for j in range(1, importantNumbers["problemsOnPage"]):
            try:
                importantNumbers["problemsVisited"] += 1
                link = browser.find_element_by_xpath(
                    pathToProblem1.format(j)).get_attribute(
                    'href')
                problemsFile.write(json.dumps(ParseProblem(link)) + ',\n')
                importantNumbers["problemsLogged"] += 1

        # NoSuchElementException is raised on benchmark problems due to a different xpath format
            except NoSuchElementException:
                link = browser.find_element_by_xpath(
                    pathToProblem2.format(j)).get_attribute(
                    'href')
                problemsFile.write(json.dumps(ParseProblem(link)) + ',\n')
                importantNumbers["problemsLogged"] += 1

        # If unknown exception is thrown on a problem, skip it (Like 404 errors)
            except Exception as e:
                print(e)
                continue

            if (updateNums):
                checkValues(importantNumbers, file)

        xpathString = pathToMenuNumbers.format(i)
        browser.find_element_by_xpath(xpathString).click()

def getTotalProblemsAndWriteToFile(importantNumbers, problemsFile):
    totalProblems = browser.find_element_by_id("totalProblems").text
    tempNum = int((browser.find_element_by_id("totalProblems").text).split(' ')[0])
    importantNumbers["totalProblemsNum"] = tempNum
    importantNumbers["onePercent"] = tempNum*0.01
    problemsFile.write("{}\n".format(totalProblems))

def endProcess(problemsFile, importantNumbers):
    problemsFile.close()
    print("Done\n{} problems logged\n".format(importantNumbers["problemsLogged"]))
    sys.exit()

xpathProblemNoFail = '//*[@id="grdProblems"]/div[2]/table/tbody/tr[{}]/td/div/div[1]/h3/a'
xpathProblemYesFail = '//*[@id="grdProblems"]/div[2]/table/tbody/tr[{}]/td/div/div[2]/h3/a'
xpathMenuNums = '//*[@id="grdProblems"]/div[3]/ul/li[{}]/a'


if __name__ == "__main__":
    browser = webdriver.Chrome('/usr/local/bin/chromedriver')
    browser.get("https://www.moonboard.com/Dashboard/Index")
    importantNumbers = {"problemsVisited": 0, "problemsLogged": 0, "problemsOnPage": 16, "totalProblemsNum": 0,
                        "onePercent": 0, "previousPercentage": 1}
    s   (browser)

    navigateToProblemsPage(browser,"MoonBoard Masters 2017")

    problemsFile = open("Data/problems.txt", 'w', encoding='utf-8')
    getTotalProblemsAndWriteToFile(importantNumbers, problemsFile)

# Parse first 45 problems (No back button for these pages so xpath is slightly different for the buttons on the bottom)
    getAllProblems(3,6,importantNumbers, xpathProblemNoFail, xpathProblemYesFail, xpathMenuNums)

# Parse remaining problems
    try:
        while (True): #End of File Process in function
            getAllProblems(4, 7, importantNumbers, xpathProblemNoFail, xpathProblemYesFail, xpathMenuNums, True)

    except Exception as e:
        print(e)
        problemsFile.close()

