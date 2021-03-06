import sqlite3 as lite
import BeautifulSoup
import glob
# import os
# import urllib

#document to erase
deletelist =[ "./Documents/all-dirs.html","./Documents/all-files.html",
             "./Documents/idldoc-index.html","./Documents/index.html",
             "./Documents/search.html","./Documents/categories.html",
             "./Documents/dir-files.html" ,"./Documents/libdata.js"]+glob.glob('./Documents/*/dir-overview.html')
for f in deletelist:
    if os.path.isfile(f):
       os.remove(f)

if os.path.isfile("./Documents/dir-overview.html"):
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
    soup = BeautifulSoup.BeautifulSoup(open(file))
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
    
    path = file[12:len(file)]
    print "Title : "+title.title().ljust(40),"Path :"+path
    #insert in the DB
    cur.execute("INSERT INTO searchIndex (path,type,name) VALUES (?,'func',?)",(path,title.title()))

#delete the directories entry
cur.execute('DELETE FROM searchIndex WHERE name LIKE "%\%"')

#commit the DB changes
con.commit()