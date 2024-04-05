from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from findFilesAndMove import findFilesAndMove
import time
import json
import traceback

with open(r'settings.json','r') as f: 
    settings = json.load(f)

# driver settings, driver path & url

service = Service(executable_path= settings['webDriverPath'])
options = webdriver.EdgeOptions()

if settings['isHidden']:
    options.use_chromium = True
    options.add_argument("headless")
    options.add_argument("disable-gpu")
try:
    driver = webdriver.Edge(service = service , options = options)
    driver.get(settings['url'])

    wait = WebDriverWait(driver,10)

    # Login procedures
    username_f = wait.until(EC.presence_of_element_located((By.NAME,"username")))
    password_f = driver.find_element(By.NAME,"password")
    
    username_f.send_keys(settings['username'])
    password_f.send_keys(settings['password'])
    driver.find_element(By.CSS_SELECTOR,'input[type="submit"]').click()
    
    # Downloading reports -> This part may cause problem in future
    reports = wait.until(EC.element_to_be_clickable((By.ID,'TAI_Reports')))
    reports.click()
    
    change_report = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="My Enovia"]/div[2]/ul/li[4]/ul/li[1]/a/label'))) #If "redacted" element's place order change, it will not find any element.
    change_approval_report = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="My Enovia"]/div[2]/ul/li[4]/ul/li[2]/a/label')))
    change_report.click()
    change_approval_report.click()
    
    
    if not findFilesAndMove(settings['reportName'], settings['downloadPath'], settings['destinationPath']):
        raise Exception(str(settings['reportName']) + " couldnt find.")
    
    if not findFilesAndMove(settings['reportName2'], settings['downloadPath'], settings['destinationPath']):
        raise Exception(str(settings['reportName2']) + " couldnt find.")
        
    with open(settings['destinationPath']+ '\\' + "Completion_Report.txt",'w') as f:
        f.write(time.strftime("%d.%m.%y %H:%M:%S",time.localtime()) + " \n Report was successfully completed.")
        
    print(time.strftime("%d.%m.%y %H:%M:%S",time.localtime()) + " \nReport was successfully completed.")
    
    driver.quit()
    
except Exception as e:
    print(e)
    with open(settings['destinationPath']+ '\\' + "Error_Report.txt",'w') as f:
        traceback_str = traceback.format_exc()
        f.write(str(e) + "\n\n" + str(traceback_str) )
        
    driver.quit()

# # BACKLOG:
#     Web sayfaları indirme bitince kapanmalı, +
#     Raporlar indikten sonra seçilen directory e taşınmalı +
#     Raporlar taşındıktan sonra veya önce isimlendirilmeli -