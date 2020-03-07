# -*- coding: UTF-8 -*-
from docx import Document
import time
import random
import glob
import os, json
dir_name = '/Users/sherwood/Desktop/2020杰青+科学探索奖/引用查询/郑侠武部分文件夹/'
dir_list = glob.glob(dir_name + '*')
dir_list.sort()
for i in dir_list:
    print(i)
    id = int(i.split('/')[-1][0:2])
    info_array = json.load(open(os.path.join(i, 'info.json')))
    save_name = os.path.join(i, str(id) + ' ' + info_array['title'] + '.docx')
    # create docx
    document = Document()
    table = document.add_table(rows=3+5*len(info_array['reference']), cols=1)
    table.style = 'TableGrid'
    table.rows[0].cells[0].text = "被引用论文：通讯  谷歌他引："
    table.rows[1].cells[0].text = info_array['apa']
    for j in range(len(info_array['reference'])):
        table.rows[3+5*j].cells[0].text = "引用论文"+str(j+1)
        table.rows[4 + 5 * j].cells[0].text = info_array['reference'][j]['apa']
        table.rows[5 + 5 * j].cells[0].text = "引用出处：[ ]"
    document.save(save_name)
    pass
