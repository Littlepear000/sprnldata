from swxl.pandaspro.core import pwread
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

# Define Globals
dbpath = r'Q:\DATA\SPRNL\Users\Shelley\databases'
monameta = {
    ''
}

# Update Data in Local Drives
def monaupdate():
    global driver
    driver = webdriver.Edge()
    driver.get("https://www.imf.org/external/np/pdr/mona/Arrangements.aspx")
    time.sleep(15)
    for ele in driver.find_elements(By.XPATH, "//div[@class='whatIsThis']//td/a[text()!='Table Labels and Description']")[0:3]:
        print(f"Downloading {ele.text}")
        ele.click()
        time.sleep(45)
