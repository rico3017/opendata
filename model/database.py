from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from mysql import connector

#parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
#sys.path.insert(0,parentdir)
import myconfig

def getConnection():
    conn = connector.connect(**myconfig.db)
    return conn

myDbConPool = pool.QueuePool(getConnection,pool_size=myconfig.db_option["pool_size"], 
                            max_overflow = myconfig.db_option["max_overflow"], echo = True, timeout = 3600)

#engine = create_engine("mysql+mysqlconnector://", pool = myDbConPool)
engine = create_engine("mysql+mysqlconnector://%s:%s@%s/%s"%(myconfig.db["user"], myconfig.db["password"], myconfig.db["host"], myconfig.db["database"]),
                       max_overflow = 0, pool_size = 5)   
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Model = declarative_base(name="Model")
Model.query = db_session.query_property()


def testConn():
    conn = myDbConPool.connect()
    cursor = conn.cursor(dictionary = True)
    cursor.execute("show processlist")
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    conn.close()

#To define your models, just subclass the Model class that was created by the code above
