from requests_html import HTMLSession
import sys
import urllib.request, urllib.error, urllib.parse
import webbrowser
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
import re
import shutil
import os
from urllib.request import Request, urlopen
import urllib.parse
import names
import random
import csv
from csv import writer
import datetime
from currency_converter import CurrencyConverter

cc = CurrencyConverter()

brandnamefile = open("thebrand.txt", "r+")
brand = brandnamefile.read()

chromepathfile = open("chromepath.txt", "r+")
chromepath = chromepathfile.read().strip()

tocurrencyfile = open("currency.txt", "r+")
thecurrency = tocurrencyfile.read().strip()

brandnamefile = open("thebrand.txt", "r+")
brand = brandnamefile.read()
owd=os.getcwd()
owd
def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)

def getalllinks(brandname,thepage):
    url=trefacurl+str(brandname)+"&key="+str(thepage)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    values = {'name' : names.get_full_name(),
        'location' : 'Northampton',
        'language' : 'Python' }
    headers = { 'User-Agent' : user_agent }
    req = Request(url, headers=headers)
    the_page = urlopen(req).read()
    pageitemsoup = BeautifulSoup(the_page, 'lxml')
    linktags=pageitemsoup.find_all('ul',{'class' : 'itemList l-inlineBox'})[0]
    for itematag in linktags.find_all('a'):
        if len(itematag['href'])>0:
            linklist.append(itematag['href'])
    return(linklist)

def getgetpagerange(brandname):
    checkpage=True
    thepage=1
    while checkpage:
        url=trefacurl+str(brandname)+"&key="+str(thepage)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        values = {'name' : names.get_full_name(),
            'location' : 'Northampton',
            'language' : 'Python' }
        headers = { 'User-Agent' : user_agent }
        req = Request(url, headers=headers)
        the_page = urlopen(req).read()
        pageitemsoup = BeautifulSoup(the_page, 'lxml')
        pagesection=pageitemsoup.find_all('section',{'class' : 'main-pager'})[0]
        splitpagesbottom=str(pagesection).split()
        if "</b>" not in str(splitpagesbottom[-2]):
            thepage+=1
        else:
            return thepage
            checkpage=False

thebrand=(brand.replace(" ","+").lower())
trefacurl="https://www.trefac.jp/store/tcpsb/?srchword="
linklist=[]
os.chdir(owd)
if not os.path.exists(brand.replace(" ","")):
    os.makedirs(brand.replace(" ",""))
os.chdir(brand.replace(" ",""))
if not os.path.exists(brand.replace(" ","")+"catalogue.csv"):
    append_list_as_row(brand.replace(" ","")+"catalogue.csv",["Site", "Brand", "ItemCode","URL","Price","Type", "Title","Availability","Material", "Colour", "Size", "Model", "Description", "Condition","Time"])
for page in range(1,getgetpagerange(thebrand)+1):
    allthelinks=getalllinks(thebrand,page)
owd=os.getcwd()
owd
for itemurl in allthelinks:
    ax=0
    bx=0
    cx=0
    dx=0
    ex=0
    fx=0
    gx=0
    spliturl=itemurl.split("/")
    itemcode=spliturl[-2]
    if not os.path.exists("trefac_"+itemcode):
        os.makedirs("trefac_"+itemcode)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        values = {'name' : names.get_full_name(),
            'location' : 'Northampton',
            'language' : 'Python' }
        headers = { 'User-Agent' : user_agent }
        item_req = Request(itemurl, headers=headers)
        item_page = urlopen(item_req).read()
        item_soup = BeautifulSoup(item_page, 'lxml')
        theline=item_soup.find_all('span',{'itemprop' : 'name'})[0]
        thelineis=str(theline)[str(theline).index('"name">')+7:str(theline).index("</span")]
        theitemcodeis=itemcode
        theitemurlis=itemurl
        allitemdetail=item_soup.find_all('div',{'class' : 'itemCaption-txt'})[0]
        thepricetag=item_soup.find_all('dd',{'class' : 'itemList-price price'})[0]
        thesizetag=item_soup.find_all('p',{'class' : 'd-point-before'})[0]
        thesizeis=str(thesizetag)[str(thesizetag).index(":")+1:str(thesizetag).index("</p")]
        if "¥" in str(thepricetag):
            ax=1
            thepriceis=str(thepricetag)[str(thepricetag).index("¥")+1:str(thepricetag).index("<span")]
        if ax==0:
            thesalepricetag=item_soup.find_all('dd',{'class' : 'itemList-price priceDown'})[0]
            thepriceis=str(thesalepricetag)[str(thesalepricetag).index("¥")+1:str(thesalepricetag).index("<span")]
        checksoldout=item_soup.find_all('p',{'class' : 'backBtn soldout'})
        if len(checksoldout)>0:
            bx=1
            avalibis="SOLD"
        if bx==0:
            avalibis="AVALIABLE"
        allitemstuffsplit=str(allitemdetail).split("\n")
        for eachline in allitemstuffsplit:
            if "【アイテム名】" in eachline:
                cx=1
                thenameis=eachline[eachline.index('】')+1:eachline.index('<br')]
            if cx==0:
                thenameis="N/A"
            if "【カラー】" in eachline:
                dx=1
                thecolouris=eachline[eachline.index('】')+1:eachline.index('<br')]
            if dx==0:
                thecolouris="N/A"
            if "【型番】" in eachline:
                ex=1
                themodelis=eachline[eachline.index('】')+1:eachline.index('<br')]
            if ex==0:
                themodelis="N/A"
            if "【素材】" in eachline:
                fx=1
                thematerialis=eachline[eachline.index('】')+1:eachline.index('<br')]
            if fx==0:
                thematerialis="N/A"
            if "【状態】" in eachline:
                gx=1
                theconditionis=eachline[eachline.index('】')+1:eachline.index('<')]
            if gx==0:
                theconditionis="N/A"
        imageurls=[]
        append_list_as_row(brand.replace(" ","")+"catalogue.csv",["trefac",thelineis, "trefac_"+theitemcodeis,theitemurlis,str(cc.convert(int(re.findall("\d+", thepriceis)[0]),'JPY',thecurrency))+" "+thecurrency,"N/A",thenameis,avalibis,thematerialis,thecolouris,thesizeis,themodelis,"N/A",theconditionis,datetime.datetime.now()])
        getimagewindow=item_soup.find_all('ul',{'id' : 'thumblist', 'class' : 'clearfix detailimg'})[0]
        for getimageurl in getimagewindow.find_all('a'):
            imageurls.append(str(getimageurl)[str(getimageurl).index('largeimage:')+13:str(getimageurl).index('}">')-1])
        for clothingimage in imageurls:
            splitimage=clothingimage.split('/')
            urllib.request.urlretrieve(str(clothingimage), str(splitimage[-1]))
            shutil.move(os.getcwd()+'/'+splitimage[-1], os.getcwd()+'/'+"trefac_"+itemcode+'/'+splitimage[-1])
            #time.sleep(random.randint(0,2))
    ax=1
    bx=1
    cx=1
    dx=1
    ex=1
    fx=1
    gx=1
