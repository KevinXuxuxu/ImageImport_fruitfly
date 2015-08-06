# use UTP-8 #
"""
    Import iterable class for insitu imagesc
    with metadatas in mysql db.
"""

__author__ = "Xu Fangzhou"
__email__ = "kevin.xu.fangzhou@gmail.com"

import os
import MySQLdb as msdb
import re
import csv

def decapitate(attrs):
    head, body = [],[]
    same = []
    for i in range(len(attrs)):
        tmp = re.split("\.", attrs[i])
        head.append(tmp[0])
        if tmp[1] in body:
            same.append(i)
            same.append(body.index(tmp[1]))
        body.append(tmp[1])
    for i in range(len(body)):
        if i in same:
            body[i] = head[i]+'.'+body[i]
    return body

def trans(com):
    rtn = com.replace(';','\;')
    rtn = rtn.replace("'","\\'")
    return rtn

class Insitu:

    def __init__(self, sql_addr="128.3.62.222", uname="guest", db="insitu", attrs=[], froms=[], filters=[]):
        # self.db = msdb.connect(host=sql_addr, user=uname, db=db)
        if len(attrs) == 0:
            attrs = ["image.id", # depricate
                     "image.image_path",
                     "image.magnification",
                     "image.ap",
                     "image.dv",
                     "image.orientation",
                     "image.handedness",
                     "image.image_processing_flags",
                     "image.validated",
                     "main.est_id",
                     "main.date",
                     "main.species",
                     "main.fly_strain",
                     "main.tissue",
                     "main.is_published",
                     "main.publish_date",
                     "main2info.fbgn",
                     "main2info.clone",
                     "main2info.symbol",
                     "annot.stage"]
        if len(froms) == 0:
            froms = ["image",
                     "annot",
                     "main",
                     "main2info"]
        if len(filters) == 0:
            filters = ["main.id = main2info.main_id",
                       "annot.main_id = main.id",
                       "image.annot_id = annot.id",
                       "main2info.symbol = 'twi'"]
        command = "SELECT "+attrs[0]
        for i in range(1,len(attrs)):
            command += " ,"+attrs[i]
        command += " FROM "+froms[0]
        for i in range(1,len(froms)):
            command += ", "+froms[i]

        # filtering part
        command += " WHERE "+filters[0]
        for i in range(1,len(filters)):
            command += " AND "+filters[i]

        command += ";"
        print command

        # temporary measure: log into sql through fangzhou@toy.lbl.gov

        command = trans(command)
        command_line = "echo \"echo %s | mysql -u %s -h %s %s\" | ssh fangzhou@toy.lbl.gov > out.tsv" %(command, uname, sql_addr, db)
        print command_line
        os.system(command_line)
        fp = open("out.tsv")
        r = csv.reader(fp, delimiter='\t', quoting=csv.QUOTE_ALL)
        self.rtn = []
        for i in r:
            self.rtn += [i]
        fp.close()
        os.system("rm out.tsv")

        # cur = self.db.cursor()
        # cur.execute(command)
        # self.rtn = cur.fetchall()
        self.attrs = decapitate(attrs)

        self.i = 1
        self.n = len(self.rtn)

    def __iter__(self):
        return self

    def next(self):
        d = {}
        if self.i < self.n:
            i = self.i
            self.i += 1
            for j in range(len(self.attrs)):
                d[self.attrs[j]] = self.rtn[i][j]
            return d
        else:
            raise StopIteration()
