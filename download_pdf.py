import glob
from selenium import webdriver
import time
import json
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scihub.scihub import SciHub
import requests
import tqdm


def waiting_with_xpath_click(browser, xpath):
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))
    browser.find_element_by_xpath(xpath).click()


def get_url(href, name):
    if href is not None:
        return href
    else:
        browser = webdriver.Chrome(executable_path='/Users/sherwood/.local/chromedriver')
        browser.get('https://sci-hub.tw')
        browser.find_element_by_xpath('//*[@id="input"]/form/input[2]').send_keys(name)
        waiting_with_xpath_click(browser, '//*[@id="open"]')
        time.sleep(4)
        WebDriverWait(browser, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="plugin"]')))
        href = browser.find_element_by_xpath('//*[@id="plugin"]').get_attribute('src')
        browser.close()
        return href


def down_pdf(url, dst):
    if os.path.isfile(dst):
        return True
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    proxies = {"http": "http://127.0.0.1:1087",}
    if url is not None:
        try:
            print("download " + url)
            r = requests.get(url, stream=True, headers=header, proxies=proxies)
            with open(dst, 'wb') as fd:
                for chunk in tqdm.tqdm(r.iter_content(20000)):
                    fd.write(chunk)
            return True
        except requests.exceptions.SSLError:
            return False
        except requests.exceptions.ConnectionError:
            return False


dir_name = '/Users/sherwood/Desktop/2020杰青+科学探索奖/引用查询/郑侠武部分文件夹/'
dir_list = glob.glob(dir_name + '*')
dir_list.sort()
sh = SciHub()
for i in dir_list:
    print(i)
    id = int(i.split('/')[-1][0:2])
    info_array = json.load(open(os.path.join(i, 'info.json')))
    #this_paper_href = get_url(info_array['pdf_href'], info_array['title'])
    save_name = os.path.join(i, str(id) + ' ' + info_array['title'] + '.pdf')
    down_pdf(info_array['pdf_href'], save_name)
    for j in range(len(info_array['reference'])):
        print(j)
        save_name = os.path.join(i, '引用论文' + str(j+1) + '.pdf')
        print(down_pdf(info_array['reference'][j]['href'], save_name))