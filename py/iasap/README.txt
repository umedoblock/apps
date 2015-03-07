# Copyright 2011-2015 梅濁酒(umedoblock)

= mini辞書
== 辞書の作成方法
windowsでは \ を ^ に置き換えます。
python3 ./iasap/pydic.py \
            --path=./iasap/eijiro98.txt.mini \
            --dbpath=./iasap/iasap.sqlite3.mini \
            --schema=./iasap/eijiro98.schema

== 辞書の確認
windowsでは飛ばします。

$ sqlite3 ./iasap/iasap.sqlite3.mini
sqlite> .schema
CREATE TABLE __namedtuples__
            (
                id integer primary key,
                typename text,
                field_names text
            );
CREATE TABLE eijiro98 (id integer primary key, head text, tail text);

sqlite> select * from __namedtuples__;
1|__namedtuples__|id typename field_names
2|eijiro98|id head tail

sqlite> select * from eijiro98;
1|#|~/backups/eijiro/eijiro98.txt
2|$__ deposit required for making a bid on|?に入札するために必要な＿ドルの保証金
3|$__-an-hour salary|《a ?》時給＿ドルの給与
4|$__-per-movie actor|映画1本の出演料が＿ドルの俳優

= 辞書
== 辞書の作成方法
$ python3 ./iasap/pydic.py \
            --path=~/backups/eijiro/eijiro98.txt \
            --dbpath=./iasap/iasap.sqlite3 \
            --schema=./iasap/eijiro98.schema
123M ./iasap/iasap.sqlite3

== 辞書の確認
windowsでは飛ばします。
$ sqlite3 ./iasap/iasap.sqlite3
sqlite> select * from __namedtuples__;
1|__namedtuples__|id typename field_names
2|eijiro98|id head tail
sqlite> select count(*) from eijiro98;
1711559
sqlite> select * from eijiro98 limit 10;
1|!|【記号】感嘆符、びっくりマーク◆【同】exclamation point◆【語源】ギリシャ語の io（イオ）＝驚く
2|"|【記号】《長さの単位》インチ(inch)
3|"Best Product of the Year" award|「年間最優秀製品」賞
4|"go slow" convoy|のろのろ運転の車列、ゆっくり運転の車列
5|"it's me" fraud|おれおれ詐欺、なりすまし詐欺◆あちこちに電話をかけて、電話に出た人の子供（または孫）のふりをして、緊急に多額の金が必要になったと告げ、指定の口座に銀行送金させるという詐欺。
6|"me too" price hikes|便乗値上げ
7|"piercing the corporate veil" doctrine|法人格否認の法理
8|#1 standard of excellence|王者、究極［至高・本物］の逸品
9|#1 | USE OF FIELD BY PERMIT ONLY|《野球場の看板》1番球場。許可を得ずに使用することを禁ずる。
10|$1 store|米国版100円ショップ

== index 作成
$ sqlite3 ./iasap/iasap.sqlite3 < ./iasap/create_index.sql
300M ./iasap/iasap.sqlite3

== iasap の動作確認
$ python3 ./iasap/iasap.py \
           --dbpath=./iasap/iasap.sqlite3
ctrl-c(コントロールキー(CTRL)とCキーの同時押し)で終了。

== debug
:!wc -l ~/backups/eijiro/eijiro98.txt
1637342 /home/umedoblock/backups/eijiro/eijiro98.txt

:!sqlite3 iasap/iasap.sqlite3
SQLite version 3.7.9 2011-11-01 00:52:41
Enter ".help" for instructions
Enter SQL statements terminated with a ";"
sqlite> select count(*) from eijiro98;
1711559
sqlite> ^\^Hct id, head from eijiro98 where id >= 1637342;

74218

>>> 1637342 + 74218
1711560

sqlite> select id,head from eijiro98 where id <= 1637342 limit 10;
1|!
2|"
3|"Best Product of the Year" award
4|"go slow" convoy
5|"it's me" fraud
6|"me too" price hikes
7|"piercing the corporate veil" doctrine
8|#1 standard of excellence
9|#1 | USE OF FIELD BY PERMIT ONLY
10|$1 store

sqlite> select id,head from eijiro98 where head = '!';
1|!
74218|!

sqlite> delete from eijiro98 where id <= 74217;
