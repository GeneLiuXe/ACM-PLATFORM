import tornado.web
from tornado.web import RequestHandler
import config
import os
import application
from database.MySQL import MySQL

db = MySQL(config.mysql["host"], config.mysql["user"], config.mysql["passwd"], config.mysql["dbName"],
                        config.mysql["port"])
stus = db.get_all_obj("select * from Problem", "Problem")
for line in stus:
    line['Algorithm'] = ""
    OJ_id = "'" + line['OJ_id'] + "'"
    now = db.get_all_obj("select Name from Online_Judge where OJ_id = " + OJ_id,
                                          "Online_Judge", "Name")
    line['OJ_id'] = now[0]['Name']
    Problem_id = "'" + line['Problem_id'] + "'"
    now = db.get_all_obj(
        "select Algorithm_id from Problem_Algorithm where Problem_id = " + Problem_id, "Problem_Algorithm",
        "Algorithm_id")
    for hp in now:
        Algorithm_id = hp['Algorithm_id']
        tp = db.get_all_obj("select Name from Algorithm where Algorithm_id = " + Algorithm_id,
                                             "Algorithm", "Name")
        hp['Algorithm_id'] = tp[0]['Name']
    cnt = 0
    for hp in now:
        if cnt != 0:
            line['Algorithm'] = line['Algorithm'] + "、"
        line['Algorithm'] = line['Algorithm'] + hp['Algorithm_id']
        cnt += 1
with open('ans.txt', 'w') as f:
    for line in stus:
        f.write(line['Problem_id'] + '\t')
        f.write(line['Problem_name'] + '\t')
        f.write(line['OJ_id'] + '\t')
        f.write(line['OJ_Pnumber'] + '\t')
        f.write(line['Difficulty_level'] + '\t')
        f.write(line['Link'] + '\t')
        f.write(line['Algorithm'] + '\n')