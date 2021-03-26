import io
import random
from pyhive import hive
import traceback
import configparser
import re
import device_config

def get_data_from_hive():
    try:
        conn = hive.connect(host='172.20.207.6', port=10000, username='supdev')
        # conn = connect(host='172.20.207.6', port=10000, auth_mechanism="PLAIN")
        cur = conn.cursor()
        sql = "select * from dwd.dwd_shouji_model_reg where dt = '2020-12-02'"
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    except Exception as e:
        print(traceback.format_exc())

'''
brand_dict = {'Apple/苹果':['iphone','apple','苹果'],'honor/荣耀':['荣耀','honour'],'Huawei/华为':['华为','huawei'],'vivo':['vivo','iqoo'],'OnePlus/一加':['一加','oneplus'],'OPPO':['oppo'],'realme':['真我','realme'],'Xiaomi/小米':['xiaomi','小米','redmi','红米']}
'''
def count_phone_brand_info():
    brand_num_dict = {}
    brand_dict = {}
    model_dict_all = {}
    product_num_all = 201525
    product_num_now = 154171
    clean_product = 90959
    brand2model_dict = {'Apple/苹果': ['iphone', 'apple', '苹果'], 'honor/荣耀': ['荣耀', 'honour'], 'Huawei/华为': ['华为', 'huawei'],
                  'vivo': ['vivo'], 'OnePlus/一加': ['一加', 'oneplus'], 'OPPO': ['oppo'],
                  'realme': ['真我', 'realme'], 'Xiaomi/小米': ['xiaomi', '小米']}

    def split_brand(model,brand_item):
        if 'redmi' in model or '红米' in model:
            if 'redmi' in model:
                model = model.replace('redmi','红米')
            return model
        else:
            brand_list = brand2model_dict[brand_item]
            for i in range(len(brand_list)):
                model = model.replace(brand_list[i],'')
            return model

    data_tuple = get_data_from_hive()
    if len(data_tuple) != 0:
        for data in data_tuple:
            if len(data) != 8:continue
            pid, brand_id_std, brand_name_std, tmp, title, describe, data_source,dt = data
            if brand_name_std not in brand_num_dict:
                brand_num_dict[brand_name_std] = 1
                brand_dict[brand_name_std] = [data]
            else:
                brand_num_dict[brand_name_std] += 1
                brand_dict[brand_name_std].append(data)
        for brand_item in brand_dict:
            model_dict = {}
            for product_data in brand_dict[brand_item]:
                pid, brand_id_std, brand_name_std, tmp, title, describe, data_source, dt = product_data
                tmp = split_brand(tmp,brand_item)
                if tmp not in model_dict:
                    model_dict[tmp] = 1
                else:
                    model_dict[tmp] += 1
            model_dict_all[brand_item] = model_dict

        with open("./stat_data/brand_num.txt","w",encoding="utf-8") as f1:
            for k, v in brand_num_dict.items():
                rate = v/product_num_all
                f1.write("%s\t%s\t%s\n" %(k,str(v),str(rate)))
            other_brand = product_num_all - clean_product
            other_brand_rate = other_brand/product_num_all
            f1.write("%s\t%s\t%s\n" %('其他',str(other_brand),str(other_brand_rate)))
            f1.flush()

        with open("./stat_data/model_num.txt","w",encoding="utf-8") as f2:
            for brand, brand_dict in model_dict_all.items():
                for k,v in brand_dict.items():
                    rate = v/brand_num_dict[brand]
                    f2.write("%s\t%s\t%s\t%s\n" %(brand,k,str(v),str(rate)))
            f2.flush()


def get_data_from_hive_v1(brand_id):
    try:
        conn = hive.connect(host='172.20.207.6', port=10000, username='supdev')
        # conn = connect(host='172.20.207.6', port=10000, auth_mechanism="PLAIN")
        cur = conn.cursor()
        sql = "select b.sku,coalesce(c.title,d.title) as title,b.brand_id,b.brand_name,b.model_info,a.sale_amount from dwi.dwi_retailers_online_platform_info as a \
        left join dwd.dwd_phone_sku2model_info as b on a.spu_id = b.sku left join tmp.tmp_tmall_shouji_all_20200801 c \
        on b.sku = c.pid left join tmp.tmp_jd_shouji_all_20200801 d on b.sku = d.pid where a.platform_type in ('jd','tmall') \
        and a.dc = 'month' and a.dt = '2020_m11' and a.category3_std = '手机' and a.brand_id_std = '%s' \
        and b.dt = '2020-12-08' and b.sku is not null order by a.sale_amount desc limit 200" %(brand_id)
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    except Exception as e:
        print(traceback.format_exc())


def sku_sample_test(brand_id_list,output_file):
    result_list = []
    for brand_id in brand_id_list:
        data_tuple = get_data_from_hive_v1(brand_id)
        if len(data_tuple) != 0:
            for data_item in data_tuple:
                if len(data_item) != 6:continue
                result_list.append("%s\t%s\t%s\t%s\t%s\t%s" %(data_item[0],data_item[1],data_item[2],data_item[3],data_item[4],data_item[5]))
    with io.open(output_file,"w",encoding="utf-8") as f1:
        f1.write("\n".join(result_list))
        f1.flush()





if __name__ == "__main__":
    brand_id_list = ["10936677","10561609","10365607","10698337","10429338","10694602","10943471","10489679","10282053","10620759","10683308"]
    output_file = "./check_clean_result/1209_check_data.txt"
    sku_sample_test(brand_id_list,output_file)