import configparser
import io
import os
import re
from pre_clean_data import struct_hive_data_tm,struct_hive_data_jd


def multi_blank_clean(s1):
    s1 = re.sub(r"[\s]+", "", s1)
    return s1

def read_phone_v1(input_file, cfg_file):
    config = configparser.ConfigParser()
    phone_model_dict = {}
    with io.open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if line == "":continue
            line_list = line.split("\t")
            if len(line_list) != 3:continue
            line_list = [tmp_item.strip() for tmp_item in line_list]
            p_brand, p_model, p_time = line_list
            struct_model = p_model + "|" + p_time
            if p_brand.lower() not in phone_model_dict:
                phone_model_dict[p_brand.lower()] = [struct_model]
            else:
                phone_model_dict[p_brand.lower()].append(struct_model)
    print(phone_model_dict)
    config.read(cfg_file,encoding="utf-8")
    brand_list = config['brand_lst']['brand'].strip().split(",")
    for brand_item in brand_list:
        p_list = config[brand_item]['model_no'].strip().split(",")
        p_list_ = [tmp.lower().replace(" ","") for tmp in p_list]
        key_str = config[brand_item]['en_brand_name'].lower() + "/" + config[brand_item]['ch_brand_name']
        if key_str not in phone_model_dict:continue
        for p_item in phone_model_dict[key_str]:
            if p_item.lower().replace("5g","").replace(" ","") not in p_list_:
                p_list.append(p_item.replace("5g ",""))
            else:
                continue
        config.set(brand_item,"model_no",",".join(p_list))
    with io.open("config_data/new_config.cfg", "w", encoding="utf-8") as f2:
        config.write(f2)


def read_phone(input_file,cfg_file):
    config_1 = configparser.ConfigParser()
    config_1.read(input_file,encoding="utf-8")
    config_2 = configparser.ConfigParser()
    config_2.read(cfg_file,encoding="utf-8")
    brand_list = config_1['brand_lst']['brand'].strip().split(",")
    for brand in brand_list:
        p_list = config_1[brand]['model_no'].strip().split(",")
        p_list_ = [tmp.replace(" ","") for tmp in p_list]
        tmp_device_list = []    #此list添加的元素是只包含手机型号且去空格转小写了
        for p_list_item in p_list_:
            tmp_device_list.append(p_list_item.split("|")[0])
        ori_list = config_2[brand]['brand_model'].strip().split(",")
        ori_list_ = [tmp.lower().replace(" ","") for tmp in ori_list]
        for tmp_device in tmp_device_list:
            if tmp_device.lower() not in ori_list_:
                ori_list.append(tmp_device)
            else:
                continue
        config_2.set(brand,"brand_model",",".join(ori_list))
    with io.open("config_data/new_config_update.cfg", "w", encoding="utf-8") as f2:
        config_2.write(f2)


def multi_pixel_clean(s1):
    s1 = re.sub('\d+万?像素', " ", s1)
    s1 = re.sub('\d+万?超清像素', " ", s1)
    return s1


def special_words_reg(word_str):
    pattern = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", word_str)
    pattern = re.sub(u"\\（.*?\\）|\\{.*?}|\\[.*?]", "", pattern)
    brand_name_item = re.sub('\W+', '', pattern).replace("_", '').lower()
    return pattern


def multi_generation_clean(s1):
    s1 = re.sub("5g", "", s1.lower())
    s1 = re.sub("4g", "", s1.lower())
    return s1


def multi_version_clean(s1):
    s1 = re.sub("青春版","青春",s1)
    return s1


def model_clean_ext(sku_name, device_list):
    '''
    The function is updated in 2020.09.27 by gcw.
    :param sku_name:
    :param device_list:
    :return:
    '''
    sku_name = multi_blank_clean(sku_name.lower())
    brand_st_dict = {}
    for m1 in device_list:
        m1_ = multi_version_clean(m1)
        st_brand_rgx = re.compile(m1_)
        rgx_result = st_brand_rgx.search(sku_name)
        if rgx_result == None:
            continue
        brand_st_dict[m1] = rgx_result.span()

    if len(brand_st_dict) == 0: return None
    return brand_st_dict


def load_model2brand():
    model_dict = {}
    honour_brand_model = "30青春版,30,30pro,30s,20青春版,20s,20i,10青春版,10,9青春版,8青春版,20,20pro,9,8,7,6,6plus,7i,honor,x10max,x10,9x,9xpro,8xmax,8x,3x,x2,x1,畅玩9a,畅玩7a,畅玩6a,畅玩7c,畅玩5x,畅玩6x,畅玩5a,畅玩6,畅玩5,畅玩5c,畅玩4x,畅玩4c,畅玩4,3c畅玩版,v30pro,v30,v20,v10,v9,v9play,v8,magic2,note10,4a,3c,play4,play3,play3e,play,play4pro,play4t,play4tpro"
    huawei_brand_model = "mate40pro,mate40rs保时捷,mate30epro,mate30,mate30pro,mate20pro,mate10,mate20x,mate9,mate8,mate9pro,mate7,mates,mate,mate2,nova7,nova7pro,nova7se,nova6,nova4,nova2s,nova5i,nova5z,nova5ipro,nova4e,nova5pro,nova3i,nova2plus,nova青春版,nova,nova2,畅享20pro,畅享10,畅享10plus,畅享9plus,畅享7s,畅享7plus,畅享20plus,畅享20,畅享z,畅享10e,畅享10s,畅享9,畅享9s,畅享8,畅享7,畅享6s,畅享6,畅享5s,畅享5,p20pro,p40pro,p40,p30,p30pro,p10plus,p9,p9plus,p8,p8lite,麦芒9,麦芒5,麦芒4,g9青春版,g7plus,ascendp7,g9plus,ascendg7,ascendp6,c199,c8812,u9500,g330,c8813,ascendg700,g730,y300,ascendw2,ascendd2,y635,8800,g300,ascendp1,g520,g510,y511,ascendg6,g620,vision,w1,y210,g610,c8600,g309t"
    honour_list = honour_brand_model.strip().split(",")
    huawei_list = huawei_brand_model.strip().split(",")
    for huawei_item in huawei_list:
        model_dict[huawei_item] = "华为"
    for honour_item in honour_list:
        model_dict[honour_item] = "荣耀"
    return model_dict


def extract_brand(ori_file_jd, ori_file_tmall):
    huawei_list = []
    err_lst = []
    if not os.path.exists(ori_file_jd):
        data_list_jd = []
    else:
        data_list_jd = struct_hive_data_jd(ori_file_jd)
    if not os.path.exists(ori_file_tmall):
        data_list_tmall = []
    else:
        data_list_tmall = struct_hive_data_tm(ori_file_tmall)
    data_list_all = data_list_jd + data_list_tmall
    model_dict = load_model2brand()
    model_list = list(model_dict.keys())

    for product_info_dict in data_list_all:
        if len(product_info_dict) != 9: continue
        brand_id_std = product_info_dict['brand_id_std']
        brand_name_std = product_info_dict['brand_name_std']
        pid = product_info_dict['pid']
        title = product_info_dict['title']
        brand_name = product_info_dict['brand_name']
        describe = product_info_dict['describe']
        iphone_into = product_info_dict['iphone_into']
        data_source = product_info_dict['data_source']
        sku_name = str(iphone_into) + str(title)
        if brand_id_std != "10561609": continue
        sku_name_tmp = multi_pixel_clean(sku_name)
        sku_name_tmp = special_words_reg(sku_name_tmp)
        tmp_dict = model_clean_ext(sku_name_tmp, model_list)

        if tmp_dict == None:
            err_lst.append(product_info_dict)
            continue

        tmp = ""
        span_start = 10000
        span_end = -1
        for k, v in tmp_dict.items():  # 找到商品名中最前面的品牌
            if v[0] < span_start:
                tmp = k
                span_start = v[0]
                span_end = v[1]
            elif v[0] == span_start:  # 如果起点相同，对品牌进行最长匹配
                if v[1] > span_end:
                    tmp = k
                    span_start = v[0]
                    span_end = v[1]
            else:
                continue

        if model_dict[tmp] == "华为":
            huawei_list.append(product_info_dict)

    with open("./result_data_updata_1210/huawei_sku.txt","w",encoding="utf-8") as f1:
        for huawei_item in huawei_list:
            f1.write("%s\t%s\t%s\t%s\n" %(huawei_item['pid'],huawei_item['title'],huawei_item['iphone_into'],huawei_item['data_source']))

def lengthOfLongestSubstring(s):
    """
    :type s: str
    :rtype: int
    """
    x_list = []
    max_len_list = []
    # flag = len(s)
    for i in range(len(s)):
        if s[i] not in x_list:
            x_list.append(s[i])
        else:
            idx = x_list.index(s[i])
            x_list = x_list[idx + 1:]
        max_len_list.append(len(x_list))
    print(max(max_len_list))


if __name__ == "__main__":
    # cfg_file = './config_data/phone_model_2020.cfg'
    # ori_file = './config_data/phone_model.cfg'
    # # read_phone("config_data/phone.txt", cfg_file)
    # read_phone(cfg_file,ori_file)
    # input_file_jd = "./cnt_data_1201/jd_phone_data.txt"
    # input_file_tm = "./cnt_data_1201/tmall_phone_data.txt"
    # extract_brand(input_file_jd,input_file_tm)
    # s = ['1','4','8','2']
    # x = s[::-1]
    # print(x)

    # leetcode
    s = "abcabcbb"
    lengthOfLongestSubstring(s)