from record import loadFromDb
import getpass


raise('Refactor out this as we will use Postgres roles for user mgt.')

class MyUser(object):
    "I copied this into a new module"
    def __init__(self, user, pwd):
        self.user = None
        self.__test = False
        self.role = None
        self.lst_users = []
        self.user_role = {}    #view id: role
        #__dic = {}
        sql = "select username, pwd, role, windows_user from tbl_users order by username"
       # Db.c.execute(sql)
        lst = loadFromDb(sql)
        print len(lst)
        for rec in lst:
            __dic = lst.toDict('username', 'pwd')
            self.lst_users.append(rec.username)
            __dicRole = lst.toDict('username', 'role')
            __dicWindosUser = lst.toDict('username', 'windows_user')

        if __dic.has_key(user):
            if __dic[user]==pwd:
                self.__test = user
                self.user = user
                self.role = __dicRole[user]

            elif __dicWindosUser[user]==str(getpass.getuser()):
                self.__test = user
                self.user = user
                self.role = __dicRole[user]
            else: pass
            #sql = "select view_id, role from tbl_users_view where user='%s'" % user
            sql = """SELECT tbl_users_view.id, tbl_users_view.view_id, tbl_users.username, tbl_users.role
                    FROM (tbl_users_view INNER JOIN tbl_users ON tbl_users_view.user_id = tbl_users.id) 
                    INNER JOIN tbl_views ON tbl_users_view.view_id = tbl_views.id
                    WHERE (((tbl_users.username)='%s'))""" % user
            lst = loadFromDb(sql)
            self.user_role = lst.toDict('view_id', 'role')
            
    def __iter__(self):
        for rec in self.lst:
            yield rec
        
    def __str__(self):
        str = ','.join(self.lst_users)
        return ':'+str
    
    def check(self, requst):
        raise("should we try to do this better?")
        if requst=='yardloader':
            if self.user=='admin':
                return True
            else: return False
        elif requst.user=='yard' or requst.user == self.__test:
            return True
        elif self.user=='admin':
            return True
        else:
            return False #self.__test
    
   # check = staticmethod(check)
                    
    def __call__(self):
        return self.__test
    
if __name__=='__main__':
    from record import WhichDb_v3
    WhichDb_v3('Postgress', 'test_01', 'admin', '123')
    t = MyUser('admin', '123')
    print t()
    print t.role
    