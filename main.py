#coding=utf-8
from bs4 import BeautifulSoup
from requests import *
import os
import re
from fetchHtml import *
from html2hexo import *

index = "http://blog.csdn.net/qq_29947311/"
csdnUrl = "http://blog.csdn.net"
hexoPath = "./hexoFile/"


def main():
	for articleUrl in fetchArticleList(index):
		articleText = fetchHtml(csdnUrl+articleUrl)
		if articleText != "":
			html2hexo(articleText)
			print "[+] Done!"
if __name__ == '__main__':
	main()


