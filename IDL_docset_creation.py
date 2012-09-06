python code:

import sqlite3 as lite
import sys
import urllib
import BeautifulSoup

con = lite.connect('docSet.dsidx')

cur = con.cursor()    
cur.execute('SELECT id,path,name,type FROM searchIndex')

rows = cur.fetchall()

for row in rows:
     print BeautifulSoup.BeautifulSoup(urllib.urlopen("/Users/damo_ma/Library/Application Support/Dash/DocSets/IDL/IDL/Contents/Resources/Documents/"+row[1])).title.string

for row in rows:
     update_query = 'UPDATE searchIndex SET name="'+BeautifulSoup.BeautifulSoup(urllib.urlopen("/Users/damo_ma/Library/Application Support/Dash/DocSets/IDL/IDL/Contents/Resources/Documents/"+row[1])).title.string+'" WHERE id='+str(row[0])
     print update_query
     cur.execute(update_query)
     
con.commit()
    
sqlite3 code: 

-- entry with no defined title
SELECT name FROM searchIndex WHERE name LIKE "%!_!_%"  escape '!';;

-- set the method type clm = class methods
SELECT name FROM searchIndex WHERE name LIKE "%::%";
UPDATE  searchIndex SET type='clm' WHERE name LIKE "%::%";

-- erase strange &#160;
SELECT replace(name,'&#160;','') FROM searchIndex WHERE name LIKE "%&#160;%";
UPDATE  searchIndex SET name=replace(name,'&#160;','') WHERE name LIKE "%&#160;%";


SELECT id,type,name FROM searchIndex WHERE name LIKE "IDL%" AND not name LIKE "%::%" AND not name LIKE "%Properties%" AND not name LIKE "% %" AND not name LIKE "%!_!_%"  escape '!';

--erase set some entry as cl = class
UPDATE  searchIndex SET type='cl' WHERE name LIKE "IDL%" AND not name LIKE "%::%" AND not name LIKE "%Properties%" AND not name LIKE "% %" AND not name LIKE "%!_!_%"  escape '!';

--erase x'0A',x'20',x'0D'
UPDATE searchIndex SET name=replace(name,x'0A','')  WHERE name LIKE '%'||X'0A'||'%';
UPDATE searchIndex SET name=replace(name,x'20','')  WHERE name LIKE '%'||X'20'||'%';
UPDATE searchIndex SET name=replace(name,x'0D','')  WHERE name LIKE '%'||X'0D'||'%';
