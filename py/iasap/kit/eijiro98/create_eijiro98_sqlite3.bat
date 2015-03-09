# Copyright 2011-2015 梅濁酒(umedoblock)

rem prompt の文字 code を UTF-8 にする。
chcp 65001

DB_PATH=./eijiro98.sqlite3

rem 英次郎の一行形式の text file を sqlite3 形式の db に変換。
python3 ./make_db.py \
        --txtpath=/home/umedoblock/backups/eijiro/eijiro98.txt ^
        --dbpath=${DB_PATH}

rem index 作成。
sqlite3 ${DB_PATH} < ./create_index_on_eijiro98.sql

sqlite3 ${DB_PATH} "select * from __namedtuples__"

rem 1|__namedtuples__|id typename field_names
rem 2|eijiro98|id key value
sqlite3 ${DB_PATH} "select count(*) from eijiro98"
rem 1637342
sqlite3 ${DB_PATH} "select * from eijiro98 limit 10"
rem prompt の文字 code を元の shift_jis に戻す。
chcp 932
