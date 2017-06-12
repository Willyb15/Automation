import csv
import time
from selenium import webdriver
import selenium.webdriver.common.by as By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support  import expected_conditions as EC

def parseWaterfallTable(table):
    for index, item in list(enumerate(table)):
        text = item.text
        if text == "200 OK":
            return index

def gtMetrixLogin(l,p,gtMetric):
    browser.get(gtMetrix)
    browser.find_element_by_css_selector('a.site-nav-menu').click()
    WebDriverWait(browser,100).until(
        EC.presence_of_element_located((By.By.ID, 'li-email'))
    )
    browser.save_screenshot("test.png")
    browser.find_element_by_id('li-email').send_keys(l)
    browser.find_element_by_id('li-password').send_keys(p)
    browser.find_element_by_css_selector('div.form-buttons > button').click()
    WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.By.CSS_SELECTOR , 'h1.page-heading'))
    )

def findUrlTtfb(browser,urlToScan,gtMetrix,mobile):
    results = urlToScan.split()
    browser.get(gtMetrix)
    if mobile == "yes":
        browser.find_element_by_css_selector('a.analyze-form-options-trigger').click()
        WebDriverWait(browser, 100).until(
            EC.presence_of_element_located((By.By.ID, 'af-browser'))
        )
        Select(browser.find_element_by_css_selector('select#af-browser')).select_by_index(2)
        WebDriverWait(browser, 5)

    browser.find_element_by_css_selector('.js-analyze-form-url').send_keys(urlToScan)
    browser.find_element_by_css_selector('div.analyze-form-button button').click()
    WebDriverWait(browser,100).until(
        EC.presence_of_element_located((By.By.CLASS_NAME, 'report-waterfall'))
    )
    pagedetails = browser.find_elements_by_css_selector('span.report-page-detail-value')
    pageLoadTime = float(pagedetails[0].text.replace('s',''))
    totalPageSize = pagedetails[1].text
    if 'KB' in totalPageSize:
        totalPageSize = float(totalPageSize.replace('KB',''))/1000
    else:
        totalPageSize = float(totalPageSize.replace('MB',''))
    pageLoadRequestCount = float(pagedetails[2].text)

    iframe = browser.find_element_by_class_name('report-waterfall')
    print(iframe.get_attribute('src'))
    browser.get(iframe.get_attribute('src'))

    print(browser.current_url)
    WebDriverWait(browser,10).until(
        EC.presence_of_element_located((By.By.CLASS_NAME, 'pageName'))
    )
    waterfallNetStatus = browser.find_elements_by_css_selector('.netStatusLabel')
    index = parseWaterfallTable(waterfallNetStatus)
    waterfallNetReceiving = browser.find_elements_by_css_selector('.netReceivingBar')[index].value_of_css_property('width').replace('px','')
    waterfallNetWaiting = browser.find_elements_by_css_selector('.netWaitingBar')[index].value_of_css_property('width').replace('px','')
    waterfallNetTimeLabel = browser.find_elements_by_css_selector('span.netTimeLabel')[index].text
    if 'ms' in waterfallNetTimeLabel:
        waterfallNetTimeLabel = float(waterfallNetTimeLabel.replace('ms', ''))
    else:
        waterfallNetTimeLabel = float(waterfallNetTimeLabel.replace('s',''))*1000

    ttfb = float(waterfallNetWaiting) / float(waterfallNetReceiving) * waterfallNetTimeLabel
    results.append(ttfb)
    results.append(pageLoadTime)
    results.append(totalPageSize)
    results.append(pageLoadRequestCount)
    return results

gtMetrix = "https://gtmetrix.com/"
gtmLogin = "robot.sharecare@gmail.com"
gtmPass = "jameswang"
phantomJsLoc = r'c:\PATH\phantomjs.exe'
browser = webdriver.PhantomJS(phantomJsLoc) #Headless
#browser = webdriver.Chrome() #Visible
currDay = time.strftime("%m/%d/%Y")
currTime = time.strftime("%H:%M")

gtMetrixLogin(gtmLogin,gtmPass,gtMetrix)

with open(r'C:\Users\Mentos\Automated Reports\SEO - Page Speed Report - Daily\Inputs\Pages to Test.csv','r') as pageInputList, open(r'C:\Users\Mentos\Automated Reports\SEO - Page Speed Report - Daily\Raw Data\Page Speed Output.csv', 'a', newline='') as pageOutputList:
    pages = csv.reader(pageInputList)
    resultsPage = csv.writer(pageOutputList)
    failedPages = list([])
    for row in pages:
        print(row[0] + ":" + row[1])
        try:
            output = findUrlTtfb(browser,row[0],gtMetrix,"noMobile")
            #output.insert(0,currTime)
            output.insert(0,currDay)
            output.insert(6,row[1]) #need to edit when currTime added.
            output.insert(7, "Desktop")  # need to edit when currTime added.
            resultsPage.writerow(output)
            print(output)
        except:
            failedPages.append(row[0])
            print("Failed: " + row[0])
        WebDriverWait(browser,5)
        try:
            output = findUrlTtfb(browser,row[0],gtMetrix,"yes")
            #output.insert(0,currTime)
            output.insert(0,currDay)
            output.insert(6,row[1]) #need to edit when currTime added.
            output.insert(7, "Mobile")  # need to edit when currTime added.
            resultsPage.writerow(output)
            print(output)
        except:
            failedPages.append(row[0])
            print("Failed: " + row[0])

retryIterations = 0
while len(failedPages) > 1 and retryIterations <= 10:
    for i,page in enumerate(failedPages):
        try:
            output = findUrlTtfb(browser, page, gtMetrix)
            output.insert(0,currDay)
            resultsPage.writerow(output)
            print(output)
            del failedPages[i]
            time.sleep(10)
        except:
            if retryIterations < 10:
                print(page + ' failed. Retrying...')
            else:
                resultsPage.writerow(page)
    retryIterations += 1