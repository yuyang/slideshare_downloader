#!/usr/bin/python2
#coding:utf-8
# SCRIPT: slideshare_downloader.py
# AUTHOR: DARK_LBP
# MAIL: jtrkid@gmail.com
# DATE: 2013/06/09
# REV: 0.6
# PURPOSE:
# Download Document images from slideshare and convert to pdf format.
# Need imagemagick to convert to pdf
# Use Age:
# ./slideshare_downloader.py -p http://127.0.0.1:8086 -s \
# http://www.slideshare.net/thegaragegroup/new-approaches-to-business-model-innovation \
# -f abc.pdf

import pycurl
import StringIO
import os
import sys
import argparse
import re


parser = argparse.ArgumentParser(description='该工具用于下载slideshark上的文档并转为pdf格式.')   # This and preceding 4 lines used to control the arguments entered in the CLI.
parser.add_argument('-f', action="store", dest='file_name', help='pdf文件的名称')
parser.add_argument('-s', action="store", dest='url', help='文档的URL')

args = parser.parse_args()


if len(sys.argv) == 1:  # 当用户没有输入任何参数时显示帮助并退出
    parser.print_help()
    sys.exit(1)
args = vars(args)   # converts the arguments into dictionary format for easier retrieval.


def get_img_url(html):
    m = re.search(r'full="(http://image\.slidesharecdn\.com/.*?)-1-1024\.jpg\?', html)
    return m.group(1)

def get_pages(html):
    pages = re.findall('"slide_count":\d*', html)
    pages = re.findall(r'\d+$', pages[0], re.M)
    pages = int(pages[0])
    return pages

def get_result(url):
    buf = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(c.CONNECTTIMEOUT, 5)
    c.setopt(c.TIMEOUT, 8)
    c.perform()
    html = buf.getvalue()
    buf.close()
    return html


def download_image(url, number):
    print "downloading %s image please wait"  % number
    toolbar_width = number
    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['
    number = number + 1
    for i in range(1, number):
        img_url = '%s-%s-1024.jpg' % (url, i)
        cmd = 'wget -x -q -O ../output/%03d.jpg %s' % (i, img_url)
        print cmd
        os.system(cmd)
    sys.stdout.write("\n")


def convert_to_pdf(filename):
    os.system('convert ../output/*.jpg ../output/%s' % filename)
    print "%s has been created at folder output please check" % filename
    filelist = [f for f in os.listdir("../output") if f.endswith(".jpg")]
    print "removing images"
    os.system('rm ../output/*.jpg')

if __name__ == '__main__':
    os.system('rm -f ../output/*')
    html = get_result(args['url'])
    url = get_img_url(html)
    pages = get_pages(html)
    download_image(url, pages)
    print "start conver images to pdf please wait..."
    convert_to_pdf(args['file_name'])
