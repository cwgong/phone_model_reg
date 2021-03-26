#!/bin/bash

hive -e "select t.brand_id_std,t.brand_name_std,t.pid,t.title,t.brand_name,t.descibe,t.descibe_more from dwd.dwd_retailers_online_shouji t where t.dt = '$1' and t.platform_type = 'tmall'" > ./cnt_data_1201/tmall_phone_data.txt

hive -e "select t.brand_id_std,t.brand_name_std,t.pid,t.title,t.brand_name,t.descibe,t.descibe_more from dwd.dwd_retailers_online_shouji t where t.dt = '$1' and t.platform_type = 'jd'" > ./cnt_data_1201/jd_phone_data.txt

if [ $? -ne 0 ]; then
    echo "load data error!"
    exit 1
fi

python device_reg_tool.py "$1"

if [ $? -ne 0 ]; then
    echo "device_reg_tool error!"
    exit 1
fi

hive -e "load data local inpath './data/result_data_updata_$1/clean_result.txt' overwrite into table dwd.dwd_phone_sku2model_info partition(dt = '$1')"
hive -e "load data local inpath './data/result_data_updata_$1/error_save_result.txt' into table dwd.dwd_phone_sku2model_info partition(dt = '$1')"

exit 0
