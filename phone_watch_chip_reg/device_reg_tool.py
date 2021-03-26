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
from struct_zgc_phone_no5g import Struct_Info
import sys
import shutil
import json

class DeviceRegTool(object):
    def __init__(self, standard_device, human_model_file, brand_name):
        '''
        荣耀和华为以及小米和红米等这些品牌对会存在混淆的情况，因此清洗华为时需要在荣耀中再进行一次清洗
        :param standard_device:
        :param brand_name:
        '''
        if not os.path.exists(standard_device):
            raise Exception("%s config file does exists!" % standard_device)
        if not os.path.exists(human_model_file):
            raise Exception("%s config file does exists!" % human_model_file)
        try:
            self.confound_sku_dict = {"华为":["荣耀"],"荣耀":["华为"],"vivo":["iQOO"],"iQOO":["vivo"],"小米":["红米"],"红米":["小米"]}
            self.confound_sku_std_dict = {"Huawei/华为":["honor/荣耀"],"honor/荣耀":["Huawei/华为"],\
                                          "vivo":["vivo"],"Xiaomi/小米":["Xiaomi/小米"]}
            self.confound_sku_id_std_dict = {"10365607": ["10561609"], "10561609": ["10365607"], \
                                          "10429338": ["10429338"], "10698337": ["10698337"]}
            self.extra_brand_name = ['realme','红米','魅族','三星','OPPO','华为','荣耀','小米','vivo']  #如果有人工添加的型号，品牌需要在该处备注
            self.brand_name = brand_name
            self.device_loading_obj = DeviceInfoLoading(standard_device,human_model_file, self.brand_name)
            self.device_list = self.device_loading_obj._standard_device_loading()
            if self.brand_name in self.extra_brand_name:
                self.human_model_dict = self.device_loading_obj._human_model_loading()
            else:
                self.human_model_dict = {}
            self.brand_id = self.device_loading_obj._get_device_id()
            self.brand_seg_dict = {"苹果":["apple","iphone","苹果"],"华为":["huawei","华为"],"红米":["红米","redmi"],\
                                   "OPPO":["oppo"],"vivo":["vivo"],"iQOO":["iqoo"],"小米":["xiaomi","小米"],\
                                   "一加":["oneplus","一加"],"荣耀":["honour","荣耀"],"realme":["realme","真我"],"三星":["三星","samsung"],\
                                   "魅族":["魅族","meizu"],"黑鲨":["黑鲨"],"纽曼":["纽曼"],\
                                    "飞利浦":["飞利浦"],"中兴":["中兴"],"诺基亚":["诺基亚"]}


            # self.brand2model_dict = {'Apple/苹果': ['iphone', 'apple', '苹果'], 'honor/荣耀': ['荣耀', 'honour'],
            #                     'Huawei/华为': ['华为', 'huawei'],
            #                     'vivo': ['vivo'], 'OnePlus/一加': ['一加', 'oneplus'], 'OPPO': ['oppo'],
            #                     'realme': ['真我', 'realme'], 'Xiaomi/小米': ['xiaomi', '小米']}
        except Exception as e:
            raise e

    def sku_clean_brand_ext(self,phone_element,json_file):
        '''
        在其它品牌下做扩展清洗，需要加载扩展品牌的型号信息以及型号对应的零件参数
        :param phone_element:
        :param json_file:
        :return:
        '''
        device_loading_obj_ext = DeviceInfoLoading(standard_device, human_model_file, self.confound_sku_dict[self.brand_name][0])
        device_list_ext = device_loading_obj_ext._standard_device_loading()
        if self.confound_sku_dict[self.brand_name][0] in self.extra_brand_name:
            human_model_dict = device_loading_obj_ext._human_model_loading()
        else:
            human_model_dict = {}
        brand_id_ext = device_loading_obj_ext._get_device_id()
        struct_zgc = Struct_Info(phone_element)
        phone_model_dict = struct_zgc.struct_zgc_info(json_file, self.confound_sku_dict[self.brand_name][0])
        return device_loading_obj_ext,device_list_ext,brand_id_ext,phone_model_dict,human_model_dict


    def get_zgc_info(self, phone_element, json_file):
        struct_zgc = Struct_Info(phone_element)
        phone_model_dict = struct_zgc.struct_zgc_info(json_file, self.brand_name)
        return phone_model_dict

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

    def brand_recognition(self,sku_name):
        brand_list = []
        brand_result = ""
        for brand_item in brand_list:
            if len(sku_name.split(brand_item)) > 1:
                brand_result = brand_item
                break
        return brand_result

    def clean_model_loading(self,brand_ext,phone_element, json_file):
        device_loading_obj_ext = DeviceInfoLoading(standard_device, human_model_file, brand_ext)
        device_list_ext = device_loading_obj_ext._standard_device_loading()
        brand_id_ext = device_loading_obj_ext._get_device_id()
        struct_zgc = Struct_Info(phone_element)
        phone_model_dict = struct_zgc.struct_zgc_info(json_file, brand_ext)


        return device_loading_obj_ext,device_list_ext,brand_id_ext,phone_model_dict


    # def _device_reg_clean(self, ori_file_jd, ori_file_tmall, output_file, phone_element, json_file):
    #     '''
    #     The function is updated in 2020.12.04 by gcw.
    #     :param ori_file:
    #     :param output_file:
    #     :return:
    #     '''
    #     r_lst = []
    #     err_lst = []
    #
    #
    #     if not os.path.exists(ori_file_jd):
    #         data_list_jd = []
    #     else:
    #         data_list_jd = struct_hive_data_jd(ori_file_jd)
    #     if not os.path.exists(ori_file_tmall):
    #         data_list_tmall = []
    #     else:
    #         data_list_tmall = struct_hive_data_tm(ori_file_tmall)
    #     data_list_all = data_list_jd + data_list_tmall
    #     device_list_ext = []
    #     phone_model_dict_ext = {}
    #     human_model_dict = {}
    #
    #     if self.brand_name in self.confound_sku_dict:
    #         device_loading_obj_ext, device_list_ext, brand_id_ext, phone_model_dict_ext, human_model_dict = self.sku_clean_brand_ext(phone_element, json_file)
    #
    #     phone_model_dict = self.get_zgc_info(phone_element, json_file)
    #     for product_info_dict in data_list_all:
    #         flag_reg = 0
    #         if len(product_info_dict) != 9: continue
    #         brand_id_std = product_info_dict['brand_id_std']
    #         brand_name_std = product_info_dict['brand_name_std']
    #         pid = product_info_dict['pid']
    #         title = product_info_dict['title']
    #         brand_name = product_info_dict['brand_name']
    #         describe = product_info_dict['describe']
    #         iphone_into = product_info_dict['iphone_into']
    #         data_source = product_info_dict['data_source']
    #         sku_name = str(title) + str(iphone_into)
    #         # dt, sku, b_id, b_name, _, cnt, sku_name = lst9
    #         if brand_id_std != self.brand_id: continue
    #         sku_name_tmp = self.device_loading_obj.multi_pixel_clean(sku_name)
    #         sku_name_tmp = self.device_loading_obj.special_words_reg(sku_name_tmp)
    #         if self.brand_name == "黑鲨":
    #             sku_name_tmp = sku_name_tmp.replace("游戏手机","")
    #         tmp_dict = self.model_clean_ext(sku_name_tmp, self.device_list)
    #
    #         #添加标志位，原生识别出来的商品和在扩展的品牌识别出来的商品做区分
    #         if tmp_dict != None:
    #             flag_reg = 1
    #
    #         if tmp_dict == None:
    #             if self.brand_name in self.confound_sku_dict:
    #                 tmp_dict = self.model_clean_ext(sku_name_tmp, device_list_ext)
    #                 if tmp_dict != None:
    #                     flag_reg = 2
    #                 else:
    #                     err_lst.append(product_info_dict)
    #                     continue
    #             else:
    #                 err_lst.append(product_info_dict)
    #                 continue
    #
    #
    #         tmp = ""
    #         span_start = 10000
    #         span_end = -1
    #         for k, v in tmp_dict.items():  # 找到商品名中最前面的品牌
    #             if v[0] < span_start:
    #                 tmp = k
    #                 span_start = v[0]
    #                 span_end = v[1]
    #             elif v[0] == span_start:  # 如果起点相同，对品牌进行最长匹配
    #                 if v[1] > span_end:
    #                     tmp = k
    #                     span_start = v[0]
    #                     span_end = v[1]
    #             else:
    #                 continue
    #
    #
    #         if flag_reg == 1:
    #             brand_list = self.brand_seg_dict[self.brand_name]       #清洗的过程中添加了品牌名称，对应到型号中时需要去掉品牌名称进行型号对应
    #             phone_model = tmp
    #             for brand_item in brand_list:
    #                 phone_model = phone_model.replace(brand_item,"")
    #
    #             if phone_model in phone_model_dict:
    #                 zgc_info_dict = phone_model_dict[phone_model]
    #
    #                 r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
    #                              (pid, brand_id_std, brand_name_std, phone_model, data_source,\
    #                               zgc_info_dict['camera_num'],zgc_info_dict['main_screen_resolution'],zgc_info_dict['main_screen_material'],zgc_info_dict['5g'],zgc_info_dict['rear_camera_max'],\
    #                               zgc_info_dict['rear_camera_info'],zgc_info_dict['rear_camera_num'],zgc_info_dict['front_facing_camera_max'],zgc_info_dict['front_facing_camera_info'],\
    #                               zgc_info_dict['release_time']))
    #
    #             elif phone_model in self.human_model_dict:
    #                 human_info_dict = self.human_model_dict[phone_model]
    #
    #                 r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
    #                              (pid, brand_id_std, brand_name_std, phone_model, data_source,\
    #                               human_info_dict['camera_num'], human_info_dict['main_screen_resolution'],
    #                               human_info_dict['main_screen_material'], human_info_dict['5g'],
    #                               human_info_dict['rear_camera_max'],\
    #                               human_info_dict['rear_camera_info'], human_info_dict['rear_camera_num'],
    #                               human_info_dict['front_facing_camera_max'], human_info_dict['front_facing_camera_info'],\
    #                               human_info_dict['release_time']))
    #
    #
    #             else:
    #                 r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
    #                              (pid, brand_id_std, brand_name_std, phone_model, data_source,\
    #                               "", "",
    #                               "", "",
    #                               "","",\
    #                               "", "",
    #                               "",""))
    #
    #         elif flag_reg == 2:
    #             brand_list = self.brand_seg_dict[self.confound_sku_dict[self.brand_name][0]]  #清洗的过程中添加了品牌名称，对应到型号中时需要去掉品牌名称进行型号对应
    #             phone_model = tmp
    #             for brand_item in brand_list:
    #                 phone_model = phone_model.replace(brand_item, "")
    #
    #             if phone_model in phone_model_dict_ext:
    #                 zgc_info_dict = phone_model_dict_ext[phone_model]
    #
    #                 r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
    #                              (pid, self.confound_sku_id_std_dict[brand_id_std][0], self.confound_sku_std_dict[brand_name_std][0],\
    #                               phone_model, data_source,\
    #                               zgc_info_dict['camera_num'], zgc_info_dict['main_screen_resolution'],
    #                               zgc_info_dict['main_screen_material'], zgc_info_dict['5g'],
    #                               zgc_info_dict['rear_camera_max'],\
    #                               zgc_info_dict['rear_camera_info'], zgc_info_dict['rear_camera_num'],zgc_info_dict['front_facing_camera_max'],
    #                               zgc_info_dict['front_facing_camera_info'],\
    #                               zgc_info_dict['release_time']))
    #
    #             elif phone_model in human_model_dict:
    #                 human_info_dict = human_model_dict[phone_model]
    #
    #                 r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
    #                              (pid, self.confound_sku_id_std_dict[brand_id_std][0], self.confound_sku_std_dict[brand_name_std][0],\
    #                               phone_model, data_source,\
    #                               human_info_dict['camera_num'], human_info_dict['main_screen_resolution'],
    #                               human_info_dict['main_screen_material'], human_info_dict['5g'],
    #                               human_info_dict['rear_camera_max'],\
    #                               human_info_dict['rear_camera_info'], human_info_dict['rear_camera_num'],
    #                               human_info_dict['front_facing_camera_max'], human_info_dict['front_facing_camera_info'],\
    #                               human_info_dict['release_time']))
    #
    #             else:
    #                 r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
    #                              (pid, brand_id_std, brand_name_std, phone_model, data_source,\
    #                               "", "",
    #                               "", "",
    #                               "","",\
    #                               "", "",
    #                               "", ""))
    #
    #     # print(len(err_lst))
    #     with io.open(output_file + "clean_result.txt", "a", encoding="utf-8") as f2:
    #         f2.write("\n".join(r_lst))
    #         f2.flush()
    #     with io.open(output_file + "error_result.txt","a",encoding="utf-8") as f3:
    #         for item_dict in err_lst:
    #             f3.write(item_dict['pid'] + "\t" + item_dict['brand_id_std'] + "\t" + item_dict['brand_name_std'] + "\t" + \
    #                      item_dict['title'] + "\t" + item_dict['data_source'] + "\n")
    #         f3.flush()
    #     with io.open(output_file + "error_save_result.txt","a",encoding="utf-8") as f4:
    #         for item_dict in err_lst:
    #             f4.write(item_dict['pid'] + "\t" + item_dict['brand_id_std'] + "\t" + item_dict['brand_name_std'] + "\t" + \
    #                      "" + "\t" + item_dict['data_source'] + ""+"\t"+""+"\t"+""+"\t"+""+"\t"+""+\
    #                      "\t"+""+"\t"+""+"\t"+""+"\t"+""+"\t"+""+"\n")
    #         f4.flush()



    def _device_reg_clean(self, ori_file_jd, ori_file_tmall, output_file, phone_element, json_file):
        '''
        The function is updated in 2020.12.04 by gcw.
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
        device_list_ext = []
        phone_model_dict_ext = {}
        human_model_dict = {}

        if self.brand_name in self.confound_sku_dict:
            device_loading_obj_ext, device_list_ext, brand_id_ext, phone_model_dict_ext, human_model_dict = self.sku_clean_brand_ext(phone_element, json_file)

        phone_model_dict = self.get_zgc_info(phone_element, json_file)
        for product_info_dict in data_list_all:
            flag_reg = 0
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
            sku_name_tmp = self.device_loading_obj.multi_pixel_clean(sku_name)
            sku_name_tmp = self.device_loading_obj.special_words_reg(sku_name_tmp)
            if self.brand_name == "黑鲨":
                sku_name_tmp = sku_name_tmp.replace("游戏手机","")
            tmp_dict = self.model_clean_ext(sku_name_tmp, self.device_list)

            #添加标志位，原生识别出来的商品和在扩展的品牌识别出来的商品做区分
            if tmp_dict != None:
                flag_reg = 1

            if tmp_dict == None:
                if self.brand_name in self.confound_sku_dict:
                    tmp_dict = self.model_clean_ext(sku_name_tmp, device_list_ext)
                    if tmp_dict != None:
                        flag_reg = 2
                    else:
                        err_lst.append(product_info_dict)
                        continue
                else:
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


            if flag_reg == 1:
                brand_list = self.brand_seg_dict[self.brand_name]       #清洗的过程中添加了品牌名称，对应到型号中时需要去掉品牌名称进行型号对应
                phone_model = tmp
                for brand_item in brand_list:
                    phone_model = phone_model.replace(brand_item,"")

                if phone_model in phone_model_dict:
                    zgc_info_dict = phone_model_dict[phone_model]

                    r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
                                 (pid, brand_id_std, brand_name_std, phone_model, data_source,\
                                  zgc_info_dict['camera_num'],zgc_info_dict['main_screen_resolution'],zgc_info_dict['main_screen_material'],zgc_info_dict['5g'],zgc_info_dict['rear_camera_max'],\
                                  zgc_info_dict['rear_camera_info'],zgc_info_dict['rear_camera_num'],zgc_info_dict['front_facing_camera_max'],zgc_info_dict['front_facing_camera_info'],\
                                  zgc_info_dict['release_time']))

                elif phone_model in self.human_model_dict:
                    human_info_dict = self.human_model_dict[phone_model]

                    r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
                                 (pid, brand_id_std, brand_name_std, phone_model, data_source,\
                                  human_info_dict['camera_num'], human_info_dict['main_screen_resolution'],
                                  human_info_dict['main_screen_material'], human_info_dict['5g'],
                                  human_info_dict['rear_camera_max'],\
                                  human_info_dict['rear_camera_info'], human_info_dict['rear_camera_num'],
                                  human_info_dict['front_facing_camera_max'], human_info_dict['front_facing_camera_info'],\
                                  human_info_dict['release_time']))


                else:
                    r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
                                 (pid, brand_id_std, brand_name_std, phone_model, data_source,\
                                  "", "",
                                  "", "",
                                  "","",\
                                  "", "",
                                  "",""))

            elif flag_reg == 2:
                brand_list = self.brand_seg_dict[self.confound_sku_dict[self.brand_name][0]]  #清洗的过程中添加了品牌名称，对应到型号中时需要去掉品牌名称进行型号对应
                phone_model = tmp
                for brand_item in brand_list:
                    phone_model = phone_model.replace(brand_item, "")

                if phone_model in phone_model_dict_ext:
                    zgc_info_dict = phone_model_dict_ext[phone_model]

                    r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
                                 (pid, self.confound_sku_id_std_dict[brand_id_std][0], self.confound_sku_std_dict[brand_name_std][0],\
                                  phone_model, data_source,\
                                  zgc_info_dict['camera_num'], zgc_info_dict['main_screen_resolution'],
                                  zgc_info_dict['main_screen_material'], zgc_info_dict['5g'],
                                  zgc_info_dict['rear_camera_max'],\
                                  zgc_info_dict['rear_camera_info'], zgc_info_dict['rear_camera_num'],zgc_info_dict['front_facing_camera_max'],
                                  zgc_info_dict['front_facing_camera_info'],\
                                  zgc_info_dict['release_time']))

                elif phone_model in human_model_dict:
                    human_info_dict = human_model_dict[phone_model]

                    r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
                                 (pid, self.confound_sku_id_std_dict[brand_id_std][0], self.confound_sku_std_dict[brand_name_std][0],\
                                  phone_model, data_source,\
                                  human_info_dict['camera_num'], human_info_dict['main_screen_resolution'],
                                  human_info_dict['main_screen_material'], human_info_dict['5g'],
                                  human_info_dict['rear_camera_max'],\
                                  human_info_dict['rear_camera_info'], human_info_dict['rear_camera_num'],
                                  human_info_dict['front_facing_camera_max'], human_info_dict['front_facing_camera_info'],\
                                  human_info_dict['release_time']))

                else:
                    r_lst.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
                                 (pid, brand_id_std, brand_name_std, phone_model, data_source,\
                                  "", "",
                                  "", "",
                                  "","",\
                                  "", "",
                                  "", ""))

        # print(len(err_lst))
        with io.open(output_file + "clean_result.txt", "a", encoding="utf-8") as f2:
            f2.write("\n".join(r_lst))
            f2.flush()
        with io.open(output_file + "error_result.txt","a",encoding="utf-8") as f3:
            for item_dict in err_lst:
                f3.write(item_dict['pid'] + "\t" + item_dict['brand_id_std'] + "\t" + item_dict['brand_name_std'] + "\t" + \
                         item_dict['title'] + "\t" + item_dict['data_source'] + "\n")
            f3.flush()
        with io.open(output_file + "error_save_result.txt","a",encoding="utf-8") as f4:
            for item_dict in err_lst:
                f4.write(item_dict['pid'] + "\t" + item_dict['brand_id_std'] + "\t" + item_dict['brand_name_std'] + "\t" + \
                         "" + "\t" + item_dict['data_source'] + ""+"\t"+""+"\t"+""+"\t"+""+"\t"+""+\
                         "\t"+""+"\t"+""+"\t"+""+"\t"+""+"\t"+""+"\n")
            f4.flush()



if __name__ == "__main__":
    #根据调度执行程序
    mon = str(sys.argv[1])
    standard_device = "./config_data/new_config_update.cfg"
    human_model_file = "./config_data/human_model_info.cfg"
    # input_file_jd = "./data/jd_phone_data_"+mon+".txt"
    # input_file_tm = "./data/tmall_phone_data_"+mon+".txt"
    input_file_jd = "./cnt_data_1201/jd_phone_data.txt"
    input_file_tm = "./cnt_data_1201/tmall_phone_data.txt"
    output_file = "./data/result_data_updata_"+mon+"/"
    phone_element = "./phone_element.cfg"
    json_file = "./zgc_data/zgc_phone_model.txt"

    if os.path.exists(output_file):
        shutil.rmtree(output_file)
        os.mkdir(output_file)
    else:
        os.mkdir(output_file)

    # #单机执行程序
    # standard_device = "./config_data/new_config_update.cfg"
    # human_model_file = "./config_data/human_model_info.cfg"
    # input_file_jd = "./cnt_data_1201/jd_phone_data.txt"
    # input_file_tm = "./cnt_data_1201/tmall_phone_data.txt"
    # output_file = "./result_data_updata_1212/"
    # phone_element = "./phone_element.cfg"
    # json_file = "./zgc_data/zgc_phone_model.txt"

    #清洗过程
    device_obj = DeviceRegTool(standard_device, human_model_file, "华为")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file, phone_element, json_file)
    # #-----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "小米")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file, phone_element, json_file)
    # # -----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "苹果")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file, phone_element, json_file)
    # # -----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "荣耀")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file, phone_element, json_file)
    # # -----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "红米")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file, phone_element, json_file)
    # # -----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "vivo")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file, phone_element, json_file)
    # #-----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "iQOO")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file, phone_element, json_file)
    # #-----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "OPPO")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file, phone_element, json_file)
    # #-----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "realme")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file, phone_element, json_file)
    # #-----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "一加")
    device_obj._device_reg_clean(input_file_jd,input_file_tm,output_file, phone_element, json_file)
    # #-----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "三星")
    device_obj._device_reg_clean(input_file_jd, input_file_tm, output_file, phone_element, json_file)
    # #-----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "魅族")
    device_obj._device_reg_clean(input_file_jd, input_file_tm, output_file, phone_element, json_file)
    # #-----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "黑鲨")
    device_obj._device_reg_clean(input_file_jd, input_file_tm, output_file, phone_element, json_file)
    # #-----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "纽曼")
    device_obj._device_reg_clean(input_file_jd, input_file_tm, output_file, phone_element, json_file)
    # #-----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "中兴")
    device_obj._device_reg_clean(input_file_jd, input_file_tm, output_file, phone_element, json_file)
    # #-----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "诺基亚")
    device_obj._device_reg_clean(input_file_jd, input_file_tm, output_file, phone_element, json_file)
    # #-----------------
    device_obj = DeviceRegTool(standard_device, human_model_file, "飞利浦")
    device_obj._device_reg_clean(input_file_jd, input_file_tm, output_file, phone_element, json_file)

    #调试测试过程
    # device_obj = DeviceRegTool(standard_device, "huawei")
    # device_obj._device_reg_clean_test(input_file,output_file)
