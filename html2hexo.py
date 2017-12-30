#coding=utf-8
import os
import re
from bs4 import BeautifulSoup
from requests import *

hexoPath = "./hexoFile/"
def html2hexo(articleHtml):
	soup = BeautifulSoup(articleHtml)
	head,title = hexoHead(soup)
	if not os.path.exists(hexoPath):
		 os.makedirs(hexoPath)
	path = hexoPath+title.replace(" ","_")
	with open(path +".md","w") as f:
		f.write(head.encode("utf-8"))
		f.write(hexoBody(soup,path+"/").encode("utf-8"))
		f.close()

def hexoHead(soup):
	title = soup.title.string[-9::-1][::-1]
	date = ''
	tags = soup.body.ul
	tagRes = []
	describ = soup.head.find(attrs={'name':"description"})["content"]
	print "[=] Coverting article :" + title + " Please wait ...."
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

def hexoBody(soup,path):
	body = ""
	for tag in soup.find(id="article_content").descendants:
		try:
			if tag.name == "h1":
				body += "\n# "+tag.string
			elif tag.name == "h2":
				body += "\n## "+tag.string
			elif tag.name == "h3":
				body += "\n### "+tag.string
			elif tag.name == "h4":
				body += "\n#### "+tag.string
			elif tag.name == "h5":
				body += "\n##### "+tag.string
			elif tag.name == "h6":
				body += "\n###### "+tag.string
			elif tag.name == "p":
				body += "\n"+tag.string+"\n"
			elif tag.name == "code":
				body += "~~~\n" + tag.string + "~~~\n"
			elif tag.name == "img":
				imageFile = fetchImage(tag["src"],path)
				body += "\n{% image_asset/" + imageFile + " %}\n"
		except Exception as e:
			continue
	return body

def stripCharacter(s,repl=""):
	regex = re.compile(ur"[\u4e00-\u9fa5a]")
	return regex.sub(repl,s.encode("utf-8").decode("utf-8"))
	#if not encode,the console will treat s as ascii string; 
	#if not decode,then the s will not be unicode so that the regex is useless

def main():
	print "test html2hexo"

if __name__ == '__main__':
	main()
