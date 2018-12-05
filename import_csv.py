import os
import datetime
import pandas as pd
from sqlalchemy import create_engine


basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'))

#csv导入到sqlite中,提供路径和表名
def csv2sqlite(csvPath, csvTableName):
    # with open(csvPath, encoding='utf-8') as f:
    #     reader = csv.reader(f)
    #     reader.to_sql(csvTableName, engine, if_exists='append', index=False)

    with open(csvPath, encoding='utf-8', errors = 'backslashreplace') as f:
        df = pd.read_csv(f, error_bad_lines=False, encoding='utf-8')
        df['date'] = pd.to_datetime(df['date'])
        df = df.rename(columns={'sender-address':'sender_address', 'recipient-count':'recipient_count', \
        'recipient-address':'recipient_address', 'return-path':'return_path', 'client-h\
        ostname':'client_hostname', 'client-ip':'client_ip', 'server-hostname':'server_hostname'\
        , 'server-ip':'server_ip', 'original-client-ip':'original_client_ip', 'original-server-ip\
        ':'original_server_ip', 'event-id':'event_id', 'total-bytes':'total_bytes', 'connector-id\
        ':'connector_id', 'message-subject':'message_subject', 'source':'source'})
        df.to_sql(csvTableName, engine, if_exists='replace', index_label='id', chunksize=10000)
        # df.to_sql(csvTableName, engine, if_exists='replace', index_label='id', \
        #     dtype={'date': sqlalchemy.types.DateTime}, chunksize=10000)

    # with pd.read_csv(csvPath, encoding = "utf-8") as f:
    #     f.to_sql(csvTableName, engine, if_exists='append', index=False)


csv2sqlite('uploads/result_4_import_test.csv', 'second_half_2018_kazakh')