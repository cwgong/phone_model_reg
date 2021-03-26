#!/usr/bin/env python
#coding=utf-8

import re
from config_tool import ConfigInfo

class DeviceModelClean(object):
    def __init__(self, model_str, ok_model_str, brand_name):
        lst1 = self.multi_blank_clean(model_str.lower()).strip().split(',')
        self._model_lst = list(set(lst1))
        self._brand_name = self.multi_blank_clean(brand_name.lower())
        lst1 = self.multi_blank_clean(ok_model_str.lower()).strip().split(',')
        lst1 = [self._brand_name + tmp for tmp in lst1]
        self._ok_model_lst = list(set(lst1))

    def multi_blank_clean(self, s1):
        s1 = re.sub(r"[\s]+", "", s1)
        return s1

    def model_clean(self,  brand_name):
        brand_name = self.multi_blank_clean(brand_name.lower())
        lst2 = []
        for m1 in self._model_lst:
            tmp_brand = self._brand_name + m1
            if tmp_brand in brand_name:
                lst2.append((tmp_brand, len(tmp_brand)))
            else:
                continue
        lst2 = sorted(lst2, key=lambda  x: x[1], reverse=True)
        model_no = lst2[0][0]
        if model_no in self._ok_model_lst:
            return model_no
        else:
            return None

def multi_blank_clean(s1):
    s1 = re.sub(r"[\s]+", "", s1)
    return s1

def model_clean(sku_name, _model_lst):
    sku_name = multi_blank_clean(sku_name.lower())
    lst2 = []
    for m1 in _model_lst:
        if m1 in sku_name:
            lst2.append((m1, len(m1)))
        else:
            continue
    if len(lst2) == 0: return None
    lst2 = sorted(lst2, key=lambda x: x[1], reverse=True)
    return lst2[0][0]

def model_clean_ext(sku_name, _model_lst):
    sku_name = multi_blank_clean(sku_name.lower())
    lst2 = []
    for m1 in _model_lst:
        if m1 in sku_name:
            lst2.append((m1, len(m1)))
        else:
            continue
    if len(lst2) == 0: return None
    #lst2 = sorted(lst2, key=lambda x: x[1], reverse=True)
    return lst2

def getting_kw(b_lst, phone_name):
    c1 = ConfigInfo("huidingkeji", phone_name)
    model_lst = c1.get_brand_model_lst()
    lst1 = []
    for b in b_lst:
        b = multi_blank_clean(b.lower())
        for m in model_lst:
            m = multi_blank_clean(m.lower())
            lst1.append(b+m)
    return list(set(lst1))


'''
dt
,spu_id
,brand_id_std
,brand_name_std
,sale_amount
,sale_count
,regexp_replace(title, '[\t|\r]', ' ') as title
'''
def brand_data_clean(_model_lst, arg_b_id, f_name, ex_brand_dict):
    r_lst = []
    err_lst = []
    with open("cnt_data/ori_data_2.txt") as f1:
        for line in f1:
            line = line.strip()
            if line == "": continue
            lst9 = line.split("\001")
            if len(lst9) != 7: continue
            lst9 = [tmp.strip() for tmp in lst9]
            dt, sku, b_id, b_name, _, cnt, sku_name = lst9
            if arg_b_id != b_id:  continue
            tmp_lst = model_clean_ext(sku_name, _model_lst)
            if tmp_lst == None:
                err_lst.append(line)
                continue

            for m in tmp_lst:
                tmp, _ = m
                for k, v in ex_brand_dict.items():
                    if k in tmp:
                        tmp = tmp.replace(k, v)
                        break
                r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % \
                             (dt, cnt, tmp, b_id, b_name, sku, sku_name))

    with open("cnt_output/" + f_name, "w") as f2:
        f2.write("\n".join(r_lst))
        f2.flush()
    '''
    with open("cnt_data/" + "err_" + f_name, "w") as f3:
        f3.write("\n".join(err_lst))
        f3.flush()
    '''

def model_stat():
    d1 = {}
    with open("cnt_output/all_phone_model.txt") as f2:
        for line in f2:
            lst1 = line.strip().split("\t")
            if len(lst1) != 7: continue
            dt, cnt, model_no, b_id, b_name, sku, sku_name = lst1
            k = "%s\t%s\t%s\t%s" % (dt, b_id, b_name, model_no)
            if k in d1:
                tmp = d1[k]
                d1[k] = tmp + int(float(cnt))
            else:
                d1[k] = int(float(cnt))

    lst2 = ["%s\t%s" % (k, v) for k, v in d1.items()]
    with open("cnt_output/all_phone_model_stat.txt", "w") as f3:
        f3.write("\n".join(lst2))
        f3.flush()

    season_d = {"2018_m01": "2018-第一季度", "2018_m02": "2018-第一季度", "2018_m03": "2018-第一季度", \
                "2018_m04": "2018-第二季度", "2018_m05": "2018-第二季度", "2018_m06": "2018-第二季度", \
                "2018_m07": "2018-第三季度", "2018_m08": "2018-第三季度", "2018_m09": "2018-第三季度", \
                "2018_m10": "2018-第四季度", "2018_m11": "2018-第四季度", "2018_m12": "2018-第四季度", \
                "2019_m01": "2019-第一季度", "2019_m02": "2019-第一季度", "2019_m03": "2019-第一季度", \
                "2019_m04": "2019-第二季度", "2019_m05": "2019-第二季度", "2019_m06": "2019-第二季度", \
                "2019_m07": "2019-第三季度", "2019_m08": "2019-第三季度", "2019_m09": "2019-第三季度", \
                "2019_m10": "2019-第四季度", "2019_m11": "2019-第四季度", "2019_m12": "2019-第四季度", \
                "2020_m01": "2020-第一季度", "2020_m02": "2020-第一季度", "2020_m03": "2020-第一季度", \
                "2020_m04": "2020-第二季度", "2020_m05": "2020-第二季度", "2020_m06": "2020-第二季度"}
    d2 = {}
    for k, v in d1.items():
        dt, b_id, b_name, model_no = k.split("\t")
        if dt not in season_d: print("error dt(%s)" % dt)
        s1 = season_d[dt]
        k1 = "%s\t%s" % (s1, model_no)
        if k1 in d2:
            tmp = d2[k1]
            d2[k1] = tmp + v
        else:
            d2[k1] = v
    lst3 = ["%s\t%s" % (k, v) for k, v in d2.items()]
    with open("cnt_output/all_phone_season_model_stat.txt", "w") as f3:
        f3.write("\n".join(lst3))
        f3.flush()


def season_stat(listed_cmp_name):
    cmp_name = ''
    model_lst = []
    with open("test_output/" + listed_cmp_name + ".txt") as f1:
        for line in f1:
            lst2 = line.strip().split("\t")
            if len(lst2) != 5: continue
            _, _, info, _, _ = lst2
            cmp_name, tmp_b_name, tmp_model_no = info.strip().split("|")
            model_lst.append(tmp_b_name + tmp_model_no)

    season_d = {"2018_m01": "2018-第一季度", "2018_m02": "2018-第一季度", "2018_m03": "2018-第一季度", \
               "2018_m04": "2018-第二季度", "2018_m05": "2018-第二季度", "2018_m06": "2018-第二季度", \
               "2018_m07": "2018-第三季度", "2018_m08": "2018-第三季度", "2018_m09": "2018-第三季度", \
               "2018_m10": "2018-第四季度", "2018_m11": "2018-第四季度", "2018_m12": "2018-第四季度", \
               "2019_m01": "2019-第一季度", "2019_m02": "2019-第一季度", "2019_m03": "2019-第一季度", \
               "2019_m04": "2019-第二季度", "2019_m05": "2019-第二季度", "2019_m06": "2019-第二季度", \
               "2019_m07": "2019-第三季度", "2019_m08": "2019-第三季度", "2019_m09": "2019-第三季度", \
               "2019_m10": "2019-第四季度", "2019_m11": "2019-第四季度", "2019_m12": "2019-第四季度", \
               "2020_m01": "2020-第一季度", "2020_m02": "2020-第一季度", "2020_m03": "2020-第一季度", \
               "2020_m04": "2020-第二季度", "2020_m05": "2020-第二季度", "2020_m06": "2020-第二季度"}


    d2 = {}
    with open("cnt_output/all_phone_model_stat.txt") as f2:
        for line in f2:
            lst1 = line.strip().split("\t")
            if len(lst1) != 5: continue
            dt, b_id, b_name, model_no, cnt = lst1
            if dt not in season_d: print("error(%s) dt" % dt)
            if model_no not in model_lst: continue
            s = season_d[dt]
            if s in d2:
                tmp = d2[s]
                d2[s] = tmp + int(cnt)
            else:
                d2[s] = int(cnt)

    lst4 = []
    d3 = {}
    total = 0.0
    for s1 in ["2018-第一季度", "2018-第二季度", "2018-第三季度", "2018-第四季度", \
               "2019-第一季度", "2019-第二季度", "2019-第三季度", "2019-第四季度", \
               "2020-第一季度", "2020-第二季度"]:
        if s1 not in d2: continue
        lst4.append((s1, d2[s1]))
        total += d2[s1]
        d3[s1] = d2[s1]
    total_avg = 1.0 * total / len(d3)
    d4 = {}
    d4_freq = {}
    for s2 in ["第一季度", "第二季度", "第三季度", "第四季度"]:
        for k, v in d3.items():
            if s2 not in k: continue
            if s2 in d4:
                tmp = d4[s2]
                d4[s2] = tmp + d3[k]

                tmp1 = d4_freq[s2]
                d4_freq[s2] = tmp1 + 1
            else:
                d4[s2] = d3[k]
                d4_freq[s2] = 1

    d5 = {}
    for k, v in d4.items():
        tmp_avg = 1.0 * v / d4_freq[k]
        d5[k] = tmp_avg / total_avg

    d6 = {}
    for k, v in d5.items():
        for z in lst4:
            s3, cnt = z
            cnt = int(cnt)
            if k not in s3: continue
            d6[s3] = "%s\t%s\t%s\t%s" % (s3, cnt, int(cnt * d5[k]), d5[k])

    lst5 = []
    for s1 in ["2018-第一季度", "2018-第二季度", "2018-第三季度", "2018-第四季度", \
               "2019-第一季度", "2019-第二季度", "2019-第三季度", "2019-第四季度", \
               "2020-第一季度", "2020-第二季度"]:
        if s1 not in d6: continue
        lst5.append(d6[s1])

    with open("listed_cmp_stat/" + listed_cmp_name + ".txt", "w") as f4:
        f4.write("\n".join(lst5))
        f4.flush()


if __name__ == "__main__":
    ex_brand_dict = {"xiaomi": "小米", "redmi": "红米", "huawei": "华为", "honour": "荣耀"}
    '''
    {'honor/荣耀': '10561609', 'Huawei/华为': '10365607', 
    'OPPO': '10694602', 'realme': '10943471',
     'vivo': '10429338', 'Xiaomi/小米': '10698337', 'OnePlus/一加': '10489679'}
    '''

    xiaomi_kw_lst = getting_kw(["小米", "XiaoMi"], "xiaomi")
    brand_data_clean(xiaomi_kw_lst, "10698337", "xiaomi_b_clean.txt", ex_brand_dict)

    redmi_kw_lst = getting_kw(["红米", "Redmi"], "redmi")
    brand_data_clean(redmi_kw_lst, "10698337", "redmi_b_clean.txt", ex_brand_dict)

    huawei_kw_lst = getting_kw(["华为", "huawei"], "huawei")
    brand_data_clean(huawei_kw_lst, "10365607", "huawei_b_clean.txt", ex_brand_dict)

    rongyao_kw_lst = getting_kw(["荣耀", "honour"], "honour")
    brand_data_clean(rongyao_kw_lst, "10561609", "honour_b_clean.txt", ex_brand_dict)

    vivo_kw_lst = getting_kw(["vivo"], "vivo")
    brand_data_clean(vivo_kw_lst, "10429338", "vivo_b_clean.txt", ex_brand_dict)

    iqoo_kw_lst = getting_kw(["iqoo"], "iqoo")
    brand_data_clean(iqoo_kw_lst, "10429338", "iqoo_b_clean.txt", ex_brand_dict)

    oppo_kw_lst = getting_kw(["oppo"], "oppo")
    brand_data_clean(oppo_kw_lst, "10694602", "oppo_b_clean.txt", ex_brand_dict)

    realme_kw_lst = getting_kw(["realme"], "realme")
    brand_data_clean(realme_kw_lst, "10943471", "realme_b_clean.txt", ex_brand_dict)

    yijia_kw_lst = getting_kw(["一加"], "yijia")
    brand_data_clean(yijia_kw_lst, "10489679", "yijia_b_clean.txt", ex_brand_dict)

    name_2_file = {"xiaomi": "小米", "redmi": "红米", "huawei": "华为", "honour": "荣耀"}


    #model_stat()
    '''
    for c_name in ["geergufen", "huidingkeji", "jingdongfang", "juchengufen", "oufeiguang", \
                   "qiutaikeji", "ruishengkeji", "shunyuguangxue", "xinwangda", \
                   "zhaoyichuangxin", "zhuoshengwei"]:
        print(c_name)
        try:
            season_stat(c_name)
        except:
            continue
    '''
    # season_stat("huidingkeji")
    # season_stat("juchengufen")

    pass