import re
import json

def test_research(test_str,st_brand):
    st_brand_rgx = re.compile(st_brand)
    rgx_result_list = st_brand_rgx.search(test_str)
    print(rgx_result_list)

def struct_hive_data(input_file):
    data_list = []
    with open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 5:continue
            pid,title,brand_name,describe,describe_more = line_list
            if describe == "NULL":
                describe_dict = {}
            else:
                describe_dict = json.loads(describe)
            if '型号' not in describe_dict:
                iphone_into = "无"
            else:
                iphone_into = describe_dict['型号']
            tmp_dict = {"pid":pid,"title":title,"brand_name":brand_name,"describe":describe,"describe_more":describe_more,"iphone_into":iphone_into}
            data_list.append(tmp_dict)
    return data_list

def struct_hive_data_jd(input_file):
    data_list = []
    with open(input_file, "r", encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0: continue
            line_list = line.strip().split("\t")
            if len(line_list) != 5: continue
            tmp_dict = {}
            pid, title, brand_name, describe, describe_more = line_list
            if describe == "NULL":
                describe_list = []
            else:
                describe_list = describe.strip().split("；")
            if len(describe_list) >= 1:
                if '商品名称：' not in describe_list[0]:
                    iphone_into = '无'
                else:
                    iphone_str = describe_list[0]
                    iphone_into = iphone_str.replace("商品名称：","")
            else:
                iphone_into = "无"
            tmp_dict = {"pid": pid, "title": title, "brand_name": brand_name, "describe": describe,
                        "describe_more": describe_more, "iphone_into": iphone_into}
            data_list.append(tmp_dict)
    return data_list


if __name__ == "__main__":
    # test_str = "今天我买了一台vivo3x手机，这是我的第一台vivo3x"
    # st_brand = "vivo3x"
    # test_research(test_str,st_brand)
    # 天猫结构化数据测试
    # input_file = "./tmall_phone_data.txt"
    # data_list = struct_hive_data(input_file)
    # print(len(data_list))
    # print(data_list[0])
    # print(data_list[1])

    #jd结构化数据测试
    input_file = "./jd_phone_data.txt"
    data_list = struct_hive_data_jd(input_file)
    print(len(data_list))
    print(data_list[0])
    print(data_list[1])

