from selenium import webdriver
import selenium.common.exceptions as selenium_exceptions
import time
import requests
import os
import pprint
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def download_pdf(url, dst_path):
    r = requests.get(url, stream=True)
    with open(dst_path, 'wb') as fd:
        for chunk in r.iter_content(2000):
            fd.write(chunk)


def get_href_by_xpath(browser, xpath):
    try:
        pdf_href = browser.find_element_by_xpath(xpath).get_attribute('href')
    except EC.NoSuchElementException:
        pdf_href = None
    return pdf_href


def mkdir_(path):
    if os.path.isdir(path):
        return
    else:
        os.mkdir(path)


def waiting_with_xpath_click(browser, xpath):
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))
    browser.find_element_by_xpath(xpath).click()


# zhengxiawu_list = [{'index': 68, 'title': 'Dense auto-encoder hashing for robust cross-modality retrieval'}]
zhengxiawu_list = [{'index': 68, 'title': 'Dense auto-encoder hashing for robust cross-modality retrieval'}]
browser = webdriver.Chrome(executable_path='/Users/sherwood/.local/chromedriver')
dst_dir = '/Users/sherwood/Desktop/2020杰青+科学探索奖/引用查询/郑侠武部分文件夹'
for paper in zhengxiawu_list:
    this_paper_information = {'title': paper['title']}
    # create the folder
    this_paper_dir_name = os.path.join(dst_dir, str(paper['index']) + ' ' + paper['title'])
    mkdir_(this_paper_dir_name)
    browser.get('https://scholar.google.com')
    browser.set_window_size(800, 1000)
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="gs_hdr_tsi"]').send_keys(paper['title'])
    waiting_with_xpath_click(browser, '//*[@id="gs_hdr_tsb"]')
    waiting_with_xpath_click(browser, '//*[@id="gs_res_ccl_mid"]/div/div[2]/div[3]/a[2]')
    time.sleep(4)
    this_paper_apa_text = browser.find_element_by_xpath('//*[@id="gs_citt"]/table/tbody/tr[3]/td/div').text
    waiting_with_xpath_click(browser, '//*[@id="gs_cit-x"]')
    pdf_href = get_href_by_xpath(browser, '//*[@id="gs_res_ccl_mid"]/div/div[1]/div/div/a')
    this_paper_information['apa'] = this_paper_apa_text
    this_paper_information['pdf_href'] = pdf_href
    waiting_with_xpath_click(browser, '//*[@id="gs_res_ccl_mid"]/div/div[2]/div[3]/a[3]')
    this_paper_information['reference'] = []
    flag = True
    while flag:
        elements = browser.find_elements_by_xpath('//*[@id="gs_res_ccl_mid"]//div[@class="gs_r gs_or gs_scl"]')
        ele_length = len(elements)
        del elements
        for i in range(ele_length):
            # elements = browser.find_elements_by_xpath('//*[@id="gs_res_ccl_mid"]//div[@class="gs_r gs_or gs_scl"]')
            # element = browser.find_element_by_xpath('//*[@id="gs_res_ccl_mid"]/div[{}]'.format(str(i+1)))
            # _a = element.find_element_by_xpath('//h3//a')
            _a = browser.find_element_by_xpath('//*[@id="gs_res_ccl_mid"]/div[{}]/div[@class="gs_ri"]/h3/a'.format(str(i+1)))
            reference_paper_name = _a.text
            print(reference_paper_name)
            reference_paper_href = get_href_by_xpath(browser, '//*[@id="gs_res_ccl_mid"]/div[{}]/div[1]/div/div/a'.
                                                     format(str(i+1)))
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="gs_res_ccl_mid"]/div[{}]/div[@class="gs_ri"]/div[3]/a[2]'.format(str(i+1))).click()
            # element.find_element_by_xpath('//a[@class="gs_or_cit gs_nph"]').click()
            time.sleep(4)
            reference_paper_apa_text = browser.find_element_by_xpath('//*[@id="gs_citt"]/table/tbody/tr[3]/td/div').text
            browser.find_element_by_xpath('//*[@id="gs_cit-x"]').click()
            this_paper_information['reference'].append({
                "name": reference_paper_name,
                "href": reference_paper_href,
                "apa": reference_paper_apa_text
            })
        try:
            button = browser.find_element_by_xpath('//*[@id="gs_nm"]/button[2]')
            button_onclick = button.get_attribute('onclick')
            if len(button_onclick) > 0:
                button.click()
            else:
                flag = False
        except EC.NoSuchElementException:
            flag = False
        # try:
        #
        #     browser.find_element_by_xpath('//*[@id="gs_nm"]/button[2]').click()
        #     time.sleep(4)
        #     flag = True
        # except WebDriverException:
        #     flag = False
    json.dump(this_paper_information, open(os.path.join(this_paper_dir_name, 'info.json'), 'w+'))
    pprint.pprint(this_paper_information)
