from baisc import Baisc


class HoldersNum(Baisc):
    def read_tushare_data(self, ts_code):
        pro = self.init_tushare()
        df = pro.stk_holdernumber(ts_code=ts_code)
        print(df)
        return df

    def update_data(self, data):
        db, cursor = self.init_db()


if __name__ == "__main__":
    a = HoldersNum()
    a.read_tushare_data('300199.SZ')
