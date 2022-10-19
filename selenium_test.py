# librerias e importes

import locale
import os
import sys
import time

import unidecode as unidecode
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from loaddatatod_db import load_data_mongo


locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))


directory="D:\\ETL\\"

# time.sleep(10)

# Opciones de navegación

options = webdriver.ChromeOptions()
prefs = {
    'download.default_directory' : directory,
    'profile.default_content_setting_values.automatic_downloads': 1
}

options.add_experimental_option('prefs', prefs)
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('ignore-certificate-errors')
options.add_experimental_option("prefs", prefs)

#Dirección de driver selenium


try:
    os.makedirs(directory, mode=0o666, exist_ok=True)
except OSError as e:
    sys.exit("Can't create {dir}: {err}".format(dir=directory, err=e))


driver_path = 'driver_selenium\\105_chromedriver.exe'

driver = webdriver.Chrome(driver_path, chrome_options=options)

#Esconder ventana del navegador
# driver.set_window_position(-10000,0)

#Iniciar en pantalla

driver.maximize_window
time.sleep(1)

#URL destino

driver.get('https://app.powerbi.com/view?r=eyJrIjoiOTk3NDZhYTMtZjg5NC00OWIxLWE3NmItOTIzYjdlZmFmNmJhIiwidCI6IjU2MmQ1YjJlLTBmMzEtNDdmOC1iZTk4LThmMjI4Nzc4MDBhOCJ9&pageName=ReportSection')
time.sleep(4)


def getDownLoadedFileName(waitTime):
    driver.execute_script("window.open()")
    # switch to new tab
    driver.switch_to.window(driver.window_handles[-1])
    # navigate to chrome downloads
    driver.get('chrome://downloads')
    # define the endTime
    endTime = time.time()+waitTime
    while True:
        try:
            # get downloaded percentage
            downloadPercentage = driver.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            if downloadPercentage == 100:
                # return the file name once the download is completed
                return driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
        except:
            pass
        time.sleep(1)
        if time.time() > endTime:
            break

def check_exists_by_xpath(element, xpath):
    try:
        element.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def dataMongo(users,titles,ano):
        list = []
            #print(users)
        for y in users:
             # drop.select_by_visible_text("2019")
             item = dict()
             # print(y.text)
             cells = y.text.split("\n")
             acumulator = 0
             for x in titles:
                 # print(x.text)
                 item[x.text] = unidecode.unidecode(cells[acumulator])
                 list.append(item)
                 acumulator += 1

             item['año']=ano
             load_data_mongo(item, "scrap")
        #Cerrar navegador
        print(list)



def iterate(xpath_menu_one_row):
    years = driver.find_elements("xpath",xpath_menu_one_row)

    x_ant = None
    x_act = None
    for i, x in enumerate(years):

        print(i, x.text)

        x_ant = x
        x_ant = x.click()
        time.sleep(3)
        users = driver.find_elements("xpath", "//div[@class='innerContainer']/div[@class='bodyCells']/div/div")
        titles_xpath = "//div[@class='tableExContainer']/div[@class='tableEx']/div[@class='innerContainer']/div[@class='columnHeaders']/div/div"
        titles = driver.find_elements("xpath", titles_xpath)
        dataMongo(users,titles,x.text)
        #time.sleep(3)
        x_act = x
        x_act = x.click()

    time.sleep(3)
    years = driver.find_elements("xpath", xpath_menu_one_row)
    years[11].location_once_scrolled_into_view

    time.sleep(3)
    years = driver.find_elements("xpath",xpath_menu_one_row)

    for i, x in enumerate(years):
        print(i, x.text)
        x_ant = x
        x_ant = x.click()
        time.sleep(0.5)
        # dataMongo(users)
        x_act = x
        x_act = x.click()

    time.sleep(5)
#def last_item_uncheked(xpath_menu_one_row):
    #years = driver.find_elements("xpath", xpath_menu_one_row)
    #time.sleep(5)
    #years[11].location_once_scrolled_into_view
    #time.sleep(3)
    #years[13].location_once_scrolled_into_view
    #years = driver.find_elements("xpath", xpath_menu_one_row)
    #years.click()
    #time.sleep(3)
    #for i, x in enumerate(years):
    #    print(i, x.text)
    #    if x.text == '2021':
    #        x.click()
    #years = driver.find_elements("xpath", "//div[@class='slicer-dropdown-content']/div[@class='slicerContainer isMultiSelectEnabled']/div[@class='slicerBody']/div[@class='scroll-wrapper scrollbar-inner']/div[@class='scrollbar-inner scroll-content scroll-scrolly_visible']/div[@class='scrollRegion']/div[@class='visibleGroup']/div[@class='row']")
    #driver.execute_script("return arguments[0].scrollIntoView(true);", years)
    #driver.execute_script("arguments[0].scrollIntoView()", years)
    #driver.execute_script("scroll(0, 0);")
    #driver.execute_script("window.scrollTo(0,document.body.scrollHeight);", years)
    #years[0].location_once_scrolled_into_view
    #time.sleep(3)


time.sleep(5)
if __name__ == '__main__':

    try:

        titles_xpath = "//div[@class='tableExContainer']/div[@class='tableEx']/div[@class='innerContainer']/div[@class='columnHeaders']/div/div"
        titles= driver.find_elements("xpath",titles_xpath)
        users = driver.find_elements("xpath","//div[@class='innerContainer']/div[@class='bodyCells']/div/div")
        combobox = driver.find_element("xpath","//*[@id='pvExplorationHost']/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[6]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div/i")
        combobox.click()
        #time.sleep(5)
        xpath_menu_anos="//div[@class='slicer-dropdown-content']/div[@class='slicerContainer isMultiSelectEnabled']/div[@class='slicerBody']/div[@class='scroll-wrapper scrollbar-inner']/div[@class='scrollbar-inner scroll-content scroll-scrolly_visible']/div[@class='scrollRegion']/div[@class='visibleGroup']/div[@class='row']"
        #last_item_uncheked(xpath_menu_anos)
        time.sleep(3)
        iterate(xpath_menu_anos)

        #time.sleep(5)




    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
        sys.exit()

