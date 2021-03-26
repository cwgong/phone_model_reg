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
    def __init__(self, standard_device,brand_name):
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

    def fifth_generation_reg(self, sku_name):
        sku_name = self.multi_blank_clean(sku_name.lower())
        if len(sku_name.split("5g")) > 1:
            return True
        else:
            return False

if __name__ == "__main__":
    standard_device = "./config_data/new_config.cfg"
    device_obj = DeviceInfoLoading(standard_device,"huawei")
    device_obj._standard_device_loading()