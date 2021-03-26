#!/bin/bash

for i in `ls ./*.txt`
    do
      hive -e 'load data local inpath ./$i.txt" into table tmp.tmp_shouji_model_reg partition(dt="2020-12-02")'
    done