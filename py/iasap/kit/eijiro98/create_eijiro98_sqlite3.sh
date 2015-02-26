# Copyright 2011-2014 梅濁酒(umedoblock)

# 英次郎の一行形式のfileをdbに変換。
python3 ./pydic.py \
    --dicpath=./iasap/eijiro98.txt \
    --dbpath=./iasap/iasap.sqlite3 \
    --schema=./iasap/eijiro98.schema
# index 作成。
sqlite3 ./iasap/iasap.sqlite3 < ./iasap/create_index.sql

sqlite3 ./iasap/iasap.sqlite3 "select * from __namedtuples__"
# 1|__namedtuples__|id typename field_names
# 2|eijiro98|id head tail
sqlite3 ./iasap/iasap.sqlite3 "select count(*) from eijiro98"
# 1637342
sqlite3 ./iasap/iasap.sqlite3 "select * from eijiro98 limit 10"
