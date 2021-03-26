#!/usr/bin/env python3
#coding=utf-8

'''
The script is updated in 2020.09.23 by gcw.
'''

import os
import configparser
import re
import device_config

class DeviceInfoLoading(object):
    def __init__(self, standard_device,human_model_file,brand_name):
        if not os.path.exists(standard_device):
            raise Exception("%s does not exists!" % standard_device)
        try:
            self.config = configparser.ConfigParser()
            self.config.read(standard_device,encoding="utf-8")
            self.brand_name = brand_name

            self._exchange_brand_dict = {}
            # if brand_exchange_file != None:
                # if not os.path.exists(brand_exchange_file):
                #     raise Exception("%s does not exists!" % brand_exchange_file)
            self._exchange_brand_dict = device_config.ex_brand_dict

            #加载人工维护的型号配置信息
            self.human_config = configparser.ConfigParser()
            self.human_config.read(human_model_file,encoding="utf-8")


        except Exception as e:
            raise e

    def _standard_device_loading(self):
        device_list_all = []    #取到该品牌下所有的型号，格式为中文（英文）品牌+型号。
        model_str = self.config[self.brand_name]['brand_model']
        model_en_str = self.config[self.brand_name]['en_brand_name']
        model_ch_str = self.config[self.brand_name]['ch_brand_name']

        model_list = model_str.strip().split(",")
        model_list = [tmp.strip() for tmp in model_list]

        model_en_list = model_en_str.strip().split(",")
        model_en_list = [tmp.strip() for tmp in model_en_list]

        model_ch_list = model_ch_str.strip().split(",")
        model_ch_list = [tmp.strip() for tmp in model_ch_list]
        for model_name in model_list:
            if model_en_str != "":
                for model_en in model_en_list:
                    device_list_all.append(self.multi_blank_clean((model_en+model_name).lower()))
            if model_ch_str != "":
                for model_ch in model_ch_list:
                    device_list_all.append(self.multi_blank_clean((model_ch+model_name).lower()))
        return device_list_all

    def _human_model_loading(self):
        human_model_dict = {}
        model_list = self.human_config[self.brand_name]['model_info'].strip().split(",")
        element_list = self.human_config[self.brand_name]['element_info'].strip().split("+")
        if len(model_list) != len(element_list):
            return None
        for i in range(len(model_list)):
            tmp_dict = {}
            ele_info_list = element_list[i].strip().split("|")
            tmp_dict['camera_num'] = ele_info_list[0]
            tmp_dict['main_screen_resolution'] = ele_info_list[1]
            tmp_dict['main_screen_material'] = ele_info_list[2]
            tmp_dict['5g'] = ele_info_list[3]
            tmp_dict['rear_camera_max'] = ele_info_list[4]
            tmp_dict['rear_camera_info'] = ele_info_list[5]
            tmp_dict['rear_camera_num'] = ele_info_list[6]
            tmp_dict['front_facing_camera_max'] = ele_info_list[7]
            tmp_dict['front_facing_camera_info'] = ele_info_list[8]
            tmp_dict['release_time'] = ele_info_list[9]
            print(tmp_dict)
            human_model_dict[model_list[i]] = tmp_dict
        return human_model_dict


    def _get_device_id(self):
        device_id = self.config[self.brand_name]["std_brand_id"].strip()
        return device_id

    def multi_blank_clean(self, s1):
        s1 = re.sub(r"[\s]+", "", s1)
        return s1

    def multi_generation_clean(self, s1):
        s1 = re.sub("5g", "", s1.lower())
        s1 = re.sub("4g", "", s1.lower())
        return s1

    def multi_version_clean(self, s1):
        s1 = re.sub("青春版","青春",s1)
        return s1

    def multi_pixel_clean(self, s1):
        s1 = re.sub('\d+万?像素', " ", s1)
        s1 = re.sub('\d+万?超清像素', " ", s1)
        return s1

    def special_words_reg(self,word_str):
        pattern = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", word_str)
        pattern = re.sub(u"\\（.*?\\）|\\{.*?}|\\[.*?]", "", pattern)
        brand_name_item = re.sub('\W+', '', pattern).replace("_", '').lower()
        return pattern

    def fifth_generation_reg(self, sku_name):
        sku_name = self.multi_blank_clean(sku_name.lower())
        if len(sku_name.split("5g")) > 1:
            return True
        else:
            return False

if __name__ == "__main__":
    standard_device = "./config_data/new_config.cfg"
    human_model_file = "./config_data/human_model_info.cfg"
    device_obj = DeviceInfoLoading(standard_device,human_model_file,"苹果")
    # device_obj._standard_device_loading()
    human_model_dict = device_obj._human_model_loading()
    print(human_model_dict)