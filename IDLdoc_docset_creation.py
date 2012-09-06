import os
import sqlite3 as lite
import urllib
import BeautifulSoup
import glob

#document to erase
deletelist =[ "./Documents/all-dirs.html","./Documents/all-files.html","./Documents/idldoc-index.html","./Documents/index.html","./Documents/search.html","./Documents/categories.html","./Documents/dir-files.html" ,"./Documents/libdata.js"]+glob.glob('./Documents/*/dir-overview.html')
for f in deletelist:
    os.remove(f)

os.rename("./Documents/dir-overview.html", "./Documents/index.html")

# 2 directory level down listed
filelist = glob.glob('./Documents/*/*.html')+glob.glob('./Documents/*.html')

#connect to the sqlite db
con = lite.connect('docSet.dsidx')
cur = con.cursor()    
#erase all
cur.execute('DELETE FROM searchIndex')
#insert the file in the filelist and beautify the html file
for file in filelist:
    #get the soup ready...
    soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(os.path.abspath(file)))
    #skipping the source code
    if '-code.html' not in file :
        erase_elements=[]
        erase_elements.append(soup.find("div", {"class" : "header"}))
        erase_elements.append(soup.find("table", {"class" : "navbar smaller"}))
        erase_elements.append(soup.find("p", {"class" : "localnavbar smallest"}))
        erase_elements.append(soup.find("script", {"class" : "text/javascript"}))
        for erase in erase_elements :
            if type(erase) is BeautifulSoup.Tag :
                 erase.extract() 
        #re-write the html prettifyied file
        f = open(file, "w")
        f.write(soup.prettify())
        f.close()
    title = soup.title.string
    #erase the parenthesis content and the ".pro" in the HTML title
    title = (title.rsplit('(',1)[0]).rsplit('.pro',1)[0]
    #see the result
    
    print title.title(),file.lstrip('./Documents/')
    #insert in the DB    
    cur.execute("INSERT INTO searchIndex (path,type,name) VALUES (?,'func',?)",(file.lstrip('./Documents/'),title.title()),verbose=1)

#delete the directories entry
cur.execute('DELETE FROM searchIndex WHERE name LIKE "%\%"')

#commit the DB changes
con.commit()