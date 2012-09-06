To translate an existing IDLdoc (http://idldoc.idldev.com/) documentation follow this steps: 

1. Build the directories structure as described in http://kapeli.com/docsets/ or use the empty IDLdoc.docset 
2. copy you documentation in IDLdoc.docset/Contents/Resources/Documents/ 
3. run the IDLdoc_docset_creation.py in the Resources/ directory 

Optional : change the IDLdoc.docset/icon.png and adjust the IDLdoc.docset/Contents/nfo.plist 

The python code does the following: 
- scans only 2 level deep in the Documents folder 
- deletes some files (all-dirs.html,all-files.html etc) 
- sets as start page the dir-overview.html changing it to index.html 
- gets the title from each html page 
- modifies the html erasing the top banner 
- writes all in the sqlite DB docSet.dsidx 

In order to run properly you need to have the sqlite3,urllib,BeautifulSoup and glob modules along your python distribution. 
