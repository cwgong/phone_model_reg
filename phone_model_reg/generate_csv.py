import csv
import io

def generate_csv():
    csv_list = []
    with io.open("./cnt_data/biaozhu.txt","r",encoding="utf-8") as f1:
        for line in f1:
            if line == "":continue
            line_list = line.strip().split("\t")
            if len(line_list) != 2:continue
            c_list = line_list[0].split("，")
            csv_list.append(c_list)

    with io.open("./csv_data/model_triple.csv","w",encoding="utf-8",newline="") as f2:
        f_csv = csv.writer(f2)
        f_csv.writerows(csv_list)


if __name__ == "__main__":
    generate_csv()