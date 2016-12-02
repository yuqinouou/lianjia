import threading

import login
import db
import spider

# load constants
from constants import *

# create cookie file
import create_cookie

command = "CREATE TABLE IF NOT EXISTS xiaoqu (Neighbourhood TEXT, District TEXT, Area TEXT, Built TEXT, Avg_Price TEXT, N_Selling TEXT)"
db_xq = db.SQLiteWraper(xqDB, command)
command = "CREATE TABLE IF NOT EXISTS chengjiao (Hyperlink TEXT, Neighbourhood TEXT, Layout TEXT, Square TEXT, District TEXT, Area TEXT, Facing TEXT, Floor TEXT, Remodel TEXT, Date TEXT, Price_per_sq TEXT, Price TEXT, Type TEXT, School TEXT, Metro TEXT)"
db_cj = db.SQLiteWraper(cjDB, command)

# create lock
lock = threading.Lock()
# running query
# spider.do_xiaoqu_spider(db_xq, lock)
spider.do_chengjiao_spider(db_cj, lock)
spider.exception_spider(db_xq, db_cj, lock)
