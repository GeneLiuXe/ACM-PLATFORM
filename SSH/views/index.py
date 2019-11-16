# 视图
import tornado.web
from tornado.web import RequestHandler
import config
import os
from datetime import datetime, timedelta
import json


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        stus1 = self.application.db.get_all_obj("select Name from school", "school",
                                                "Name")
        stus2 = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                "Name")
        self.render('html/index.html', School=stus1, Lab=stus2)


class RegisterHandler(RequestHandler):
    def post(self, *args, **kwargs):
        stus1 = self.application.db.get_all_obj("select Name from school", "school",
                                                "Name")
        stus2 = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                "Name")
        Person_id = self.get_body_argument("Person_id")
        # print(Person_id)
        if Person_id == '':
            self.render('html/RgError.html', jud=1, School=stus1, Lab=stus2)
            return
        Person_id = "'" + Person_id + "'"
        stus = self.application.db.get_all_obj("select Person_id from Person where Person_id = " + Person_id, "Person",
                                               "Person_id")
        # print(len(stus))
        if len(stus) != 0:
            self.render('html/RgError.html', jud=2, School=stus1, Lab=stus2)
            return
        Name = self.get_body_argument("Name")
        Gender = self.get_body_argument("Gender")
        Major = self.get_body_argument("Major")
        Grade = self.get_body_argument("Grade")
        Class = self.get_body_argument("Class")
        School = self.get_body_argument("School")
        School = "'" + School + "'"
        stus = self.application.db.get_all_obj("select School_id from school where Name = " + School, "school",
                                               "School_id")
        School_id = stus[0]['School_id']
        Lab = self.get_body_argument("Lab")
        Lab = "'" + Lab + "'"
        stus = self.application.db.get_all_obj("select Lab_id from laboratory where Name = " + Lab, "laboratory",
                                               "Lab_id")
        Lab_id = stus[0]['Lab_id']
        Serect = self.get_body_argument("Serect")
        if Serect == '':
            self.render('html/RgError.html', jud=3, School=stus1, Lab=stus2)
            return
        Name = "'" + Name + "'"
        Major = "'" + Major + "'"
        Grade = "'" + Grade + "'"
        Gender = "'" + Gender + "'"
        Class = "'" + Class + "'"
        School_id = "'" + School_id + "'"
        Lab_id = "'" + Lab_id + "'"
        Serect = "'" + Serect + "'"
        sql = "insert into Person(Person_id,Name,Gender,Major,Grade,Class,School_id,Lab_id,Serect) values (" + Person_id + "," + Name + "," + Gender + "," + Major + "," + Grade + "," + Class + "," + School_id + "," + Lab_id + "," + Serect + ")"
        # print(sql)
        self.application.db.update(sql)
        self.render('html/RgError.html', jud=4, School=stus1, Lab=stus2)


class LoginHandler(RequestHandler):
    def post(self, *args, **kwargs):
        stus1_school = self.application.db.get_all_obj("select Name from school", "school",
                                                "Name")
        stus2_lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                "Name")
        Person_id = self.get_body_argument("InputAccount")
        Serect = self.get_body_argument("InputPassword")
        tmp = Person_id
        Person_id = "'" + Person_id + "'"
        stus = self.application.db.get_all_obj("select Serect from Person where Person_id = " + Person_id, "Person",
                                               "Serect")
        stus1 = self.application.db.get_all_obj("select * from Problem", "Problem")
        stus2 = self.application.db.get_all_obj("select * from Contest", "Contest")
        stus1 = stus1[-6:-1]
        stus2 = stus2[-6:-1]
        stus1.reverse()
        stus2.reverse()
        for line in stus2:
            line['Date'] = line['Begin_time'][0:7]
            line['Day'] = line['Begin_time'][8:10]
            line['Time1'] = line['Begin_time'][11:16]
            line['Time2'] = line['End_time'][11:16]
        if len(stus) == 0:
            self.render('html/LogError.html', School=stus1_school, Lab=stus2_lab)
        elif stus[0]['Serect'] == Serect:
            self.set_cookie('Person_id', tmp, expires_days=None)
            self.render('html/HomePage.html', Person_id=tmp,Problem=stus1,Contest=stus2)
        else:
            self.render('html/LogError.html', School=stus1_school, Lab=stus2_lab)


class LogoutHandler(RequestHandler):
    def get(self, *args, **kwargs):
        stus1 = self.application.db.get_all_obj("select Name from school", "school",
                                                "Name")
        stus2 = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                "Name")
        self.render('html/index.html', School=stus1, Lab=stus2)


class HomePageHandler(RequestHandler):
    def get(self, *args, **kwargs):
        stus1 = self.application.db.get_all_obj("select * from Problem", "Problem")
        stus2 = self.application.db.get_all_obj("select * from Contest", "Contest")
        stus1 = stus1[-6:-1]
        stus2 = stus2[-6:-1]
        stus1.reverse()
        stus2.reverse()
        for line in stus2:
            line['Date'] = line['Begin_time'][0:7]
            line['Day'] = line['Begin_time'][8:10]
            line['Time1'] = line['Begin_time'][11:16]
            line['Time2'] = line['End_time'][11:16]

        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        print("user",user)
        self.render('html/HomePage.html', Person_id=user,Problem=stus1,Contest=stus2)


class ProblemHandler(RequestHandler):
    def get(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        stus = self.application.db.get_all_obj("select * from Problem", "Problem")
        level = self.application.db.get_all_obj(
            "select * from Person where Person_id = " + "'" + user + "'", "Person")
        self.render('html/Problem.html', Person_id=user, Problem=stus, jud='1', level=level)

    def post(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        Type = self.get_argument('Type')
        tp = '0'
        if Type == '1':
            Name = "'" + self.get_argument('AddProblemName') + "'"
            OJ = "'" + self.get_argument('AddProblemOJ') + "'"
            OJ_Pnumber = "'" + self.get_argument('AddProblemOJ_Pnumber') + "'"
            Difficulty = "'" + self.get_argument('AddProblemDifficulty') + "'"
            Algorithm = "'" + self.get_argument('AddProblemAlgorithm') + "'"
            Link = "'" + self.get_argument('AddProblemLink') + "'"
            num = self.application.db.get_all_obj("select count(*) from Problem", "Problem", "Num")
            Problem_id = "%07d" % (num[0]['Num'] + 21)
            Problem_id = "'" + str(Problem_id) + "'"
            sql = "insert into Problem values (" + Problem_id + "," + Name + "," + OJ + "," + OJ_Pnumber + "," + Difficulty + "," + Link + "," + Algorithm + ")"
            # print(sql)
            self.application.db.update(sql)
            tp = '2'
        elif Type == '2':
            ProblemID = "'" + self.get_argument('DeleteProblemID') + "'"
            sql = "delete from Problem where Problem_id = " + ProblemID
            self.application.db.delete(sql)
            tp = '3'
        stus = self.application.db.get_all_obj("select * from Problem", "Problem")
        level = self.application.db.get_all_obj(
            "select * from Person where Person_id = " + "'" + user + "'", "Person")
        self.render('html/Problem.html', Person_id=user, Problem=stus, jud=tp, level=level)


class AlgorithmHandler(RequestHandler):
    def get(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        self.render('html/Algorithm.html', Person_id=user)


class ContestHandler(RequestHandler):
    def get(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        stus = self.application.db.get_all_obj("select * from Contest", "Contest")
        # print(stus)
        self.render('html/Contest.html', Person_id=user, Contest=stus)


class AddContestHandler(RequestHandler):
    def get(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        self.render('html/AddContest.html', Person_id=user, jud='0')


class AddConErrorHandler(RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        Name = self.get_argument('Name')
        # print("Name",Name)
        # Rank = self.get_argument('Rank')
        # Penalty = self.get_argument('Penalty')
        Begin_time = self.get_argument('StartTime')
        End_time = self.get_argument('EndTime')
        Link = self.get_argument('Link')
        Type = self.get_argument('Type')
        # print("Rank",Rank)
        if Name == "":
            self.render('html/AddContest.html', Person_id=user, jud='1')
            return
        if Begin_time == "":
            self.render('html/AddContest.html', Person_id=user, jud='2')
            return
        if End_time == "":
            self.render('html/AddContest.html', Person_id=user, jud='3')
            return
        if Link == "":
            self.render('html/AddContest.html', Person_id=user, jud='4')
            return
        num = self.application.db.get_all_obj("select count(*) from Contest", "Contest", "Num")
        Contest_id = "%06d" % (num[0]['Num'] + 1)
        Contest_id = "'" + str(Contest_id) + "'"
        # print(Begin_time)
        # print(End_time)
        # Rank = "'" + Rank + "'"
        # Penalty = "'" + Penalty + "'"
        Begin_time = "'" + Begin_time + "'"
        End_time = "'" + End_time + "'"
        Type = "'" + Type + "'"
        Name = "'" + Name + "'"
        Link = "'" + Link + "'"
        sql = "insert into Contest values (" + Contest_id + "," + Name + "," + Begin_time + "," + End_time + "," + Type + "," + Link + ")"
        # print(sql)
        self.application.db.update(sql)
        self.render('html/AddContest.html', Person_id=user, jud='5')


class ConInformationHandler(RequestHandler):
    def get(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        tmp = "'" + self.get_argument('Contest_id') + "'"
        sql = "select * from Contest where Contest_id = " + tmp
        stus = self.application.db.get_all_obj(sql, "Contest")
        now = "'" + stus[0]['Contest_id'] + "'"
        # tmp存储当前比赛的所有题目
        tmp = self.application.db.get_all_obj("select Problem_id from Contest_Problem where Contest_id = " + now,
                                              "Contest_Problem", "Problem_id")
        Pro = []
        for line in tmp:
            Pro.append(line['Problem_id'])
        # content存储所有题目，此处目的是将该比赛中所有题目信息补充完整
        content = self.application.db.get_all_obj("select * from Problem", "Problem")
        Problem = []
        for line in content:
            if line['Problem_id'] not in Pro:
                continue
            tmp = {}
            tmp['Problem_id'] = line['Problem_id']
            tmp['Problem_name'] = line['Problem_name']
            tmp['OJ'] = line['OJ']
            tmp['OJ_Pnumber'] = line['OJ_Pnumber']
            tmp['Difficulty'] = line['Difficulty_level']
            tmp['Link'] = line['Link']
            tmp['Algorithm'] = line['Algorithm']
            Problem.append(tmp)
        # print("Problem",Problem)
        Length = 15 * (15 - len(Problem))
        if Length < 0:
            Length = 0
        sql = "select * from Person_Finish_Problem where Person_id = " + "'" + user + "'"
        # 得到我完成的题目的信息
        Myfinish = self.application.db.get_all_obj(sql,"Person_Finish_Problem")

        # 扩展成队伍完成的题目信息
        THP = self.get_argument('THP')
        if THP == '2':
            # 得到队伍成员
            Team_id = self.get_argument('Team_id')
            Person_Team = self.application.db.get_all_obj("select * from Person_Team where Team_id = " + Team_id,
                                                          "Person_Team")
            Person = []
            Person.append(user)
            for line in Person_Team:
                if line['Person_id'] not in Person:
                    Person.append(line['Person_id'])
            Person.append("无")
            Person.append("无")
            for line in Person:
                if line != '无' and line != user:
                    Myfinish.extend(self.application.db.get_all_obj(
                        "select * from Person_Finish_Problem where Person_id = " + "'" + line + "'",
                        "Person_Finish_Problem"))

        # 重新扩展得到原有题目信息
        for line in Problem:
            line['TAG'] = ""
            line['Solution_Link'] = ""
            for xp in Myfinish:
                if(line['Problem_id'] == xp['Problem_id']):
                    line['TAG'] = xp['TAG']
                    line['Solution_Link'] = xp['Solution_Link']
                    break
        self.render('html/ConInformation.html', Person_id=user, stus=stus, Problem=Problem,
                    Length=Length, ProLen=content, jud='0')

    def post(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        Type = self.get_argument('Type')
        tmp = "'" + self.get_argument('Contest_id') + "'"
        sql = "select * from Contest where Contest_id = " + tmp
        stus = self.application.db.get_all_obj(sql, "Contest")
        now = "'" + stus[0]['Contest_id'] + "'"
        tmp = self.application.db.get_all_obj("select Problem_id from Contest_Problem where Contest_id = " + now,
                                              "Contest_Problem", "Problem_id")
        thp3 = self.get_body_argument('ConProblemID')
        AddProblem_id = ""
        for i in range(7):
            AddProblem_id += thp3[i]
        thp2 = "'" + AddProblem_id + "'"
        jud = '2'
        if Type == '1':
            for line in tmp:
                if AddProblem_id == line['Problem_id']:
                    jud = '1'
                    break
            if jud == '2':
                thp1 = "'" + self.get_argument('Contest_id') + "'"
                sql = "insert into Contest_Problem values (" + thp1 + "," + thp2 + ")"
                self.application.db.update(sql)
                # print("sql",sql)
                tmp = self.application.db.get_all_obj("select Problem_id from Contest_Problem where Contest_id = " + now,
                                                      "Contest_Problem", "Problem_id")
        else:
            jud = '3'
            thp1 = "'" + self.get_argument('Contest_id') + "'"
            sql = "delete from Contest_Problem where Contest_id = " + thp1 + " and Problem_id = " + thp2
            self.application.db.delete(sql)
            tmp = self.application.db.get_all_obj("select Problem_id from Contest_Problem where Contest_id = " + now,
                                                  "Contest_Problem", "Problem_id")
        Pro = []
        for line in tmp:
            Pro.append(line['Problem_id'])
        content = self.application.db.get_all_obj("select * from Problem", "Problem")
        Problem = []
        for line in content:
            if line['Problem_id'] not in Pro:
                continue
            tmp = {}
            tmp['Problem_id'] = line['Problem_id']
            tmp['Problem_name'] = line['Problem_name']
            tmp['OJ'] = line['OJ']
            tmp['OJ_Pnumber'] = line['OJ_Pnumber']
            tmp['Difficulty'] = line['Difficulty_level']
            tmp['Link'] = line['Link']
            tmp['Algorithm'] = line['Algorithm']
            Problem.append(tmp)
        Length = 15 * (15 - len(Problem))
        if Length < 0:
            Length = 0
        sql = "select * from Person_Finish_Problem where Person_id = " + "'" + user + "'"
        Myfinish = self.application.db.get_all_obj(sql,"Person_Finish_Problem")
        # 扩展成队伍完成的题目信息
        THP = self.get_argument('THP')
        if THP == '2':
            # 得到队伍成员
            Team_id = self.get_argument('Team_id')
            Person_Team = self.application.db.get_all_obj("select * from Person_Team where Team_id = " + Team_id,
                                                          "Person_Team")
            Person = []
            Person.append(user)
            for line in Person_Team:
                if line['Person_id'] not in Person:
                    Person.append(line['Person_id'])
            Person.append("无")
            Person.append("无")
            for line in Person:
                if line != '无' and line != user:
                    Myfinish.extend(self.application.db.get_all_obj(
                        "select * from Person_Finish_Problem where Person_id = " + "'" + line + "'",
                        "Person_Finish_Problem"))
        for line in Problem:
            line['TAG'] = ""
            line['Solution_Link'] = ""
            for xp in Myfinish:
                if(line['Problem_id'] == xp['Problem_id']):
                    line['TAG'] = xp['TAG']
                    line['Solution_Link'] = xp['Solution_Link']
                    break
        self.render('html/ConInformation.html', Person_id=user, stus=stus, Problem=Problem,
                    Length=Length, ProLen=content, jud=jud)


class UserHandler(RequestHandler):
    def get(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        jud = '-1'
        tmp = "'" + user + "'"
        Type = self.get_argument('Type')
        if Type == '-2':
            jud = '-2'
        if Type == '4':
            tmpTeam = self.application.db.get_all_obj("select count(*) from Team", "Team", "Num")
            TeamNum = "%06d" % int(tmpTeam[0]['Num'] + 1)
            TeamNum1 = "'" + str(TeamNum) + "'"
            sql = "insert into Team(Team_id, Name) values (" + TeamNum1 + "," + "'无'" + ")"
            self.application.db.update(sql)
            print("sql1", sql)
            Today = datetime.now().strftime("%Y-%m-%d")
            TodayTime = "'" + str(Today) + "'"
            sql = "insert into Person_Team values (" + tmp + "," + TeamNum1 + "," + TodayTime + "," + "'无'" + ")"
            print("sql2", sql)
            self.application.db.update(sql)
            jud = '3'
        sql = "select * from Person_Finish_Problem where Person_id = " + tmp
        stus = self.application.db.get_all_obj(sql, "Person_Finish_Problem")
        ProLen = 0
        ff = self.application.db.get_all_obj("select * from Problem", "Problem")
        for line in ff:
            ProLen += 1
            # line = line.split('\t')
            for i in stus:
                if line['Problem_id'] == i['Problem_id']:
                    i['Problem_name'] = line['Problem_name']
                    i['OJ'] = line['OJ']
                    i['OJ_Pnumber'] = line['OJ_Pnumber']
                    i['Difficulty'] = line['Difficulty_level']
                    i['Link'] = line['Link']
                    i['Algorithm'] = line['Algorithm']
                    break
        sql = "select * from Contest_Person where Person_id = " + tmp
        Contest = self.application.db.get_all_obj(sql, "Contest_Person")
        ConLen = self.application.db.get_all_obj("select * from Contest", "Contest")
        sql = "select * from Person_Team where Person_id = " + tmp
        Team = self.application.db.get_all_obj(sql, "Person_Team")
        for line in Team:
            thp = "'" + line['Team_id'] + "'"
            tmpName = self.application.db.get_all_obj("select Name from Team where Team_id = " + thp, "Team", "Name")
            line['Name'] = tmpName[0]['Name']
        ff.reverse()
        stus1 = self.application.db.get_all_obj(
            "select Problem_id from Person_Finish_Problem where Person_id = " + "'" + user + "'",
            "Person_Finish_Problem", "Problem_id")
        for line in Contest:
            stus2 = self.application.db.get_all_obj(
                "select Problem_id from Contest_Problem where Contest_id = " + "'" + line['Contest_id'] + "'",
                "Contest_Problem", "Problem_id")
            ctt = 0
            for xp in stus2:
                hpp = 0
                for xxp in stus1:
                    if xxp['Problem_id'] == xp['Problem_id']:
                        hpp = 1
                        break
                if hpp == 0:
                    ctt += 1
            line['Finish'] = ctt
        for line in Contest:
            stus2 = self.application.db.get_all_obj("select * from Contest where Contest_id = " + "'" + line['Contest_id'] + "'","Contest")
            line['Begin_time'] = stus2[0]['Begin_time']
            line['Contest_type'] = stus2[0]['Contest_type']
        # print("Contest",Contest)
        self.render('html/User.html', Person_id=user, Problem=stus,
                    Length=(15 * (15 - len(stus))), ProLen=ProLen, jud=jud, Contest=Contest,
                    Length2=(15 * (15 - len(Contest))), ConLen=ConLen, Team=Team, FF=ff,
                    Length3=(15 * (15 - len(Team))))

    def post(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        Type = self.get_argument('Type')
        if Type == '1':
            tpp = self.get_body_argument('UserAddProblemID')
            Problem_id = ""
            for i in range(7):
                Problem_id += tpp[i]
            TAG = self.get_body_argument('UserAddProblemTAG')
            Problem_Link = self.get_body_argument('UserAddProblemLink')
            jud = '0'
            tmp = "'" + user + "'"
            sql = "select * from Person_Finish_Problem where Person_id = " + tmp
            stus = self.application.db.get_all_obj(sql, "Person_Finish_Problem")
            for i in stus:
                if Problem_id == i['Problem_id']:
                    jud = '1'
            if jud == '0':
                time = "'" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "'"
                a1 = "'" + Problem_id + "'"
                a2 = "'" + TAG + "'"
                a3 = "'" + Problem_Link + "'"
                sql = "insert into Person_Finish_Problem values (" + tmp + "," + a1 + "," + time + "," + a2 + "," + a3 + ")"
                self.application.db.update(sql)
                sql = "select * from Person_Finish_Problem where Person_id = " + tmp
                stus = self.application.db.get_all_obj(sql, "Person_Finish_Problem")

            ProLen = 0
            ff = self.application.db.get_all_obj("select * from Problem", "Problem")
            for line in ff:
                ProLen += 1
                # line = line.split('\t')
                for i in stus:
                    if line['Problem_id'] == i['Problem_id']:
                        i['Problem_name'] = line['Problem_name']
                        i['OJ'] = line['OJ']
                        i['OJ_Pnumber'] = line['OJ_Pnumber']
                        i['Difficulty'] = line['Difficulty_level']
                        i['Link'] = line['Link']
                        i['Algorithm'] = line['Algorithm']
                        break
            sql = "select * from Contest_Person where Person_id = " + tmp
            Contest = self.application.db.get_all_obj(sql, "Contest_Person")
            for line in Contest:
                stus2 = self.application.db.get_all_obj(
                    "select * from Contest where Contest_id = " + "'" + line['Contest_id'] + "'", "Contest")
                line['Begin_time'] = stus2[0]['Begin_time']
                line['Contest_type'] = stus2[0]['Contest_type']
            # ConLen = self.application.db.get_all_obj("select count(*) from Contest", "Contest", "Len")
            ConLen = self.application.db.get_all_obj("select * from Contest", "Contest")

            sql = "select * from Person_Team where Person_id = " + tmp
            Team = self.application.db.get_all_obj(sql, "Person_Team")
            for line in Team:
                thp = "'" + line['Team_id'] + "'"
                tmpName = self.application.db.get_all_obj("select Name from Team where Team_id = " + thp, "Team",
                                                          "Name")
                line['Name'] = tmpName[0]['Name']
            ff.reverse()

            # 确认比赛是否全部完成
            stus1 = self.application.db.get_all_obj(
                "select Problem_id from Person_Finish_Problem where Person_id = " + "'" + user + "'",
                "Person_Finish_Problem", "Problem_id")
            for line in Contest:
                stus2 = self.application.db.get_all_obj(
                    "select Problem_id from Contest_Problem where Contest_id = " + "'" + line['Contest_id'] + "'",
                    "Contest_Problem", "Problem_id")
                ctt = 0
                for xp in stus2:
                    hpp = 0
                    for xxp in stus1:
                        if xxp['Problem_id'] == xp['Problem_id']:
                            hpp = 1
                            break
                    if hpp == 0:
                        ctt += 1
                line['Finish'] = ctt

            for line in Contest:
                stus2 = self.application.db.get_all_obj(
                    "select * from Contest where Contest_id = " + "'" + line['Contest_id'] + "'", "Contest")
                line['Begin_time'] = stus2[0]['Begin_time']
                line['Contest_type'] = stus2[0]['Contest_type']
            self.render('html/User.html', Person_id=user, Problem=stus,
                        Length=(15 * (15 - len(stus))), ProLen=ProLen, jud=jud, Contest=Contest,
                        Length2=(15 * (15 - len(Contest))), ConLen=ConLen, Team=Team, FF=ff,
                        Length3=(15 * (15 - len(Team))))
        elif Type == '11':
            a1 = "'" + user + "'"
            a2 = "'" + self.get_body_argument('UserDeleteProblemID') + "'"
            sql = "delete from Person_Finish_Problem where Person_id = " + a1 + " and Problem_id = " + a2
            self.application.db.delete(sql)
            tmp = "'" + user + "'"
            sql = "select * from Person_Finish_Problem where Person_id = " + tmp
            stus = self.application.db.get_all_obj(sql, "Person_Finish_Problem")
            ProLen = 0
            ff = self.application.db.get_all_obj("select * from Problem", "Problem")
            for line in ff:
                ProLen += 1
                # line = line.split('\t')
                for i in stus:
                    if line['Problem_id'] == i['Problem_id']:
                        i['Problem_name'] = line['Problem_name']
                        i['OJ'] = line['OJ']
                        i['OJ_Pnumber'] = line['OJ_Pnumber']
                        i['Difficulty'] = line['Difficulty_level']
                        i['Link'] = line['Link']
                        i['Algorithm'] = line['Algorithm']
                        break
            sql = "select * from Contest_Person where Person_id = " + tmp
            Contest = self.application.db.get_all_obj(sql, "Contest_Person")
            # ConLen = self.application.db.get_all_obj("select count(*) from Contest", "Contest", "Len")
            ConLen = self.application.db.get_all_obj("select * from Contest", "Contest")

            sql = "select * from Person_Team where Person_id = " + tmp
            Team = self.application.db.get_all_obj(sql, "Person_Team")
            for line in Team:
                thp = "'" + line['Team_id'] + "'"
                tmpName = self.application.db.get_all_obj("select Name from Team where Team_id = " + thp, "Team",
                                                          "Name")
                line['Name'] = tmpName[0]['Name']
            ff.reverse()

            # 确认比赛是否全部完成
            stus1 = self.application.db.get_all_obj(
                "select Problem_id from Person_Finish_Problem where Person_id = " + "'" + user + "'",
                "Person_Finish_Problem", "Problem_id")
            for line in Contest:
                stus2 = self.application.db.get_all_obj(
                    "select Problem_id from Contest_Problem where Contest_id = " + "'" + line['Contest_id'] + "'",
                    "Contest_Problem", "Problem_id")
                ctt = 0
                for xp in stus2:
                    hpp = 0
                    for xxp in stus1:
                        if xxp['Problem_id'] == xp['Problem_id']:
                            hpp = 1
                            break
                    if hpp == 0:
                        ctt += 1
                line['Finish'] = ctt

            for line in Contest:
                stus2 = self.application.db.get_all_obj(
                    "select * from Contest where Contest_id = " + "'" + line['Contest_id'] + "'", "Contest")
                line['Begin_time'] = stus2[0]['Begin_time']
                line['Contest_type'] = stus2[0]['Contest_type']
            self.render('html/User.html', Person_id=user, Problem=stus,
                        Length=(15 * (15 - len(stus))), ProLen=ProLen, jud='11', Contest=Contest,
                        Length2=(15 * (15 - len(Contest))), ConLen=ConLen, Team=Team, FF=ff,
                        Length3=(15 * (15 - len(Team))))
        elif Type == '2' or Type == '21':
            tmp = "'" + user + "'"
            jud = '-1'
            if Type == '2':
                tpp = self.get_body_argument('UserAddConID')
                Contest_id = ""
                for i in range(6):
                    Contest_id += tpp[i]
                tttName = self.application.db.get_all_obj("select Name from Contest where Contest_id = " + Contest_id, "Contest",
                                                          "Name")
                tpName = "'" + tttName[0]['Name'] + "'"
                Contest_id = "'" + Contest_id + "'"
                Rank = "'" + self.get_body_argument('UserAddConRank1') + "/" + self.get_body_argument('UserAddConRank2') + "'"
                Time_total = "'" + self.get_body_argument('UserAddConTime') + "'"
                ConTag = "'" + self.get_body_argument('UserAddConTAG') + "'"
                sql = "insert into Contest_Person values (" + Contest_id + "," + tmp + "," + tpName + "," + Rank + "," + Time_total + "," + ConTag + ")"
                jud = '2'
                self.application.db.update(sql)
            elif Type == '21':
                ConID = "'" + self.get_body_argument('UserDeleteConID') + "'"
                sql = "delete from Contest_Person where Contest_id = " + ConID + " and Person_id = " + tmp
                # sql = "delete from Contest_Person where Contest_id = " + ConID
                # print("delete sql: ",sql)
                self.application.db.delete(sql)
                jud = '21'
            sql = "select * from Person_Finish_Problem where Person_id = " + tmp
            stus = self.application.db.get_all_obj(sql, "Person_Finish_Problem")
            ProLen = 0
            ff = self.application.db.get_all_obj("select * from Problem", "Problem")
            for line in ff:
                ProLen += 1
                # line = line.split('\t')
                for i in stus:
                    if line['Problem_id'] == i['Problem_id']:
                        i['Problem_name'] = line['Problem_name']
                        i['OJ'] = line['OJ']
                        i['OJ_Pnumber'] = line['OJ_Pnumber']
                        i['Difficulty'] = line['Difficulty_level']
                        i['Link'] = line['Link']
                        i['Algorithm'] = line['Algorithm']
                        break
            sql = "select * from Contest_Person where Person_id = " + tmp
            Contest = self.application.db.get_all_obj(sql, "Contest_Person")
            ConLen = self.application.db.get_all_obj("select * from Contest", "Contest")
            # ConLen = self.application.db.get_all_obj("select count(*) from Contest", "Contest", "Len")

            sql = "select * from Person_Team where Person_id = " + tmp
            Team = self.application.db.get_all_obj(sql, "Person_Team")
            for line in Team:
                thp = "'" + line['Team_id'] + "'"
                tmpName = self.application.db.get_all_obj("select Name from Team where Team_id = " + thp, "Team",
                                                          "Name")
                line['Name'] = tmpName[0]['Name']
            ff.reverse()

            # 确认比赛是否全部完成
            stus1 = self.application.db.get_all_obj(
                "select Problem_id from Person_Finish_Problem where Person_id = " + "'" + user + "'",
                "Person_Finish_Problem", "Problem_id")
            for line in Contest:
                stus2 = self.application.db.get_all_obj(
                    "select Problem_id from Contest_Problem where Contest_id = " + "'" + line['Contest_id'] + "'",
                    "Contest_Problem", "Problem_id")
                ctt = 0
                for xp in stus2:
                    hpp = 0
                    for xxp in stus1:
                        if xxp['Problem_id'] == xp['Problem_id']:
                            hpp = 1
                            break
                    if hpp == 0:
                        ctt += 1
                line['Finish'] = ctt

            for line in Contest:
                stus2 = self.application.db.get_all_obj(
                    "select * from Contest where Contest_id = " + "'" + line['Contest_id'] + "'", "Contest")
                line['Begin_time'] = stus2[0]['Begin_time']
                line['Contest_type'] = stus2[0]['Contest_type']
            self.render('html/User.html', Person_id=user, Problem=stus,
                        Length=(15 * (15 - len(stus))), ProLen=ProLen, jud=jud, Contest=Contest,
                        Length2=(15 * (15 - len(Contest))), ConLen=ConLen, Team=Team, FF=ff,
                        Length3=(15 * (15 - len(Team))))
        elif Type == '41':
            tmp = "'" + user + "'"
            TeamID = "'" + self.get_body_argument('UserDeleteTeamID') + "'"
            sql = "delete from Person_Team where Person_id = " + tmp + " and Team_id = " + TeamID
            self.application.db.delete(sql)
            jud = '31'

            sql = "select * from Person_Finish_Problem where Person_id = " + tmp
            stus = self.application.db.get_all_obj(sql, "Person_Finish_Problem")
            ProLen = 0
            ff = self.application.db.get_all_obj("select * from Problem", "Problem")
            for line in ff:
                ProLen += 1
                # line = line.split('\t')
                for i in stus:
                    if line['Problem_id'] == i['Problem_id']:
                        i['Problem_name'] = line['Problem_name']
                        i['OJ'] = line['OJ']
                        i['OJ_Pnumber'] = line['OJ_Pnumber']
                        i['Difficulty'] = line['Difficulty_level']
                        i['Link'] = line['Link']
                        i['Algorithm'] = line['Algorithm']
                        break
            sql = "select * from Contest_Person where Person_id = " + tmp
            Contest = self.application.db.get_all_obj(sql, "Contest_Person")
            # ConLen = self.application.db.get_all_obj("select count(*) from Contest", "Contest", "Len")
            ConLen = self.application.db.get_all_obj("select * from Contest", "Contest")

            sql = "select * from Person_Team where Person_id = " + tmp
            Team = self.application.db.get_all_obj(sql, "Person_Team")
            for line in Team:
                thp = "'" + line['Team_id'] + "'"
                tmpName = self.application.db.get_all_obj("select Name from Team where Team_id = " + thp, "Team",
                                                          "Name")
                line['Name'] = tmpName[0]['Name']
            ff.reverse()

            # 确认比赛是否均完成
            stus1 = self.application.db.get_all_obj(
                "select Problem_id from Person_Finish_Problem where Person_id = " + "'" + user + "'",
                "Person_Finish_Problem", "Problem_id")
            for line in Contest:
                stus2 = self.application.db.get_all_obj(
                    "select Problem_id from Contest_Problem where Contest_id = " + "'" + line['Contest_id'] + "'",
                    "Contest_Problem", "Problem_id")
                ctt = 0
                for xp in stus2:
                    hpp = 0
                    for xxp in stus1:
                        if xxp['Problem_id'] == xp['Problem_id']:
                            hpp = 1
                            break
                    if hpp == 0:
                        ctt += 1
                line['Finish'] = ctt

            for line in Contest:
                stus2 = self.application.db.get_all_obj(
                    "select * from Contest where Contest_id = " + "'" + line['Contest_id'] + "'", "Contest")
                line['Begin_time'] = stus2[0]['Begin_time']
                line['Contest_type'] = stus2[0]['Contest_type']
            self.render('html/User.html', Person_id=user, Problem=stus,
                        Length=(15 * (15 - len(stus))), ProLen=ProLen, jud=jud, Contest=Contest,
                        Length2=(15 * (15 - len(Contest))), ConLen=ConLen, Team=Team, FF=ff,
                        Length3=(15 * (15 - len(Team))))


class TeamInformationHandler(RequestHandler):
    def get(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        Person_id = user
        Team_id = "'" + self.get_argument('Team_id') + "'"
        Team = self.application.db.get_all_obj("select * from Team where Team_id = " + Team_id, "Team")
        Person_Team = self.application.db.get_all_obj("select * from Person_Team where Team_id = " + Team_id,
                                                      "Person_Team")
        Person = []
        Person.append(Person_id)
        for line in Person_Team:
            if line['Person_id'] not in Person:
                Person.append(line['Person_id'])
        Person.append("无")
        Person.append("无")
        Contest = self.application.db.get_all_obj("select * from Contest_Team where Team_id = " + Team_id,
                                                  "Contest_Team")
        ConLen = self.application.db.get_all_obj("select * from Contest", "Contest")


        stus1 = self.application.db.get_all_obj("select Problem_id from Person_Finish_Problem where Person_id = " + "'" + Person_id + "'",
                                                  "Person_Finish_Problem","Problem_id")
        for line in Person:
            if line != '无' and line != Person_id:
                stus1.extend(self.application.db.get_all_obj("select Problem_id from Person_Finish_Problem where Person_id = " + "'" + line + "'",
                                                  "Person_Finish_Problem","Problem_id"))
        for line in Contest:
            stus2 = self.application.db.get_all_obj("select Problem_id from Contest_Problem where Contest_id = " + "'" + line['Contest_id'] + "'",
                                                    "Contest_Problem","Problem_id")
            ctt = 0
            for xp in stus2:
                hpp = 0
                for xxp in stus1:
                    if xxp['Problem_id'] == xp['Problem_id']:
                        hpp = 1
                        break
                if hpp == 0:
                    ctt += 1
            line['Finish'] = ctt
        for line in Contest:
            stus2 = self.application.db.get_all_obj(
                "select * from Contest where Contest_id = " + "'" + line['Contest_id'] + "'", "Contest")
            line['Begin_time'] = stus2[0]['Begin_time']
            line['Contest_type'] = stus2[0]['Contest_type']
        self.render('html/TeamInformation.html', Person_id=Person_id, Team=Team, Person=Person, jud='-1',
                    Contest=Contest, ConLen=ConLen)

    def post(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        Person_id = user
        Team_id = "'" + self.get_argument('Team_id') + "'"
        Type = self.get_argument('Type')
        Today = datetime.now().strftime("%Y-%m-%d")
        TodayTime = "'" + str(Today) + "'"
        jud = '-1'
        if Type == '3':
            ConID = "'" + self.get_body_argument('TeamDeleteConID') + "'"
            sql = "delete from Contest_Team where Team_id = " + Team_id + " and Contest_id = " + ConID
            self.application.db.delete(sql)
            jud = '5'
        elif Type == '2':
            tpp = self.get_body_argument('TeamAddConID')
            Contest_id1 = ""
            for i in range(6):
                Contest_id1 += tpp[i]
            Contest_id1 = "'" + Contest_id1 + "'"
            tttName = self.application.db.get_all_obj("select Name from Contest where Contest_id = " + Contest_id1,
                                                      "Contest",
                                                      "Name")
            tpName = "'" + tttName[0]['Name'] + "'"
            Rank = "'" + self.get_body_argument('TeamAddConRank1') + "/" + self.get_body_argument(
                'TeamAddConRank2') + "'"
            Time_total = "'" + self.get_body_argument('TeamAddConTime') + "'"
            ConTag = "'" + self.get_body_argument('TeamAddConTAG') + "'"
            sql = "insert into Contest_Team values (" + Contest_id1 + "," + Team_id + "," + tpName + "," + Rank + "," + Time_total + "," + ConTag + ")"
            jud = '4'
            self.application.db.update(sql)
        elif Type == '1':
            TeamName = self.get_body_argument('TeamName')
            TeamOldPerson2 = self.get_argument('Person2')
            TeamOldPerson3 = self.get_argument('Person3')
            TeamPerson2 = self.get_body_argument('TeamPerson2')
            TeamPerson3 = self.get_body_argument('TeamPerson3')
            if TeamName != "":
                TeamName = "'" + TeamName + "'"
                self.application.db.update("update Team set Name = " + TeamName + "where Team_id = " + Team_id)
            tmpPerson = self.application.db.get_all_obj("select Person_id from Person", "Person", "Person_id")
            print("tmpPerson", tmpPerson)
            if TeamPerson2 == "" and TeamPerson3 != "":
                if TeamPerson3 == user or TeamPerson3 == TeamOldPerson2 or TeamPerson3 == TeamOldPerson3 or (
                        TeamPerson3 not in [h['Person_id'] for h in tmpPerson]):
                    jud = '2'
                else:
                    TeamOldPerson3 = "'" + TeamOldPerson3 + "'"
                    TeamPerson3 = "'" + TeamPerson3 + "'"
                    self.application.db.delete(
                        "delete from Person_Team where Person_id = " + TeamOldPerson3 + " and Team_id = " + Team_id)
                    self.application.db.update(
                        "insert into Person_Team values( " + TeamPerson3 + "," + Team_id + "," + TodayTime + "," + "'无'" + ")")
                    jud = '3'
            elif TeamPerson3 == "" and TeamPerson2 != "":
                if TeamPerson2 == user or TeamPerson2 == TeamOldPerson2 or TeamPerson2 == TeamOldPerson3 or (
                        TeamPerson2 not in [h['Person_id'] for h in tmpPerson]):
                    jud = '1'
                else:
                    TeamOldPerson2 = "'" + TeamOldPerson2 + "'"
                    TeamPerson2 = "'" + TeamPerson2 + "'"
                    self.application.db.delete(
                        "delete from Person_Team where Person_id = " + TeamOldPerson2 + " and Team_id = " + Team_id)
                    self.application.db.update(
                        "insert into Person_Team values( " + TeamPerson2 + "," + Team_id + "," + TodayTime + "," + "'无'" + ")")
                    jud = '3'
            elif TeamPerson3 != "" and TeamPerson2 != "":
                if TeamPerson2 == user or TeamPerson2 == TeamOldPerson2 or TeamPerson2 == TeamOldPerson3 or (
                        TeamPerson2 not in [h['Person_id'] for h in tmpPerson]):
                    jud = '1'
                elif TeamPerson3 == user or TeamPerson3 == TeamOldPerson2 or TeamPerson3 == TeamOldPerson3 or (
                        TeamPerson3 not in [h['Person_id'] for h in tmpPerson]):
                    jud = '2'
                else:
                    TeamOldPerson3 = "'" + TeamOldPerson3 + "'"
                    TeamPerson3 = "'" + TeamPerson3 + "'"
                    self.application.db.delete(
                        "delete from Person_Team where Person_id = " + TeamOldPerson3 + " and Team_id = " + Team_id)
                    self.application.db.update(
                        "insert into Person_Team values( " + TeamPerson3 + "," + Team_id + "," + TodayTime + "," + "'无'" + ")")
                    TeamOldPerson2 = "'" + TeamOldPerson2 + "'"
                    TeamPerson2 = "'" + TeamPerson2 + "'"
                    self.application.db.delete(
                        "delete from Person_Team where Person_id = " + TeamOldPerson2 + " and Team_id = " + Team_id)
                    self.application.db.update(
                        "insert into Person_Team values( " + TeamPerson2 + "," + Team_id + "," + TodayTime + "," + "'无'" + ")")
                    jud = '3'

        Team = self.application.db.get_all_obj("select * from Team where Team_id = " + Team_id, "Team")
        Person_Team = self.application.db.get_all_obj("select * from Person_Team where Team_id = " + Team_id,
                                                      "Person_Team")
        Person = []
        Person.append(Person_id)
        for line in Person_Team:
            if line['Person_id'] not in Person:
                Person.append(line['Person_id'])
        Person.append("无")
        Person.append("无")
        Contest = self.application.db.get_all_obj("select * from Contest_Team where Team_id = " + Team_id,
                                                  "Contest_Team")
        ConLen = self.application.db.get_all_obj("select * from Contest", "Contest")

        stus1 = self.application.db.get_all_obj(
            "select Problem_id from Person_Finish_Problem where Person_id = " + "'" + Person_id + "'",
            "Person_Finish_Problem", "Problem_id")
        for line in Person:
            if line != '无' and line != Person_id:
                stus1.extend(self.application.db.get_all_obj(
                    "select Problem_id from Person_Finish_Problem where Person_id = " + "'" + line + "'",
                    "Person_Finish_Problem", "Problem_id"))
        for line in Contest:
            stus2 = self.application.db.get_all_obj(
                "select Problem_id from Contest_Problem where Contest_id = " + "'" + line['Contest_id'] + "'",
                "Contest_Problem", "Problem_id")
            ctt = 0
            for xp in stus2:
                hpp = 0
                for xxp in stus1:
                    if xxp['Problem_id'] == xp['Problem_id']:
                        hpp = 1
                        break
                if hpp == 0:
                    ctt += 1
            line['Finish'] = ctt
        for line in Contest:
            stus2 = self.application.db.get_all_obj(
                "select * from Contest where Contest_id = " + "'" + line['Contest_id'] + "'", "Contest")
            line['Begin_time'] = stus2[0]['Begin_time']
            line['Contest_type'] = stus2[0]['Contest_type']
        self.render('html/TeamInformation.html', Person_id=Person_id, Team=Team, Person=Person, jud=jud,
                    Contest=Contest, ConLen=ConLen)


class PerInformationHandler(RequestHandler):
    def get(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        stus1 = self.application.db.get_all_obj("select Name from school", "school",
                                                "Name")
        stus2 = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                "Name")
        tmp = user
        tmp = "'" + tmp + "'"
        stus3 = self.application.db.get_all_obj("select * from Person where Person_id = " + tmp, "Person")
        for line in stus3:
            School_id = "'" + line['School_id'] + "'"
            now = self.application.db.get_all_obj("select Name from school where School_id = " + School_id, "school",
                                                  "Name")
            line['School_id'] = now[0]['Name']
            Lab_id = "'" + line['Lab_id'] + "'"
            now = self.application.db.get_all_obj("select Name from laboratory where Lab_id = " + Lab_id, "laboratory",
                                                  "Name")
            line['Lab_id'] = now[0]['Name']
        self.render('html/PerInformation.html', Person_id=user, School=stus1, Lab=stus2,
                    Person=stus3[0])

    def post(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        Person_id = user
        tmp = "'" + Person_id + "'"
        stus = self.application.db.get_all_obj("select * from Person where Person_id = " + tmp, "Person")
        Name = self.get_body_argument("Name")
        Gender = self.get_body_argument("Gender")
        Major = self.get_body_argument("Major")
        School = self.get_body_argument("School")
        Grade = self.get_body_argument("Grade")
        Class = self.get_body_argument("Class")
        Lab = self.get_body_argument("Lab")
        if Name == "":
            Name = stus[0]['Name']
        if Gender == "":
            Gender = stus[0]['Gender']
        if School == "":
            School = stus[0]['School']
        if Major == "":
            Major = stus[0]['Major']
        if Grade == "":
            Grade = stus[0]['Grade']
        if Class == "":
            Class = stus[0]['Class']
        if Lab == "":
            Lab = stus[0]['Lab']
        School = "'" + School + "'"
        now = self.application.db.get_all_obj("select School_id from school where Name = " + School, "school",
                                              "School_id")
        School_id = now[0]['School_id']
        Lab = "'" + Lab + "'"
        now = self.application.db.get_all_obj("select Lab_id from laboratory where Name = " + Lab, "laboratory",
                                              "Lab_id")
        Lab_id = now[0]['Lab_id']
        Person_id = "'" + Person_id + "'"
        Name = "'" + Name + "'"
        Gender = "'" + Gender + "'"
        Major = "'" + Major + "'"
        Grade = "'" + Grade + "'"
        Class = "'" + Class + "'"
        School_id = "'" + School_id + "'"
        Lab_id = "'" + Lab_id + "'"
        sql = "update Person set Name = " + Name + ",Gender = " + Gender + ",Major = " + Major + ",Grade = " + Grade + ",Class = " + Class + ",School_id = " + School_id + ",Lab_id = " + Lab_id + " where Person_id = " + Person_id
        self.application.db.update(sql)

        stus1 = self.application.db.get_all_obj("select Name from school", "school",
                                                "Name")
        stus2 = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                "Name")
        tmp = user
        tmp = "'" + tmp + "'"
        stus3 = self.application.db.get_all_obj("select * from Person where Person_id = " + tmp, "Person")
        for line in stus3:
            School_id = "'" + line['School_id'] + "'"
            now = self.application.db.get_all_obj("select Name from school where School_id = " + School_id, "school",
                                                  "Name")
            line['School_id'] = now[0]['Name']
            Lab_id = "'" + line['Lab_id'] + "'"
            now = self.application.db.get_all_obj("select Name from laboratory where Lab_id = " + Lab_id, "laboratory",
                                                  "Name")
            line['Lab_id'] = now[0]['Name']
        self.render('html/PerInformation.html', Person_id=user, School=stus1, Lab=stus2,
                    Person=stus3[0])


class ChangeSerectHandler(RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        # cookie获取user
        user = self.get_cookie('Person_id', None)
        user_jud = None
        if user != None:
            user_jud = self.application.db.get_all_obj("select * from Person where Person_id = " + "'" + user + "'",
                                                   "Person")
        if user_jud == None:
            index_School = self.application.db.get_all_obj("select Name from school", "school",
                                                           "Name")
            index_Lab = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                        "Name")
            self.render('html/index.html', School=index_School, Lab=index_Lab)
        else:
            self.set_cookie('Person_id', user, expires_days=None)
        # user获取成功

        Person_id = user
        tmp = "'" + Person_id + "'"
        stus = self.application.db.get_all_obj("select * from Person where Person_id = " + tmp, "Person")
        OldSerect = self.get_body_argument('OldSerect')
        NewSerect = self.get_body_argument('NewSerect')
        ReNewSerect = self.get_body_argument('ReNewSerect')
        jud = '1'
        if OldSerect != stus[0]['Serect']:
            jud = '1'
        elif NewSerect == "":
            jud = '2'
        elif NewSerect != ReNewSerect:
            jud = '3'
        else:
            self.application.db.update(
                "update Person set Serect = " + "'" + NewSerect + "'" + " where Person_id = " + tmp)
            jud = '4'
        stus1 = self.application.db.get_all_obj("select Name from school", "school",
                                                "Name")
        stus2 = self.application.db.get_all_obj("select Name from laboratory", "laboratory",
                                                "Name")
        tmp = user
        tmp = "'" + tmp + "'"
        stus3 = self.application.db.get_all_obj("select * from Person where Person_id = " + tmp, "Person")
        for line in stus3:
            School_id = "'" + line['School_id'] + "'"
            now = self.application.db.get_all_obj("select Name from school where School_id = " + School_id, "school",
                                                  "Name")
            line['School_id'] = now[0]['Name']
            Lab_id = "'" + line['Lab_id'] + "'"
            now = self.application.db.get_all_obj("select Name from laboratory where Lab_id = " + Lab_id, "laboratory",
                                                  "Name")
            line['Lab_id'] = now[0]['Name']
        self.render('html/SerectError.html', Person_id=user, School=stus1, Lab=stus2,
                    Person=stus3[0], jud=jud)
