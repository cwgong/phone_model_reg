import io
import json
import configparser
import re

class Struct_Info():
    def __init__(self,element_device):
        self.config = configparser.ConfigParser()
        self.config.read(element_device, encoding="utf-8")
        self.model_list = []
        self.brand_seg_dict = {"苹果": ["apple", "iphone", "苹果"], "华为": ["huawei", "华为"], "红米": ["红米", "redmi"], \
                               "OPPO": ["oppo"], "vivo": ["vivo"], "iQOO": ["iqoo"], "小米": ["xiaomi", "小米"], \
                               "一加": ["oneplus", "一加"], "荣耀": ["honour", "荣耀"], "realme": ["realme", "真我"],
                               "三星": ["三星", "samsung"], \
                               "魅族": ["魅族", "meizu"], "黑鲨": ["黑鲨","系列","游戏手机"],"纽曼":["纽曼","系列"],\
                               "飞利浦":["飞利浦","系列"],"中兴":["中兴"],"诺基亚":["诺基亚","系列"]}
        self.ch2arab_dict = {'单':'1','双':'2','两':'2','三':'3','四':'4','五':'5','六':'6','七':'7','八':'8','九':'9','十':'10',}


    def multi_blank_clean(self, s1):
        s1 = re.sub(r"[\s]+", "", s1)
        return s1

    def normalization_sen(self,sen):
        sen = self.multi_blank_clean(sen)
        return sen.lower()

    def special_words_reg(self,word_str):
        pattern = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", word_str)
        pattern = re.sub(u"\\（.*?\\）|\\{.*?}|\\[.*?]", "", pattern)
        brand_name_item = re.sub('\W+', '', pattern).replace("_", '').lower()
        return brand_name_item

    def split_brackets_reg(self,word_str):
        pattern = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", word_str)
        pattern = re.sub(u"\\（.*?\\）|\\{.*?}|\\[.*?]", "", pattern)
        return pattern

    def split_brand(self, model, brand_item):
        '''
        The func updated in 2020.12.08 by gcw is uesd to judge model in a brand.
        :param model:
        :param brand_item:
        :return:
        '''
        model_tmp = self.normalization_sen(model)
        brand_list = self.brand_seg_dict[brand_item]
        for brand_item in brand_list:
            model_tmp = model_tmp.replace(brand_item, "")
        model_up = model_tmp
        return self.special_words_reg(model_up)

    def get_model_from_zgc(self,brand_name):
        brand_dict = {}
        with io.open(json_file,"r",encoding="utf-8") as f1:
            for line in f1:
                if len(line) == 0:continue
                data_dict = json.loads(line.strip())
                if len(data_dict) == 0:continue
                brand_model_tmp = data_dict['系列']
                brand_name_tmp = data_dict['品牌']
                if brand_name_tmp != brand_name: continue
                brand_model = self.split_brand(brand_model_tmp,brand_name_tmp)
                brand_dict[brand_model] = ""
                # if brand_model != None:
                #     brand_dict[brand_model] = ""
        print(",".join(list(brand_dict.keys())))


    def struct_zgc_info(self,json_file,brand_name):
        '''
        brand_name需要和json文件中的“品牌”字段保持一致
        :param json_file:
        :param brand_name:
        :return:
        '''
        phone_element = self.config['element']['phone_tool']
        phone_model_dict = {}
        phone_element_list = [tmp.strip() for tmp in phone_element.strip().split(",")]
        with io.open(json_file,"r",encoding="utf-8") as f1:
            for line in f1:
                if len(line) == 0:continue
                data_dict = json.loads(line.strip())
                if len(data_dict) == 0:continue
                brand_model_tmp = data_dict['系列']
                brand_name_tmp = data_dict['品牌']
                if brand_name_tmp != brand_name:continue
                brand_model = self.split_brand(brand_model_tmp,brand_name_tmp)
                if brand_model in phone_model_dict:continue         #该手机型号已经处理过，再次遇到重复的直接跳过
                tmp_dict = {}
                for phone_element_item in phone_element_list:
                    if phone_element_item in data_dict:
                        tmp_dict[phone_element_item] = data_dict[phone_element_item]
                    else:
                        tmp_dict[phone_element_item] = ""
                # if brand_name == "苹果":
                #     # print(brand_model)
                #     print(tmp_dict['后置摄像头'])
                result_dict = self.special_ele_reg(tmp_dict)
                if result_dict['camera_num'] != "":
                    phone_model_dict[brand_model] = result_dict
        return phone_model_dict

    def choose_max_camera(self,camera_str):
        int_list = []
        camera_str_list = camera_str.split(",")
        if len(camera_str_list) < 2:return camera_str
        for camera_str in camera_str_list:
            int_list.append(int(camera_str))
        camera_max = max(int_list)
        return str(camera_max)

    def special_ele_reg(self,tmp_dict):
        model_element_dict = {}
        rear_camera_num = 0
        front_camera_num = 0
        if '摄像头总数' in tmp_dict:
            model_ele_result = self.special_words_reg(tmp_dict['摄像头总数']).replace("摄像头","")
            if model_ele_result in self.ch2arab_dict:
                model_element_dict['camera_num'] = self.ch2arab_dict[model_ele_result]
            else:
                model_element_dict['camera_num'] = ""
        else:
            model_element_dict['camera_num'] = ""

        if '主屏材质' in tmp_dict:
            model_ele_result = tmp_dict['主屏材质']
            model_ele_result = self.split_brackets_reg(model_ele_result).replace("材质","")
            model_element_dict['main_screen_material'] = model_ele_result
        else:
            model_element_dict['main_screen_material'] = ""

        if '主屏分辨率' in tmp_dict:
            model_ele_result = self.special_words_reg(tmp_dict['主屏分辨率']).replace("像素", "")
            model_element_dict['main_screen_resolution'] = model_ele_result
        else:
            model_element_dict['main_screen_resolution'] = ""

        if '5G网络' in tmp_dict:
            if tmp_dict['5G网络'] == "":
                model_element_dict['5g'] = 0
            else:
                model_element_dict['5g'] = 1
        else:
            model_element_dict['5g'] = 0

        if '前置摄像头' in tmp_dict:
            model_ele_result = tmp_dict['前置摄像头']
            model_ele_list = model_ele_result.strip().split("+")
            front_camera_num = len(model_ele_list)
            num_list_all = []
            for model_ele in model_ele_list:
                if "万像素" in model_ele or "万广角" in model_ele or "万超广角" in model_ele or "万长焦" in model_ele:
                    num_list = re.findall('\d+', self.special_words_reg(model_ele))
                    if len(num_list) > 0:
                        num_list_all.append(num_list[0])
                    else:
                        continue
                else:
                    continue

            if len(num_list_all) > 0:
                model_element_dict['front_facing_camera_info'] = ",".join(num_list_all)
                model_element_dict['front_facing_camera_max'] = self.choose_max_camera(",".join(num_list_all))
            else:
                model_element_dict['front_facing_camera_info'] = ""
                model_element_dict['front_facing_camera_max'] = ""
        else:
            model_element_dict['front_facing_camera_info'] = ""
            model_element_dict['front_facing_camera_max'] = ""

        if '后置摄像头' in tmp_dict:
            model_ele_result = tmp_dict['后置摄像头']
            model_ele_list = model_ele_result.strip().split("+")
            rear_camera_num = len(model_ele_list)
            num_list_all = []
            for model_ele in model_ele_list:
                if "万像素" in model_ele or "万广角" in model_ele or "万超广角" in model_ele or "万长焦" in model_ele:
                    num_list = re.findall('\d+', self.special_words_reg(model_ele))
                    if len(num_list) > 0:
                        num_list_all.append(num_list[0])
                    else:
                        continue
                else:
                    continue
            if len(num_list_all) > 0:
                model_element_dict['rear_camera_info'] = ",".join(num_list_all)
                model_element_dict['rear_camera_max'] = self.choose_max_camera(",".join(num_list_all))
            else:
                model_element_dict['rear_camera_info'] = ""
                model_element_dict['rear_camera_max'] = ""
        else:
            model_element_dict['rear_camera_info'] = ""
            model_element_dict['rear_camera_max'] = ""

        if "上市日期" in tmp_dict:
            model_ele_result = tmp_dict['上市日期']
            year = model_ele_result[0:4]
            if len(model_ele_result) >= 8:
                month = model_ele_result[5:7]
                if '月' not in month:
                    release_time = year + "-" + month
                else:
                    month = '0' + model_ele_result[5]
                    release_time = year + "-" + month
            else:
                release_time = year
            model_element_dict['release_time'] = release_time
        else:
            model_element_dict['release_time'] = ""

        if model_element_dict['camera_num'] == "":
            camera_num = front_camera_num + rear_camera_num
            if camera_num != 0:
                model_element_dict['camera_num'] = str(camera_num)

        if '后置摄像头' in tmp_dict:
            model_element_dict['rear_camera_num'] = rear_camera_num
        else:
            model_element_dict['rear_camera_num'] = ""

        return model_element_dict


if __name__ == "__main__":

    #清洗过程
    phone_element = "./phone_element.cfg"
    json_file = "./zgc_data/zgc_phone_model.txt"
    #
    struct_zgc = Struct_Info(phone_element)
    phone_model_dict = struct_zgc.struct_zgc_info(json_file,"诺基亚")
    for k,v in phone_model_dict.items():
        print(k)
        print(v)
        print("--------------------")

    #小测试
    # s = "2017年03月03日"
    # ss = "2017年03月"
    # print(ss[2:5])

    #生成标准型号过程
    # phone_element = "./phone_element.cfg"
    # json_file = "./zgc_data/zgc_phone_model.txt"
    # # #
    # struct_zgc = Struct_Info(phone_element)
    # struct_zgc.get_model_from_zgc("华为")
    # struct_zgc.get_model_from_zgc("荣耀")
    # struct_zgc.get_model_from_zgc("苹果")
    # struct_zgc.get_model_from_zgc("vivo")
    # struct_zgc.get_model_from_zgc("OPPO")
    # struct_zgc.get_model_from_zgc("一加")
    # struct_zgc.get_model_from_zgc("realme")
    # struct_zgc.get_model_from_zgc("小米")
    # struct_zgc.get_model_from_zgc("红米")
    # struct_zgc.get_model_from_zgc("iQOO")
    # struct_zgc.get_model_from_zgc("三星")
    # struct_zgc.get_model_from_zgc("魅族")
    # struct_zgc.get_model_from_zgc("黑鲨")
    # struct_zgc.get_model_from_zgc("诺基亚")
    # struct_zgc.get_model_from_zgc("纽曼")
    # struct_zgc.get_model_from_zgc("飞利浦")
    # struct_zgc.get_model_from_zgc("中兴")

