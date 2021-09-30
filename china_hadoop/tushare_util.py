import tushare_test as ts

def get_tushare_instance(self):
    ts.set_token("47105aced0d886b2c9544eccf752c1b952eb109379a80def6119691f")
    return ts.pro_api()