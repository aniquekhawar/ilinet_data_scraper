from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import time
import glob
import os
from zipfile import ZipFile
import pandas as pd

# commands to get the current directory (which is usually the directory to the Git Repository)
parent_directory = os.path.dirname(os.path.realpath(__file__))
print(parent_directory)

def remove_zips(parent_directory):
    remove_zips = glob.glob(f'{parent_directory}/*.zip')
    for filePath in remove_zips:
        try:
            os.remove(filePath)
            print(f'File at {filePath} removed successfully.')
        except:
            print('Error while deleting file: ', filePath)
remove_zips(parent_directory)

opts = Options()
opts.add_argument("--headless")
opts.set_preference("browser.download.folderList", 2)
opts.set_preference("browser.download.manager.showWhenStarting", False)
opts.set_preference("browser.download.dir", parent_directory)
opts.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options = opts)

url = 'https://gis.cdc.gov/grasp/fluview/fluportaldashboard.html'
browser.get(url)
time.sleep(5)

disclaimer_ok_btn = '//*[@id="ngdialog1"]/div[2]/div/div[3]/button[1]'
browser.find_element('xpath', disclaimer_ok_btn).click()
print('Disclaimer button clicked')
time.sleep(3)

download_btn = '//button[@title="Download Data"]'
browser.find_element('xpath', download_btn).click()
print('Clicked Initial Download Data Button')
time.sleep(1)

who_nrevss_xpath = '//input[@ng-model="dataSource.isWHO"]'
uncheck1 = browser.find_element('xpath', who_nrevss_xpath)
if uncheck1.is_selected():
    uncheck1.click()
    print('Unchecked WHO/NREVSS Option from Download pane')

ilinet_xpath = '//input[@ng-model="dataSource.isILINet"]'
check1 = browser.find_element('xpath', ilinet_xpath)
if not check1.is_selected():
    check1.click()
    print('Checked ILINet Option from Download pane')

state_radio_xpath = '//input[@id="5"]'
browser.find_element('xpath', state_radio_xpath).click()
print('Clicked State option Radio-button')
time.sleep(2)

regions_checkbox_xpath = '//input[@ng-model="isAllRegions"]'
regions_checkbox = browser.find_element('xpath', regions_checkbox_xpath)
if not regions_checkbox.is_selected():
    regions_checkbox.click()
    print('Checked all regions checkbox')
time.sleep(5)

seasons_checkbox_xpath = '//input[@ng-model="isAllSeasons"]'
seasons_checkbox = browser.find_element('xpath', seasons_checkbox_xpath)
if not seasons_checkbox.is_selected():
    seasons_checkbox.click()
    print('Checked all seasons checkbox')
time.sleep(5)

download_data_xpath = '//button[@class ="btn btn-success"]' # probably needs to be redefined
browser.find_element('xpath', download_data_xpath).click()
print('Successfully downloaded data')
time.sleep(10) # 10 second delay to ensure data is downloaded
browser.close()

# this is subject to change
filename = 'FluViewPhase2Data.zip'

try:
    zip_file = ZipFile(filename)
    print('Reading in CSV File from Zipfile')
    ili_df = pd.read_csv(zip_file.open('ILINet.csv'), skiprows = 1)
    print('Saving CSV File')
    ili_df.to_csv('ILINet_Data.csv', index = False)
except:
    print('Unable to locate FluViewPhase2Data.zip in current directory.')

# clean up zipfiles
remove_zips(parent_directory)