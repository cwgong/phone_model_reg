#!/usr/bin/env python3
#coding=utf-8

'''
The script is updated in 2020.09.23 by gcw.
'''

import os
import io
import re
from device_reg_toolkit import DeviceInfoLoading
from pre_clean_data import struct_hive_data_tm,struct_hive_data_jd

class DeviceRegTool(object):
    def __init__(self, standard_device, brand_name):
        if not os.path.exists(standard_device):
            raise Exception("%s config file does exists!" % standard_device)
        try:
            self.brand_name = brand_name
            self.device_loading_obj = DeviceInfoLoading(standard_device, self.brand_name)
            self.device_list = self.device_loading_obj._standard_device_loading()
            self.brand_id = self.device_loading_obj._get_device_id()
        except Exception as e:
            raise e

    def model_clean_ext_v1(self, sku_name, device_list):
        sku_name = self.device_loading_obj.multi_blank_clean(sku_name.lower())
        lst2 = []
        for m1 in device_list:
            m1_ = self.device_loading_obj.multi_version_clean(m1)
            if len(sku_name.split(m1_)) > 1:
                lst2.append((m1, len(m1)))
            else:
                continue
        if len(lst2) == 0: return None
        lst2 = sorted(lst2, key=lambda x: x[1], reverse=True)
        return lst2

    def model_clean_ext(self, sku_name, device_list):
        '''
        The function is updated in 2020.09.27 by gcw.
        :param sku_name:
        :param device_list:
        :return:
        '''
        sku_name = self.device_loading_obj.multi_blank_clean(sku_name.lower())
        brand_st_dict = {}
        for m1 in device_list:
            m1_ = self.device_loading_obj.multi_version_clean(m1)
            st_brand_rgx = re.compile(m1_)
            rgx_result = st_brand_rgx.search(sku_name)
            if rgx_result == None:
                continue
            brand_st_dict[m1] = rgx_result.span()

        if len(brand_st_dict) == 0: return None
        return brand_st_dict

    def _device_reg_clean_v1(self,ori_file,output_file):
        r_lst = []
        err_lst = []
        with io.open(ori_file,"r",encoding="utf-8") as f1:
            for line_str in f1:
                line = line_str.strip()
                if line == "": continue
                lst9 = line.split("\001")
                if len(lst9) != 7: continue
                lst9 = [tmp.strip() for tmp in lst9]
                dt, sku, b_id, b_name, _, cnt, sku_name = lst9
                if b_id != self.brand_id: continue
                flag = self.device_loading_obj.fifth_generation_reg(sku_name)
                fifth_generation = ""
                if flag:
                    fifth_generation = "5G"
                sku_name_tmp = self.device_loading_obj.multi_generation_clean(sku_name)
                sku_name_tmp = self.device_loading_obj.multi_pixel_clean(sku_name_tmp)
                tmp_lst = self.model_clean_ext(sku_name_tmp, self.device_list)

                if tmp_lst == None:
                    err_lst.append(line_str)
                    continue

                for m in tmp_lst:
                    tmp, _ = m
                    for k, v in self.device_loading_obj._exchange_brand_dict.items():
                        if k in tmp:
                            tmp = tmp.replace(k, v)
                            break
                    r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
                                 (dt, cnt, tmp, b_id, b_name, sku, sku_name, fifth_generation))
                    break

        # print(len(err_lst))
        with io.open(output_file+self.brand_name+"_clean_result.txt","w",encoding="utf-8") as f2:
            f2.write("\n".join(r_lst))
            f2.flush()

    def _device_reg_clean_v2(self,ori_file,output_file):
        '''
        The function is updated in 2020.09.27 by gcw.
        :param ori_file:
        :param output_file:
        :return:
        '''
        r_lst = []
        err_lst = []
        with io.open(ori_file,"r",encoding="utf-8") as f1:
            for line_str in f1:
                line = line_str.strip()
                if line == "": continue
                lst9 = line.split("\001")
                if len(lst9) != 7: continue
                lst9 = [tmp.strip() for tmp in lst9]
                dt, sku, b_id, b_name, _, cnt, sku_name = lst9
                if b_id != self.brand_id: continue
                flag = self.device_loading_obj.fifth_generation_reg(sku_name)
                fifth_generation = ""
                if flag:
                    fifth_generation = "5G"
                sku_name_tmp = self.device_loading_obj.multi_generation_clean(sku_name)
                sku_name_tmp = self.device_loading_obj.multi_pixel_clean(sku_name_tmp)
                tmp_dict = self.model_clean_ext(sku_name_tmp, self.device_list)

                if tmp_dict == None:
                    err_lst.append(line_str)
                    continue

                tmp = ""
                span_start = 10000
                span_end = -1
                for k,v in tmp_dict.items():    #找到商品名中最前面的品牌
                    if v[0] < span_start:
                        tmp = k
                        span_start = v[0]
                        span_end = v[1]
                    elif v[0] == span_start:    #如果起点相同，对品牌进行最长匹配
                        if v[1] > span_end:
                            tmp = k
                            span_start = v[0]
                            span_end = v[1]
                    else:
                        continue

                r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
                             (dt, cnt, tmp, b_id, b_name, sku, sku_name, fifth_generation))

        # print(len(err_lst))
        with io.open(output_file+self.brand_name+"_clean_result.txt","w",encoding="utf-8") as f2:
            f2.write("\n".join(r_lst))
            f2.flush()

    def _device_reg_clean(self,ori_file_jd,ori_file_tmall,output_file):
        '''
        The function is updated in 2020.11.30 by gcw.
        :param ori_file:
        :param output_file:
        :return:
        '''
        r_lst = []
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
            sku_name = str(title) + str(iphone_into)
            # dt, sku, b_id, b_name, _, cnt, sku_name = lst9
            if brand_id_std != self.brand_id: continue
            flag = self.device_loading_obj.fifth_generation_reg(sku_name)
            fifth_generation = ""
            if flag:
                fifth_generation = "5G"
            sku_name_tmp = self.device_loading_obj.multi_generation_clean(sku_name)
            sku_name_tmp = self.device_loading_obj.multi_pixel_clean(sku_name_tmp)
            tmp_dict = self.model_clean_ext(sku_name_tmp, self.device_list)

            if tmp_dict == None:
                err_lst.append(product_info_dict)
                continue

            tmp = ""
            span_start = 10000
            span_end = -1
            for k,v in tmp_dict.items():    #找到商品名中最前面的品牌
                if v[0] < span_start:
                    tmp = k
                    span_start = v[0]
                    span_end = v[1]
                elif v[0] == span_start:    #如果起点相同，对品牌进行最长匹配
                    if v[1] > span_end:
                        tmp = k
                        span_start = v[0]
                        span_end = v[1]
                else:
                    continue

            r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
                         (pid,brand_id_std,brand_name_std, tmp, title, describe, data_source))

        # print(len(err_lst))
        with io.open(output_file+self.brand_name+"_clean_result.txt","w",encoding="utf-8") as f2:
            f2.write("\n".join(r_lst))
            f2.flush()

    def _device_reg_clean_test(self,ori_file,output_file):
        r_lst_1 = []
        r_lst_2= []
        r_lst_3 = []
        r_lst_4 = []
        err_lst = []
        with io.open(ori_file,"r",encoding="utf-8") as f1:
            for line_str in f1:
                line = line_str.strip()
                if line == "": continue
                lst9 = line.split("\001")
                if len(lst9) != 7: continue
                lst9 = [tmp.strip() for tmp in lst9]
                dt, sku, b_id, b_name, _, cnt, sku_name = lst9
                if b_id != self.brand_id: continue
                flag = self.device_loading_obj.fifth_generation_reg(sku_name)
                fifth_generation = ""
                if flag:
                    fifth_generation = "5G"
                sku_name_tmp = self.device_loading_obj.multi_generation_clean(sku_name)
                sku_name_tmp = self.device_loading_obj.multi_pixel_clean(sku_name_tmp)
                tmp_lst = self.model_clean_ext(sku_name_tmp, self.device_list)

                if tmp_lst == None:
                    err_lst.append(line_str)
                    continue

                if len(tmp_lst) == 1:
                    r_lst_1.append(tmp_lst)
                if len(tmp_lst) == 2:
                    r_lst_2.append(tmp_lst)
                if len(tmp_lst) == 3:
                    r_lst_3.append(tmp_lst)
                if len(tmp_lst) == 4:
                    r_lst_4.append(tmp_lst)
        print(len(r_lst_1))
        print(r_lst_1[0])
        print(r_lst_1[1])
        print("______________")
        print(len(r_lst_2))
        print(r_lst_2[0])
        print(r_lst_2[1])
        print("______________")
        print(len(r_lst_3))
        print(r_lst_3[0])
        print(r_lst_3[1])
        print("______________")
        print(len(r_lst_4))
        print(r_lst_4[0])
        print(r_lst_4[1])
                # for m in tmp_lst:
                #     tmp, _ = m
                #     for k, v in self.device_loading_obj._exchange_brand_dict.items():
                #         if k in tmp:
                #             tmp = tmp.replace(k, v)
                #             break
                #     r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % \
                #                  (dt, cnt, tmp, b_id, b_name, sku, sku_name, fifth_generation))
                #     break

        # print(len(err_lst))
        # with io.open(output_file+self.brand_name+"_clean_result.txt","w",encoding="utf-8") as f2:
        #     f2.write("\n".join(r_lst))
        #     f2.flush()


if __name__ == "__main__":
    standard_device = "./config_data/new_config_update.cfg"
    input_file_jd = "./cnt_data_1201/tmall_phone_data.txt"
    input_file_tm = "./cnt_data_1201/jd_phone_data.txt"
    output_file = "./result_data_updata_1201/"
    # err_file = "./result_data/err_result_huawei.txt"

    #清洗过程
    device_obj = DeviceRegTool(standard_device, "huawei")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file)
    # #-----------------
    device_obj = DeviceRegTool(standard_device, "xiaomi")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file)
    # # -----------------
    device_obj = DeviceRegTool(standard_device, "apple")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file)
    # # -----------------
    device_obj = DeviceRegTool(standard_device, "honour")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file)
    # # -----------------
    device_obj = DeviceRegTool(standard_device, "redmi")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file)
    # -----------------
    device_obj = DeviceRegTool(standard_device, "vivo")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file)
    # -----------------
    device_obj = DeviceRegTool(standard_device, "iqoo")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file)
    # -----------------
    device_obj = DeviceRegTool(standard_device, "oppo")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file)
    # -----------------
    device_obj = DeviceRegTool(standard_device, "realme")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file)
    # -----------------
    device_obj = DeviceRegTool(standard_device, "oneplus")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file)

    #调试测试过程
    # device_obj = DeviceRegTool(standard_device, "huawei")
    # device_obj._device_reg_clean_test(input_file,output_file)
