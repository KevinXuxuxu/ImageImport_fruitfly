# use UTP-8 #
"""
    Import iterable class for insitu imagesc
    with metadatas in mysql db.
"""

__author__ = "Xu Fangzhou"
__email__ = "kevin.xu.fangzhou@gmail.com"

import os
import MySQLdb as msdb

class Insitu:

    def __init__(self, sql_addr="128.3.62.222", uname="guest", db="insitu", attrs=[], froms=[]):
        self.db = msdb.connect(host=sql_addr, user=uname, db=db)
        if len(attrs) == 0:
            attrs = ["image.image_path",
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
        command = "SELECT "+attrs[0]
        for i in range(1,len(attrs)):
            command += " ,"+attrs[i]
        command += " FROM "+froms[0]
        for i in range(1,len(froms)):
            command += ", "+froms[i]

        # filtering part

        command += ";"
        print command
        cur = self.db.cursor()
        cur.execute(command)
        self.rtn = cur.fetchall()

    def __iter__(self):
        return self
