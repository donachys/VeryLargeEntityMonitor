import sys
import rethinkdb as r
import os
import io

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: compute_table_metrics.py <tablename>")
        exit(-1)
    RDB_HOST =  os.environ.get('RDB_HOST')
    RDB_PORT = os.environ.get('RDB_PORT')
    RDB_DB = "SerIoTics"
    RDB_TABLE = sys.argv[1]
    def createNewConnection():
        return r.connect(host=RDB_HOST, port=RDB_PORT, db=RDB_DB)
    connection = createNewConnection()
    def getStartTime():
        return r.table(RDB_TABLE).filter(r.row['count'].gt(0)).min('time').run(connection)['time']
    def getStopTime():
        return r.table(RDB_TABLE).filter(r.row['count'].gt(0)).max('time').run(connection)['time']
    def getRecordCount():
        return r.table(RDB_TABLE).filter(r.row['count'].gt(0)).sum('count').run(connection)
    def computeRecordsPerSecond(start_time, end_time, num_records):
        return num_records/(end_time-start_time)

    
    print(computeRecordsPerSecond(getStartTime(), getStopTime(), getRecordCount()))
    connection.close()