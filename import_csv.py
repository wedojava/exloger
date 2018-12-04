import os
import pandas as pd
# import csv

from sqlalchemy import create_engine


basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'))

#csv导入到sqlite中,提供路径和表名
def csv2sqlite(csvPath, csvTableName):
    # with open(csvPath, encoding='utf-8') as f:
    #     reader = csv.reader(f)
    #     reader.to_sql(csvTableName, engine, if_exists='append', index=False)

    with open(csvPath, encoding='utf-8', errors = 'backslashreplace') as f:
        reader = pd.read_csv(f, error_bad_lines=False)
        reader.to_sql(csvTableName, engine, if_exists='replace', index_label='id')

    # with pd.read_csv(csvPath, encoding = "utf-8") as f:
    #     f.to_sql(csvTableName, engine, if_exists='append', index=False)

    # df = pd.read_csv(csvPath, encoding='utf-8')
    # df.to_sql(csvTableName, engine, if_exists='append', index=False)


csv2sqlite('uploads/result.csv', 'second_half_2018_Kazakh')