import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import shutil
import os
from sprnldata.downloads import mona_root

monatabs = [
    'Description',
    'Purchases',
    'Reviews',
    'QPC',
    'QPCandIndTarg',
    'Combined'
]

def mona_download():
    driver = webdriver.Edge()
    time.sleep(3)
    driver.get("https://www.imf.org/external/np/pdr/mona/Arrangements.aspx")
    time.sleep(3)
    for ele in driver.find_elements(By.XPATH,"//div[@class='whatIsThis']//td/a[text()!='Table Labels and Description']"):
        print(f"Downloading {ele.text}")
        ele.click()
        time.sleep(45)
    print('''

===================================
    Step 1 Completed. Files Downloaded
    ''')
    # version = versiongui.get()
    # for file_name in monatabs:
    #     new_file_name = file_name + '_' + version + '.xlsx'
    #     print(new_file_name, file_name)
    #     shutil.move(os.path.join(downloads_path, file_name + '.xlsx'), os.path.join(target_path, new_file_name))
    # print('Step 2 Completed. Files Saved in MONA Database Path')

if __name__ == '__main__':
    driver = webdriver.Edge()
    time.sleep(3)
    driver.get("https://www.imf.org/external/np/pdr/mona/Arrangements.aspx")
    time.sleep(3)
    # for ele in driver.find_elements(By.XPATH,
    #                                 "//div[@class='whatIsThis']//td/a[text()!='Table Labels and Description']"):
    #     print(f"Downloading {ele.text}")
    #     ele.click()
    #     time.sleep(45)