import threading
import sqlite3

class SQLiteWraper(object):
    def __init__(self, path, command='', *args, **kwargs):
        self.lock = threading.RLock() #lock
        self.path = path #params

        if command!='':
            conn=self.get_conn()
            cu=conn.cursor()
            cu.execute(command)

    def get_conn(self):
        conn = sqlite3.connect(self.path)#,check_same_thread=False)
        conn.text_factory = str
        return conn

    def conn_close(self,conn=None):
        conn.close()

    def conn_trans(func):
        def connection(self,*args,**kwargs):
            self.lock.acquire()
            conn = self.get_conn()
            kwargs['conn'] = conn
            rs = func(self,*args,**kwargs)
            self.conn_close(conn)
            self.lock.release()
            return rs
        return connection

    @conn_trans
    def execute(self,command,method_flag=0,conn=None):
        cu = conn.cursor()
        try:
            if not method_flag:
                cu.execute(command)
            else:
                cu.execute(command[0],command[1])
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(e)
            return -1
        except Exception as e:
            print(e)
            return -2
        return 0

    @conn_trans
    def fetchall(self,command="select name from xiaoqu",conn=None):
        cu=conn.cursor()
        lists=[]
        try:
            cu.execute(command)
            lists=cu.fetchall()
        except Exception as e:
            print(e)
            pass
        return lists

def gen_xiaoqu_insert_command(info_dict):
    info_list=[u'Neighbourhood',u'District',u'Area',u'Built',u'Avg_Price',u'N_Selling']
    t=[]
    for il in info_list:
        if il in info_dict:
            t.append(info_dict[il])
        else:
            t.append('')
    t=tuple(t)
    command=(r"insert into xiaoqu values(?,?,?,?,?,?)",t)
    return command


def gen_chengjiao_insert_command(info_dict):
    info_list=[u'Hyperlink',u'Neighbourhood',u'Layout',u'Square',u'District',u'Area',u'Facing',u'Floor',u'Remodel',u'Date',u'Price_per_sq',u'Price',u'Type',u'School',u'Metro']
    t=[]
    for il in info_list:
        if il in info_dict:
            t.append(info_dict[il])
        else:
            t.append('')
    t=tuple(t)
    command=(r"insert into chengjiao values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",t)
    return command
