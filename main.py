#encoding:utf-8
import os
import sys
import requests
import ssl
from bs4 import BeautifulSoup as bsp
from time import sleep
#reload(sys)
#sys.setdefaultencoding('utf-8')
cur_path = os.path.dirname(__file__)

#ssl._create_default_https_context = ssl._create_unverified_context


#清空文件
f = open(cur_path+'href.list','w')
f.close()
log_file = open(cur_path+'tmp.log','w')
log_file.close()
have_done_file = open(cur_path + 'have_done.list','w')

log_file = open(cur_path+'tmp.log','a')
#打开列表文件

#page页的所有center中的a标签的href输出
index_url = 'https://www.24fa.com/MeiNv/index.html'
origin_url = 'https://www.24fa.com/MeiNv/indexp{}.html'
head_url = 'https://www.24fa.com/'
#获取每页的td,保存每个href
def save_index_href():
	href_file = open(cur_path+'href.list','a')
	url = index_url
	try:
		#获取class为wrapper下的td标签
		html = requests.get(url)
		sp = bsp(html.text,'html.parser')
		href_lists = sp.select('.wrapper td a')
		for list in href_lists:
			print(list.get('href'))
			href_url = list.get('href').replace('../',head_url)
			href_file.write(href_url+'\n')
	except BaseException:
		log_file.write(url+'\t'+'首页获取失败'+'\n')
	href_file.close()
def save_page_href(start,stop,step=1):
	for page in range(start,stop,step):
		href_file = open(cur_path+'href.list','a')
		#获取class为wrapper下的td标签
		url = origin_url.format(page)
		try:
			html = requests.get(url)
			sp = bsp(html.text,'html.parser')
			href_lists = sp.select('.wrapper td a')
			for list in href_lists:
				print(list.get('href'))
				href_url = list.get('href').replace('../',head_url)
				href_file.write(href_url+'\n')
		except BaseException:
			log_file.write(url+'\t'+'主题某一页获取失败'+'\n')
		href_file.close()

#保存每页的图片
def save_onepage_img_src(sp,src_file):
	#获取图片的src
	imgs_src = sp.select('#content div img')
	for list in imgs_src:
		print(list.get('src'))
		src_url = list.get('src').replace('../../',head_url)
		src_file.write(src_url+'\n')

#获取一个主题的图片
def save_all_img_src(url):
	#传入参数为首页
	try:
		html = requests.get(url=url)
		html.encoding='utf-8'
		sp = bsp(html.text,'html.parser')
		title = sp.find('h1',{'class':'title2'}).text
		with open(cur_path+'list/'+title+'.txt','w') as src_file:
			while(True):
				save_onepage_img_src(sp,src_file)
				#如果有下一页，则更新url
				if next_page_url(sp):
					url = next_page_url(sp);
					html = requests.get(url=url)
					html.encoding='utf-8'
					sp = bsp(html.text,'html.parser')
				else:
					break;
	except BaseException:
		log_file.write(url+'\t'+'下一页获取失败'+'\n')
def next_page_url(sp):
	#如果没有下一页
	if not '下一页' in sp.find('div',{'class':'pager'}).text:
		return False
	#如果有下一页
	else:
		url = sp.find('a',{'title':'下一页'}).get('href')
		url = url.replace('../../',head_url)
		return url
#20180513最新：https://www.24fa.com/MeiNv/2018-05/56187.html
if __name__=='__main__':
	#save_index_href()
	#save_page_href(2,23)
	#得到href_file的所有地址
	lines = open(cur_path+'href2.list','r').readlines()
	#save_all_img_src('https://www.24fa.com/MeiNv/2018-05/56144.html')
	for line in lines:
	#递归执行完成某一个地址下的所有图片
	#1.获取titile,保存成一个文件
		have_done_file.write(line+'')
		line = line.strip('\n')
		print(line)
		save_all_img_src(line)
	#2.保存图片地址
		sleep(1)
		#break
	have_done_file.close()
