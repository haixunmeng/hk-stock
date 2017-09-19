import requests

import uuid

from datetime import datetime

from multiprocessing.dummy import Pool as ThreadPool

from db import insert_department_eva, Evaluation, db_session

hk_stock_url = "http://web.ifzq.gtimg.cn/hk/tzpj/data/tzpj?p=%s&lmt=40"

def pull_bank_invetement(pageIndex):
    rps = requests.get(hk_stock_url % (pageIndex + 1))

    if not rps.status_code == 200:
        print("page %s request fail!!!" % pageIndex)
        return

    rps.encoding = "utf-8"
    rps_data = rps.json()

    if not rps_data['code'] == 0:
        print("%s %s" % (rps_data, hk_stock_url % pageIndex))
        return

    list(map(lambda x: insert_department_eva(map_to_class(x)), rps_data['data']['data']))


def map_to_class(eva):
    return Evaluation(id=''.join(str(uuid.uuid1()).split('-')), stock_code=eva['SEC_CODE'], stock_name=eva['ABRSTACT_NAME'], department_code=eva['DEPARTMENT_CODE'],
        department_name=eva['DEPARTMENT_NAME'], eva_rank="买入" if "2" == eva['EVA_RANK'] else "卖出" if "0" == eva['EVA_RANK'] else "持有",
        aim_price= 0 if '' == eva['AIM_PRICE'] else eva['AIM_PRICE'], time=eva['TIME'], url=eva['URL'], create_time=datetime.now())

if __name__ == "__main__":
    rps = requests.get("http://web.ifzq.gtimg.cn/hk/tzpj/data/tzpj?p=1&lmt=40")

    rps.encoding = "utf-8"
    rps_json = rps.json()

    pool = ThreadPool()
    pool.map(pull_bank_invetement, list(range(rps_json['data']['sumPage'])))

    db_session.commit()

