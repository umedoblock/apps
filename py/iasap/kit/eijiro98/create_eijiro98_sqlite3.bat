# Copyright 2011-2014 梅濁酒(umedoblock)

rem prompt の文字 code を UTF-8 にする。
chcp 65001
rem 英次郎の一行形式のfileをdbに変換。
python ./pydic.py ¥
    --path=./iasap/eijiro98.txt ^
    --dbpath=./iasap/iasap.sqlite3 ^
    --schema=./iasap/eijiro98.schema
rem index 作成。
sqlite3 ./iasap/iasap.sqlite3 < ./iasap/create_index.sql

sqlite3 ./iasap/iasap.sqlite3 "select * from __namedtuples__"
rem 1|__namedtuples__|id typename field_names
rem 2|eijiro98|id head tail
sqlite3 ./iasap/iasap.sqlite3 "select count(*) from eijiro98"
rem 1637342
sqlite3 ./iasap/iasap.sqlite3 "select * from eijiro98 limit 10"
rem prompt の文字 code を元の shift_jis に戻す。
chcp 932
