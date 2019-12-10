#!/usr/bin/env python
# encoding: utf-8

# @author: Zhipeng Ye
# @contact: Zhipeng.ye19@xjtlu.edu.cn
# @file: segment_file.py
# @time: 2019-12-09 15:37
# @desc:

import datetime
import random
import re
from io import StringIO

from bs4 import BeautifulSoup


def write_html_into_disk(html_text):
    # set time
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    # random factor
    suffix = str(random.randint(1, 1000))

    file_name = time_str + suffix + '.txt'

    with open('/Users/geekye/Documents/Dataset/corpus/text' + file_name, 'w') as file:
        file.write(html_text)


if __name__ == "__main__":

    time_start = datetime.datetime.now()
    with open('/Users/geekye/Documents/Dataset/corpus/SogouT.mini.txt', 'r') as file:

        # segment
        html_content = []
        for line in file:
            if '<DOC>' in line or '<DOCNO>' in line or '<URL>' in line:
                continue

            if '</DOC>' not in line:
                html_content.append(line)

            if '</DOC>' in line:
                html_value = ''.join(html_content)

                html_doc = html_value.encode('utf-8')

                soup = BeautifulSoup(html_doc, 'html.parser')

                html_text = soup.text

                # remove js and css
                info = [s.extract() for s in soup('script') or s in soup('style')]

                for script_content in info:
                    html_text = html_text.replace(script_content.text, '')

                lines = html_text.split('\n')

                html_text_list = []

                for s in lines:
                    line_content = s.strip()
                    if line_content != '' and None is not re.match('^[\u4e00-\u9fa5]{1,}$', line_content):
                        html_text_list.append(line_content)

                html_text = '\n'.join(html_text_list)

                if html_text != '':
                    # write html into files of disk
                    write_html_into_disk(html_text)

                # reset stringIO
                html_content = []
                continue

    time_stop = datetime.datetime.now()

    print('time:',time_stop-time_start)
