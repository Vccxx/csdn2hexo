#coding=utf-8
from bs4 import BeautifulSoup
from requests import *
import os
import re
def fetchHtml(url):
	r = get(url)
	if r.status_code == 200:
		return r.text
	else:
		print "[-] Network Error Occur when fetching %s"%url 
		return ""

def fetchImage(url,dest):
	r = get(url)
	image_file_name =""
	if r.status_code == 200:
		if not os.path.exists(dest):
			os.makedirs(dest)
		image_file_name =  url.replace(".","_").replace("/","_").replace(":","_")+".png"
		with open(dest+ image_file_name,"wb") as f:
			f.write(r.content)
			f.close()
	else:
		print "[-] Network Error Occur when fetching Image %s"%url
	return image_file_name 

def fetchArticleList(url):
	articleList = []
	htmlText = fetchHtml(url)
	if htmlText != "":
		soup = BeautifulSoup(htmlText)
		for li in soup.body.find_all("li"):
			try:
				if li["class"][0] == "blog-unit":
					articleList.append(li.a["href"])
			except:
				continue
	return articleList

def main():
	print "test fetch html"

if __name__ == '__main__':
	main()

