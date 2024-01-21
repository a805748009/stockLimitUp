#coding=utf-8
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant
from flask import Flask, jsonify, request
from MyXtQuantTraderCallback import connect,acc,xt_trader
from Util import encode_xt_position,logger,encode_xt_order
import json
from functools import wraps


app = Flask(__name__)


# 自定义装饰器，用于参数校验
def validate_params():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.args.get('token')
            if token != 'qqqhxyrequeis':
                return jsonify({"error": f"token error"}), 400
            # 调用原始的视图函数
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/account', methods=['GET'])
@validate_params()
def account():
    asset = xt_trader.query_stock_asset(acc)
    if asset:
        response = {
            'totalAmount': asset.total_asset,
            'availableAmount': asset.cash,
            'withdrawableAmount': asset.total_asset - asset.frozen_cash,
            'frozenAmount': asset.frozen_cash,
        }
        logger.info('查询账户: ',response)
        return jsonify(response)
    return jsonify({})

@app.route('/order_stock', methods=['GET'])
@validate_params()
def order_stock():
    stock_code = request.args.get('stock_code')
    order_type = int(request.args.get('order_type'))
    order_volume = int(request.args.get('order_volume'))
    price  = float(request.args.get('price'))
    fix_result_order_id = xt_trader.order_stock(acc, stock_code, order_type, order_volume, xtconstant.FIX_PRICE, price, 'hxy', 'remark')
    logger.info(f"下单 Stock Code: {stock_code}, Order Type: {order_type}, Order Volume: {order_volume},  Price: {price}, orderId: {fix_result_order_id}")
    return jsonify({'order_id': fix_result_order_id})

@app.route('/cancel_order', methods=['GET'])
@validate_params()
def cancel_order():
    order_id = int(request.args.get('order_id'))
    cancel_order_result = xt_trader.cancel_order_stock(acc, order_id)
    logger.info(f"撤单 order_id: {order_id}, cancel_order_result: {cancel_order_result == 0}")
    return jsonify({'result': cancel_order_result == 0})

@app.route('/query_stock_positions', methods=['GET'])
@validate_params()
def query_stock_positions():
    positions = xt_trader.query_stock_positions(acc)
    logger.info(f"查询持仓len:{len(positions)}")
    if len(positions) != 0:
        strPos = json.dumps(positions, indent=2,default=encode_xt_position)
        logger.info(f"持仓:{strPos}")
        return jsonify({'items': json.loads(strPos)})
    return jsonify({'items': []})

@app.route('/query_stock_orders', methods=['GET'])
@validate_params()
def query_stock_orders():
    orders = xt_trader.query_stock_orders(acc)
    logger.info(f"查询委托len:{len(orders)}")
    if len(orders) != 0:
        strPos = json.dumps(orders, indent=2,default=encode_xt_order)
        logger.info(f"委托:{strPos}")
        return jsonify({'items': json.loads(strPos)})
    return jsonify({'items': []})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084)

