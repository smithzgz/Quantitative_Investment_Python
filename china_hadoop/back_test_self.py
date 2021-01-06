import matplotlib.pyplot as plt
import pandas as pd
from pymongo import DESCENDING

from database_self import DB_CONN
from stock_pool_strategy import stock_pool, find_out_stocks
from stock_util_self import get_trading_dates
from macd_factor import is_macd_dead, is_macd_gold