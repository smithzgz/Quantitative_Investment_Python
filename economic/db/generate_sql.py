import sys;
import pandas as pd
import time
import datetime

sys.path.append('D:\code\Python\economic\db');
from constants_table import Constants


class GenerateSql():
    def generate_crate_table_sql(self, table_name, field_name_list):
        sql_sentence = "CREATE TABLE " + table_name + "("
        for field_name in field_name_list:
            if (field_name in Constants.sql_key_word):
                field_name += "1"

            if (field_name == "ts_code"):
                sql_sentence += field_name + " VARCHAR(64) PRIMARY KEY,\n"
            elif (field_name.endswith("_date")):
                sql_sentence += field_name + " DATE,\n"
            # elif (field_name.startswith("is_")):
            #     sql_sentence += field_name + " INT,\n"
            elif (field_name in Constants.double_field_name):
                sql_sentence += field_name + " DOUBLE,\n"
            else:
                sql_sentence += field_name + " VARCHAR(64),\n"

        if (table_name == "daily"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,trade_date) )"
        elif (table_name == "daily"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,trade_date) )"
        elif (table_name == "namechange"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,start_date) )"
        elif (table_name == "income"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,end_date) )"
        elif (table_name == "balancesheet"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,end_date) )"
        elif (table_name == "cashflow"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,end_date) )"
        elif (table_name == "dividend"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,end_date) )"
        elif (table_name == "fina_indicator"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,end_date) )"
        elif (table_name == "fina_audit"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,end_date) )"
        elif (table_name == "fina_mainbz"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,end_date) )"
        elif (table_name == "index_daily"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,trade_date) )"
        elif (table_name == "index_weight"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(index_code,con_code,trade_date) )"
        elif (table_name == "index_dailybasic"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,trade_date) )"
        elif (table_name == "fund_nav"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,end_date) )"
        elif (table_name == "fund_div"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(ts_code,ann_date) )"
        elif (table_name == "fund_company"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(name) )"
        elif (table_name == "shibor" or table_name == "shibor_lpr" or table_name == "libor" or table_name == "hibor"):
            sql_sentence = sql_sentence.replace("PRIMARY KEY", "") + "primary key(date) )"
        else:
            sql_sentence = sql_sentence.strip("\n,") + ")"

        print("success generate_crate_table_sql : ", sql_sentence)
        return sql_sentence

    def generate_check_table_exist_sql(self, table_name):
        sql_sentence = "SHOW TABLES LIKE '" + table_name + "'"
        # print("success generate_check_table_exist_sql : ", sql_sentence)
        return sql_sentence

    def generate_delete_table_sql(self, table_name):
        sql_sentence = "DROP TABLE " + table_name
        print("success generate_delete_table_sql : ", sql_sentence)
        return sql_sentence

    def generate_common_query_sql(self, table_name, field_name_list):
        sql_sentence = "SELECT FROM " + table_name
        infix = ""
        suffix = ""
        return "SHOW TABLES LIKE "

    def generate_common_insert_sql(self, table_name, field_name_list, data_list):
        if (len(field_name_list) != len(field_name_list)):
            print("error : generate_common_insert_sql field_name_list != data_list")
            return;
        sql_sentence_list = [];
        for i in range(len(data_list)):
            start1 = time.time()
            sql_sentence = "INSERT INTO " + table_name
            prefix = "("
            suffix = "("
            for field in field_name_list:
                try:
                    data_list[field]
                except KeyError:
                    # print(field, " 字段不存在；")
                    continue;

                if (data_list[field] is None or data_list[field][i] is None):
                    continue
                if (field in Constants.sql_key_word):
                    prefix += field + "1,\n"
                else:
                    prefix += field + ",\n"

                if (pd.isnull(data_list[field][i])):
                    suffix += str(0) + ",\n"
                else:
                    suffix += "'" + str(data_list[field][i]).replace("'", "\\\'") + "',\n"
            prefix = prefix.strip(",\n") + ") values "
            suffix = suffix.strip(",\n") + ")"
            sql_sentence = sql_sentence + prefix + suffix
            end1 = time.time()
            # print("success generate_common_insert_sql : ", i, end1 - start1)
            sql_sentence_list.append(sql_sentence)
        return sql_sentence_list

    def generate_latest_date_sql(self, table_name, field_name, ts_code):
        return "SELECT MAX(" + field_name + ") FROM " + table_name + " WHERE ts_code = \'" + ts_code + "\'"

    def generate_show_all_table(self, db_name):
        return "select table_name from information_schema.tables where table_schema = \'" + db_name + "\'"

    def generate_show_all_field(self, db_name, table_name):
        return "select COLUMN_NAME from information_schema.COLUMNS where table_name = \'" + table_name + "\'"

    def generate_get_original_data(self, field_list, condition):
        return ''


if __name__ == '__main__':
    generateSql = GenerateSql()
    print(generateSql.generate_crate_table_sql("trade_cal", Constants.trade_cal))

    trade_cal_data = ['a', 'a', 'a', 'a']
    print(generateSql.generate_common_insert_sql("trade_cal", Constants.trade_cal, trade_cal_data))
    sys.exit(0)
