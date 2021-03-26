import io
import random

'''
The script is updated in 2020.09.23 by gcw.
'''

def stat_fifth_generation(input_file,output_fifth_generation):
    dt_dict = {}
    dt_list = []
    five_g_list = []
    with io.open(input_file, "r", encoding="utf-8") as f1:
        for line in f1:
            lst1 = line.strip().split("\t")
            if len(lst1) != 8: continue
            dt, cnt, model_no, b_id, b_name, sku, sku_name, fifth_generation = lst1
            if fifth_generation != "5G":continue
            # if dt == "2019_m02":five_g_list.append(line)
            if dt in dt_dict:
                dt_dict[dt] = dt_dict[dt] + int(float(cnt))
            else:
                dt_dict[dt] = int(float(cnt))
    # for five_g in five_g_list:
    #     print(five_g)
    if dt_dict != {}:
        dt_list = [(k,v) for k,v in dt_dict.items()]
    with io.open(output_fifth_generation,"w",encoding="utf-8") as f2:
        for dt in dt_list:
            f2.write(str(dt[0]) + "\t" + str(dt[1]) + "\n")
        f2.flush()

def stat_device_model(input_file,output_model_name,model_name):
    dt_dict = {}
    dt_list = []
    five_g_list = []
    with io.open(input_file, "r", encoding="utf-8") as f1:
        for line in f1:
            # lst1 = line.strip().split("\t")
            lst1 = line.split("\t")
            dt, cnt, model_no, b_id, b_name, sku, sku_name, fifth_generation, _ = lst1
            if model_no.replace("huawei","").replace("华为","") != model_name:continue
            # if dt == "2019_m02":five_g_list.append(line)
            if dt in dt_dict:
                dt_dict[dt] = dt_dict[dt] + int(float(cnt))
            else:
                dt_dict[dt] = int(float(cnt))
    # for five_g in five_g_list:
    #     print(five_g)
    if dt_dict != {}:
        dt_list = [(k,v) for k,v in dt_dict.items()]
    with io.open(output_model_name,"w",encoding="utf-8") as f2:
        for dt in dt_list:
            f2.write(str(dt[0]) + "\t" + str(dt[1]) + "\n")
        f2.flush()


def stat_device_model_all(input_file, output_model_name, model_name):
    five_g_list = []
    model_list = model_name.strip().split(",")
    model_list = [tmp.strip() for tmp in model_list]

    for model_item in model_list:
        dt_dict = {}
        dt_list = []
        with io.open(input_file, "r", encoding="utf-8") as f1:
            for line in f1:
                # lst1 = line.strip().split("\t")
                lst1 = line.split("\t")
                dt, cnt, model_no, b_id, b_name, sku, sku_name, fifth_generation, _ = lst1
                if model_no.replace("oppo", "") != model_item.lower(): continue
                # if dt == "2019_m02":five_g_list.append(line)
                if dt in dt_dict:
                    dt_dict[dt] = dt_dict[dt] + int(float(cnt))
                else:
                    dt_dict[dt] = int(float(cnt))
        # for five_g in five_g_list:
        #     print(five_g)
        if dt_dict != {}:
            dt_list = [(k, v) for k, v in dt_dict.items()]
        with io.open(output_model_name+model_item+".txt", "w", encoding="utf-8") as f2:
            for dt in dt_list:
                f2.write(str(dt[0]) + "\t" + str(dt[1]) + "\n")
            f2.flush()

def random_choice_data(input_file,output_file):
    device_model_list = []
    with io.open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            lst1 = line.strip().split("\t")
            device_model_list.append(line)
    print(len(device_model_list))
    sample_list = random.sample(device_model_list, 40)
    with io.open(output_file,"a",encoding="utf-8") as f2:
        f2.write("".join(sample_list))
        f2.flush()

def stat_all_model(model_list,input_file,output_file):
    model_dict = {}
    model_list_all = []
    for model_item in model_list:
        with io.open(input_file+model_item+".txt","r",encoding="utf-8") as f1:
            for line in f1:
                if line == "":continue
                line_list = line.strip().split('\t')
                if line_list[0] not in model_dict:
                    model_dict[line_list[0]] = int(line_list[1])
                else:
                    model_dict[line_list[0]] = model_dict[line_list[0]] + int(line_list[1])
    if model_dict != {}:
        model_list_all = [(k,v) for k,v in model_dict.items()]
    with io.open(output_file,"w",encoding="utf-8") as f2:
        for item in model_list_all:
            f2.write(item[0] + "\t" + str(item[1]) + "\n")


def stat_all_brand(brand_list,input_file,out_put_file):
    brand_dict = {}
    brand_list_all = []
    for model_item in brand_list:
        with io.open(input_file + model_item + "_relation.txt", "r", encoding="utf-8") as f1:
            for line in f1:
                if line == "": continue
                line_list = line.strip().split('\t')
                if line_list[0] not in brand_dict:
                    brand_dict[line_list[0]] = int(line_list[1])
                else:
                    brand_dict[line_list[0]] = brand_dict[line_list[0]] + int(line_list[1])
    if brand_dict != {}:
        brand_list_all = [(k, v) for k, v in brand_dict.items()]
    with io.open(out_put_file, "w", encoding="utf-8") as f2:
        for item in brand_list_all:
            f2.write(item[0] + "\t" + str(item[1]) + "\n")

def find_month_model(input_file, model, month):
    with io.open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if line == "":continue
            line_list = line.split("\t")
            dt, cnt, model_no, b_id, b_name, sku, sku_name, fifth_generation, _ = line_list
            if dt == month and model_no == model:
                print(line)
            else:
                continue

def stat_device_sale_all(input_file, output_model_name, model_name):
    model_list = model_name.strip().split(",")
    model_list = [tmp.strip() for tmp in model_list]
    dt_dict = {}
    dt_list = []
    for model_item in model_list:
        sale_str = 0
        with io.open(input_file, "r", encoding="utf-8") as f1:
            for line in f1:
                # lst1 = line.strip().split("\t")
                lst1 = line.split("\t")
                dt, cnt, model_no, b_id, b_name, sku, sku_name, fifth_generation, _ = lst1
                if model_no.replace("realme", "").replace("真我", "") != model_item.lower(): continue
                sale_str = sale_str + int(float(cnt))
        dt_dict[model_item] = sale_str
    if dt_dict != {}:
        dt_list = [(k, v) for k, v in dt_dict.items()]
    dt_list = sorted(dt_list,key = lambda x: x[1],reverse=True)
    for item in dt_list:
        print(str(item))
    print(len(dt_list))
        # with io.open(output_model_name + model_item + ".txt", "w", encoding="utf-8") as f2:
        #     for dt in dt_list:
        #         f2.write(str(dt[0]) + "\t" + str(dt[1]) + "\n")
        #     f2.flush()


if __name__ == "__main__":
    # 统计5G
    # input_fifth_generation = "./result_data_update/huawei_clean_result.txt"
    # output_fifth_generation = "./stat_result_update/fifth_generation_stat_huawei.txt"
    # stat_fifth_generation(input_fifth_generation,output_fifth_generation)

    # # 统计型号变化
    # input_file = "./result_data_update/huawei_clean_result.txt"
    # output_model_name = "./stat_result_update/p40_stat.txt"
    # model_name = "p40"
    # stat_device_model(input_file,output_model_name,model_name)

    # 统计某一品牌下所有型号的变化
    # input_file = "./result_data_update_2/oppo_clean_result.txt"
    # output_model_name = "./model_month_2/oppo_stat"
    # honour_model_name = "畅玩5A,畅玩5C,畅玩5X,畅玩5,畅玩6A,畅玩6X国际版,畅玩6X,畅玩6,畅玩7A,畅玩7C,畅玩7,畅玩9A,畅玩9,Magic2,Note10,Play3e,Play3,Play4Pro,Play4TPro,Play4T,Play4,V8Max,V8,V9Play,V9,V10,V20,V30PRO,V30,X10Max,X10,10青春版,10,20Pro,20S,20i,20青春版,20,30Pro+,30Pro,30S,30青春版,30,8XMax,8X,8青春版,8,9XPro,9X,9青春版,9,畅玩7X"
    # oppo_model_name = "A5,A7X,A7,A8,A9,A11,A92s,Ace2,FindX2,FindX,K1,K3,K5,Reno3Pro,Reno3,Reno4Pro,Reno4,Reno10,RenoAce,RenoZ,R3,R7,R9,R819,reno3元气版,FindX2Pro,A72,K7,a9x,renoace2,a11x"
    # stat_device_model_all(input_file, output_model_name, oppo_model_name)

    #随机采样人工审核
    # input_file = "./result_data_update/vivo_clean_result.txt"
    # output_model_name = "./stat_result/random_data.txt"
    # random_choice_data(input_file, output_model_name)

    # 统计某一公司的手机销量变化
    # 汇顶科技
    # huawei_model_list = ["P40","P40Pro","nova7","nova7SE","nova7Pro"]
    # vivo_model_list = ["X50Pro+", "X50Pro", "X50"]
    # iqoo_model_list = ["Neo3", "3"]
    # realme_model_list = ["X50Pro", "X50"]
    # xiaomi_model_list = ["10至尊纪念版", "10Pro", "10"]
    # redmi_model_list = ["10X", "K30至尊纪念版"]
    # oneplus_model_list = ["8Pro", "8"]
    # oppo_model_list = ["FindX2", "FindX2Pro", "Reno4", "Reno4Pro"]
    # honour_model_list = ["30"]
    # #歌尔公司
    # huawei_model_list_geer = ["P40","P40Pro"]
    # xiaomi_model_list_geer = ["10"]
    # redmi_model_list_geer = ["k30pro"]
    #欧菲光
    # huawei_model_list_ou = ["P40", "P40Pro"]
    # xiaomi_model_list_ou = ["10","10Pro","10青春","10至尊纪念版"]
    # redmi_model_list_ou = ["9","9A","10X","10XPro"]
    # oppo_model_list_ou = ["FindX2", "FindX2Pro"]
    # input_file = "./model_month_2/honour_stat"
    # output_model_name = "./relation_model_2/honour_relation.txt"
    # stat_all_model(honour_model_list, input_file, output_model_name)

    # 统计所有品牌的销量
    brand_list = ["huawei", "iqoo", "oneplus", "oppo", "realme", "redmi", "vivo","xiaomi","honour"]
    # brand_list = ["huawei", "redmi", "xiaomi"]
    # brand_list = ["huawei", "redmi", "xiaomi","oppo"]
    input_file = "./relation_model_2/"
    output_model_name = "./brand_relation_2/result_relation_update.txt"
    stat_all_brand(brand_list, input_file, output_model_name)

    #查找某一型号手机某一月份的数据
    # input_file = "./result_data_update_2/oppo_clean_result.txt"
    # brand_model = "opporeno4"
    # month = "2019_m07"
    # find_month_model(input_file,brand_model,month)

    #统计某一品牌下所有型号的销量情况
    # input_file = "./result_data_update_2/realme_clean_result.txt"
    # output_model_name = "./model_month_2/realme_stat"
    # honour_model_name = "畅玩5A,畅玩5C,畅玩5X,畅玩5,畅玩6A,畅玩6X国际版,畅玩6X,畅玩6,畅玩7A,畅玩7C,畅玩7,畅玩9A,畅玩9,Magic2,Note10,Play3e,Play3,Play4Pro,Play4TPro,Play4T,Play4,V8Max,V8,V9Play,V9,V10,V20,V30PRO,V30,X10Max,X10,10青春版,10,20Pro,20S,20i,20青春版,20,30Pro+,30Pro,30S,30青春版,30,8XMax,8X,8青春版,8,9XPro,9X,9青春版,9,畅玩7X"
    # oppo_model_name = "A5,A7X,A7,A8,A9,A11,A92s,Ace2,FindX2,FindX,K1,K3,K5,Reno3Pro,Reno3,Reno4Pro,Reno4,Reno10,RenoAce,RenoZ,R3,R7,R9,R819,reno3元气版,FindX2Pro,A72,K7,a9x,renoace2,a11x"
    # vivo_model_name = "G1,NEX3S,NEX3,NEX,S1Pro,S1,S5,S6,U1,U3x,U3,X5,X6Plus,X6,X21i,X21,X23幻彩,X23,X27,X30Pro,X30,X50Pro+,X50Pro,X50,Y70,Y71,Y75,Y79,Y93,Y97,Z1i,Z1青春版,Z1,Z3X,Z3,Z5x,Z5,Z6,Y3,X30Proaw联名限定版,Y5,y70S,y51s,S7,Y93s"
    # iqoo_model_name = "Z1x,Z1,U1,Neo3,3,Z6,5Pro,5"
    # oneplus_model_name = "6T,6,7Pro,7TPro,7T,7,8Pro,8"
    # huawei_model_name = "畅享7Plus,畅享7S,畅享7,畅享8,畅享9Plus,畅享9S,畅享9,畅享10Plus,畅享10S,畅享10e,畅享10,畅享20Pro,畅享20,畅享Z,G7Plus,G9青春版,Mate10,Mate20Pro,Mate20X,Mate20,Mate20RS,Mate30Pro,Mate30RS,Mate30,MateRS,MateXs,MateX,nova2Plus,nova2s,nova2,nova3i,nova3,nova4e,nova4,nova5Pro,nova5Z,nova5iPro,nova5i,nova5,nova6,nova7Pro,nova7SE,nova7,nova青春版,P10Plus,P10,P20Pro,P20,P30Pro,P30,P40Pro+,P40Pro,P40"
    # xiaomi_model_name = "CC9Pro,CC9e,CC9,MIX2s,MIX2,MIX3,MIX,Max3,10Pro,10青春版,10,2A,9Pro,9透明,9,6Pro,6A,6X,6,7A,7,8SE,8青春版,8,黑鲨游戏手机3,黑鲨游戏手机3PRO,10至尊纪念版,9se"
    # redmi_model_name = "7,K30Pro,K305G,K30i,K30,K20Pro,K20,9,10X5G,10XPro,10X,Note7,Note8Pro,Note8,8A,8,9A,K30至尊纪念版"
    # realme_model_name = "X50Pro,X50m,X50t,X50,Q,X2Pro,X2,X青春版,X50Pro玩家版,V5,X7Pro"
    # stat_device_sale_all(input_file, output_model_name, realme_model_name)