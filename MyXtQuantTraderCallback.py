from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant
from Util import logger
import random

class MyXtQuantTraderCallback(XtQuantTraderCallback):
    def on_disconnected(self):
        """
        连接断开
        :return:
        """
        logger.info("connection lost")
        connect()
    def on_stock_order(self, order):
        """
        委托回报推送
        :param order: XtOrder对象
        :return:
        """
        logger.info(f"委托回报推送,code:{order.stock_code}  status:{order.order_status}   sysid:{order.order_sysid}")
    def on_stock_asset(self, asset):
        """
        资金变动推送  注意，该回调函数目前不生效
        :param asset: XtAsset对象
        :return:
        """
        logger.info(f"资金变动 account_id:{asset.account_id}  cash:{asset.cash}  total_asset:{asset.total_asset}")
    def on_stock_trade(self, trade):
        """
        成交变动推送
        :param trade: XtTrade对象
        :return:
        """
        logger.info(f"成交变动 account_id:{trade.account_id}  stock_code:{trade.stock_code}  order_id:{trade.order_id}")
    def on_stock_position(self, position):
        """
        持仓变动推送  注意，该回调函数目前不生效
        :param position: XtPosition对象
        :return:
        """
        logger.info(f"持仓变动 stock_code:{position.stock_code}  volume:{position.volume}")
    def on_order_error(self, order_error):
        """
        委托失败推送
        :param order_error:XtOrderError 对象
        :return:
        """
        logger.info(f"委托失败 order_id:{order_error.order_id}  error_id:{order_error.error_id}  error_msg:{order_error.error_msg}")
    def on_cancel_error(self, cancel_error):
        """
        撤单失败推送
        :param cancel_error: XtCancelError 对象
        :return:
        """
        logger.info("撤单失败 order_id:{cancel_error.order_id}  error_id:{cancel_error.error_id}  error_msg:{cancel_error.error_msg}")
    def on_order_stock_async_response(self, response):
        """
        异步下单回报推送
        :param response: XtOrderResponse 对象
        :return:
        """
        logger.info(f"异步下单回报推送 account_id:{response.account_id}  order_id:{response.order_id}  seq:{response.seq}")
    def on_account_status(self, status):
        """
        :param response: XtAccountStatus 对象
        :return:
        """
        logger.info(f"XtAccountStatus   account_id:{status.account_id}  account_type:{status.account_type}  status:{status.status}")

# 替换自己的自己账号
acc = StockAccount('1111')
xt_trader = None
def connect():
    global xt_trader
    path = 'D://国金证券QMT交易端//userdata_mini'
    # session_id为会话编号，策略使用方对于不同的Python策略需要使用不同的会话编号
    session_id = random.randint(100000, 999999)
    xt_trader = XtQuantTrader(path, session_id)
    # 创建交易回调类对象，并声明接收回调
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    # 启动交易线程
    xt_trader.start()
    # 建立交易连接，返回0表示连接成功
    connect_result = xt_trader.connect()
    if connect_result != 0:
        import sys
        sys.exit('链接失败，程序即将退出 %d'%connect_result)
    # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
    subscribe_result = xt_trader.subscribe(acc)
    if subscribe_result != 0:
        logger.error('账号订阅失败 %d'%subscribe_result)
    logger.info("connect success")
    return xt_trader

connect()