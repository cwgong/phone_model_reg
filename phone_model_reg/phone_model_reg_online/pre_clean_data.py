import json


def struct_hive_data_tm(input_file):
    data_list = []
    with open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 7:continue
            brand_id_std,brand_name_std,pid,title,brand_name,describe,describe_more = line_list
            if describe == "NULL":
                describe_dict = {}
            else:
                describe_dict = json.loads(describe)
            if '型号' not in describe_dict:
                iphone_into = "无"
            else:
                iphone_into = describe_dict['型号']
            tmp_dict = {"brand_id_std":brand_id_std,"brand_name_std":brand_name_std,"pid":pid,"title":title,"brand_name":brand_name,"describe":describe,"describe_more":describe_more,"iphone_into":iphone_into,"data_source":"tmall"}
            data_list.append(tmp_dict)
    return data_list

def struct_hive_data_jd(input_file):
    data_list = []
    with open(input_file, "r", encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0: continue
            line_list = line.strip().split("\t")
            if len(line_list) != 7: continue
            brand_id_std,brand_name_std,pid, title, brand_name, describe, describe_more = line_list
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
            tmp_dict = {"brand_id_std":brand_id_std,"brand_name_std":brand_name_std,"pid": pid, "title": title, "brand_name": brand_name, "describe": describe,
                        "describe_more": describe_more, "iphone_into": iphone_into,"data_source":"jd"}
            data_list.append(tmp_dict)
    return data_list

if __name__ == "__main__":
    # 天猫结构化数据测试
    # input_file = "./tmall_phone_data.txt"
    # data_list = struct_hive_data_tm(input_file)
    # print(len(data_list))
    # print(data_list[0])
    # print(data_list[1])

    # jd结构化数据测试
    input_file = "./jd_phone_data.txt"
    data_list = struct_hive_data_jd(input_file)
    print(len(data_list))
    print(data_list[0])
    print(data_list[1])