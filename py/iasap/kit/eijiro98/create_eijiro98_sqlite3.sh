# Copyright 2011-2015 梅濁酒(umedoblock)

DB_PATH=./eijiro98.sqlite3

# 英辞郎の一行形式の text file を sqlite3 形式の db に変換。
/usr/bin/python3 ./make_db.py \
               --txtpath=./eijiro98.txt \
               --dbpath=${DB_PATH}

echo
echo sqlite3 形式の db 作成後の大きさ
ls -lh ${DB_PATH}

# index 作成。
echo eijiro98 table 用の index 作成中
time sqlite3 ${DB_PATH} < ./create_index_on_eijiro98.sql

echo
echo index 作成後の大きさ
ls -lh ${DB_PATH}

echo
sqlite3 ${DB_PATH} "select * from __namedtuples__"
# 1|__namedtuples__|id typename field_names
# 2|eijiro98|id key value
sqlite3 ${DB_PATH} "select count(*) from eijiro98"
# 1637342
sqlite3 ${DB_PATH} "select * from eijiro98 limit 10"
