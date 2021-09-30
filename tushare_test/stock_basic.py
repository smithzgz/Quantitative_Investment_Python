from baisc import Baisc


class StockBasic(Baisc):
    def read_tushare_data(self):
        pro = self.init_tushare()
        df = pro.stock_basic(
            fields='ts_code,symbol,name,area,industry,fullname,enname,cnspell,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
        print(df)
        return df

    def update_data(self, data):

        pass


if __name__ == "__main__":
    a = StockBasic()
    data = a.read_tushare_data()
    a.update_data(data)
