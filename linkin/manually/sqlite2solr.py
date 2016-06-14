 #-*- coding: utf-8 -*-
import sqlite3
import solr

def Main():
    s = solr.Solr("http://localhost:8080/solr")
    con = sqlite3.connect("d:/temp/test.db")
    cursor = con.cursor()
    #cursor.execute("select * from t_talents limit 6,3")
    cursor.execute("select * from t_talents")
    rows = cursor.fetchall()
    count = 0
    for row in rows:
        count += 1
        tid = row[0]
        tname = row[1]
        ttitle = row[2]
        tlocality = row[4]
        tindustry = row[5]
        tcurposition = row[6]
        tprofile = row[9]
        docn = {'id':tid,'talent_name':tname,'talent_title':ttitle,'talent_locality':tlocality,'talent_industry':tindustry,'talent_curposition':tcurposition,'talent_profile':tprofile}
        s.add(docn,commit=True)
        print('done:'+str(count))
    con.close()
if __name__ == "__main__":
    Main()

