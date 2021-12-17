from BeautifulSoup import BeautifulSoup,BeautifulStoneSoup
import os,pysqlite2
from pysqlite2 import dbapi2 as sqlite
wikitable=open("wikipedia")
soup=BeautifulSoup(wikitable)
db=sqlite.connect("solubility.db")
cursor=db.cursor()
#table=soup.find("table", {"class":"wikitable"})
#tomatsuppe=BeautifulSoup(table)
for stoff in soup("tr"):
	#for x in stoff.contents:
	#	print x
	#	print stoff.contents.index(x)
	try:
		formelhtml= stoff.contents[3].find("a").renderContents()
		formel=formelhtml.replace("<sub>","").replace("</sub>","")
		if formel:
		#print dir(stoff.contents[3].find("a"))
			anion=max(os.popen("echo '%s'|grep -f anions -o" % formel).readlines()).replace("\n","")
			cation=max(os.popen("echo '%s'|grep -f cations -o" %formel).readlines()).replace("\n","")
			print "%s - %s - %s - %f " % (formel,anion,cation,float(stoff.contents[9].string))
			cursor.execute("INSERT INTO formulas VALUES (?,?,?,?)",(formel,cation,anion,float(stoff.contents[9].string)))
			#print float(stoff.contents[9].string)
		#print BeautifulSoup(str(stoff.contents[3])).contents[0].find("a")
	except:
		pass
db.commit()
