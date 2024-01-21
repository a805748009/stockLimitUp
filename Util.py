from xtquant.xtpythonclient import XtPosition,XtOrder
import logging

logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为 DEBUG，你可以根据需要调整级别
    format='%(asctime)s [%(levelname)s] %(message)s',  # 设置日志格式
    handlers=[
        logging.FileHandler('log.txt'),  # 输出到文件，文件名为 log.txt
        logging.StreamHandler()  # 输出到控制台
    ]
)
logger = logging.getLogger(__name__)

def encode_xt_position(obj):
    if isinstance(obj, XtPosition):
        return {
            "account_id": obj.account_id,
            "stock_code": obj.stock_code,
            "volume": obj.volume,
            "can_use_volume": obj.can_use_volume,
            "open_price": obj.open_price,
            "market_value": obj.market_value,
        }
    return obj

def encode_xt_order(obj):
    if isinstance(obj, XtOrder):
        return {
            "account_id": obj.account_id,
            "stock_code": obj.stock_code,
            "order_id": obj.order_id,
            "order_time": obj.order_time,
            "order_type": obj.order_type,
            "order_volume": obj.order_volume,
            "price_type": obj.price_type,
            "price": obj.price,
            "traded_volume": obj.traded_volume,
            "traded_price": obj.traded_price,
            "order_status": obj.order_status,
            "status_msg": obj.status_msg,
        }
    return obj