#coding=utf-8
from bs4 import BeautifulSoup
from requests import *
import os
import re

index = "http://blog.csdn.net/qq_29947311/"
csdnUrl = "http://blog.csdn.net"
hexoPath = "./hexoFile/"
def fetchHtml(url):
	r = get(url)
	if r.status_code == 200:
		return r.text
	else:
		print "[-] Network Error Occur when fetching %s"%url 
		return ""

def fetchImage(url):
	r = get(url)
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

def html2hexo(articleHtml):
	soup = BeautifulSoup(articleHtml)
	head,title = hexoHead(soup)
	if not os.path.exists(hexoPath):
		 os.makedirs(hexoPath)
	with open(hexoPath+title.replace(" ","_")+".md","w") as f:
		f.write(head.encode("utf-8"))
		hexoBody(soup)
		#f.write(hexoBody(soup).encode("utf-8"))
		f.close()

def hexoHead(soup):
	title = soup.title.string[-9::-1][::-1]
	date = ''
	tags = soup.body.ul
	tagRes = []
	describ = soup.head.find(attrs={'name':"description"})["content"]
	for tag in tags.find_all("li"):
		if tag.a != None:
			tagRes.append(tag.a.string)
	for span in soup.body.find_all("span"):
		try:
			if span["class"][0] == "time":
				date = stripCharacter(span.string,"-").replace("- "," ")
				break
		except:
			continue
	head = "---\ntitle: %s\ndate: %s\n"%(title,date)
	describ = "%s\n<!-- more -->"%describ
	head += "tags:\n"
	for tag in tagRes:
		head += "- %s\n"%tag
	head += "---\n"
	head += describ
	return head,title

def hexoBody(soup):
	body = ""
	for tag in soup.find(id="article_content").descendants:
		if tag.name == "h1":
			body += "# "+tag.string
		elif tag.name == "p":
			body += tag.string+"\n"
		elif tag.name == "code":
			body += "~~~\n" + tag.string + "~~~\n"
		elif tag.name == "image":


def stripCharacter(s,repl=""):
	regex = re.compile(ur"[\u4e00-\u9fa5a]")
	return regex.sub(repl,s.encode("utf-8").decode("utf-8"))
	#if not encode,the console will treat s as ascii string; 
	#if not decode,then the s will not be unicode so that the regex is useless
def main():
	for articleUrl in fetchArticleList(index):
		articleText = fetchHtml(csdnUrl+articleUrl)
		if articleText != "":
			html2hexo(articleText)
if __name__ == '__main__':
	main()


