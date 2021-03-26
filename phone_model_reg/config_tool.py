#!/usr/bin/env python3
#coding=utf-8

import os
import re
import configparser
import kg_tools

class ConfigInfo(object):
    def __init__(self, listed_cmp_name, device_name):
        cmp_cfg_file_path = "config_data/cmp_" + listed_cmp_name + ".cfg"
        if not os.path.exists(cmp_cfg_file_path):
            raise Exception("%s confige file does exists!" % cmp_cfg_file_path)


        device_cfg_file_path = "config_data/" + device_name + ".cfg"
        if not os.path.exists(device_cfg_file_path):
            raise Exception("%s confige file does exists!" % device_cfg_file_path)

        cmp_cf = configparser.ConfigParser()
        cmp_cf.read(cmp_cfg_file_path)
        self.cmp_cf = cmp_cf

        device_cf = configparser.ConfigParser()
        device_cf.read(device_cfg_file_path)
        self.device_cf = device_cf
        '''
        opt1 = cf.options("device_name")
        device_name = opt1[0][1]
        short_name = opt1[1][1]
        opt2 = cf.options("huawei")
        '''

    def get_device_name(self):
        return self.device_cf["device_name"]["device_name"]

    def get_ecmp_name(self):
        return self.cmp_cf["listed_company_info"]["e_cmp_name"]

    def get_listed_cmp_name(self):
        return self.cmp_cf["listed_company_info"]["company_name"]

    def get_listed_cmp_short_name(self):
        return self.cmp_cf["listed_company_info"]["short_name"]

    def get_brand_name(self):
        return self.device_cf["brand_info"]["brand_name"]

    def get_brand_model_lst(self):
        s1 = self.device_cf["brand_info"]["brand_model"]
        s1 = kg_tools.multi_blank_clean(s1)
        lst1 = s1.strip().split(',')
        lst1 = [tmp.strip() for tmp in lst1]

        return lst1

    def get_keyword_lst(self):
        cmp_name = self.get_listed_cmp_name()
        b_name = self.get_brand_name()
        b_model_lst = self.get_brand_model_lst()

        lst2 = []
        for tmp in b_model_lst:
            lst2.append("%s|%s|%s" % (cmp_name, b_name, tmp))

        return lst2
