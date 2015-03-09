# Copyright 2011-2015 梅濁酒(umedoblock)

= 概要
interactive as soon as possible (a.k.a iasap)

iasap は、key-value store 形式のテキスト検索を目的として開発しました。
iasap は、incremental 検索機能を実現しています。

iasap は、key-value store の key, value の保存先として、sqlite3 を使用していま
す。
iasap は、tkinter, curses, command prompt のいずれかで、対話的に検索できます。
iasap は、検索単語に空白を入力せずに検索すると、一致検索を実行します。
iasap は、検索単語の前に空白を入力すると前方一致検索、 検索単語の後に空白を入力
すると後方一致検索、を実行します。

= ライセンス
iasap のライセンスは、「Mit License」です。
詳しくは、LICENSE.txt をご覧下さい。
LICENSE.txt の参考として、LICENSE.ja.txt もご覧下さい。

= 具体的な使い方
英語の辞書としての使用を想定しています。
開発者の私は、手元のPCで英辞郎を使用したくて、iasap の開発を始めました。
以下では、英辞郎の一行テキスト形式のファイルを、
eijiro98.txt
と仮定して、iasapの使用方法を説明します。

iasap/kit/eijiroXXX/init_eijiroXXX.py

= 実行ログ
$ cd ./kit/eijiroXXX/
$ py3.3 ./init_eijiroXXX.py --xxx=98
...

$ cd ../eijiro98

英辞郎
eijiro98.txt を
$ cp ~/backups/eijiro/eijiro98.txt .

~/repos/hg/work/py/iasap/kit/eijiro98
$ ./create_eijiro98_sqlite3.sh
zsh: 許可がありません: ./create_eijiro98_sqlite3.sh

~/repos/hg/work/py/iasap/kit/eijiro98
$ bash ./create_eijiro98_sqlite3.sh
args.txtpath = ./eijiro98.txt
args.dbpath = ./eijiro98.sqlite3
args.conf = /home/umedoblock/repos/hg/work/py/iasap/kit/eijiro98/eijiro98.conf

dbpath=./eijiro98.sqlite3
に、sqlite3 形式の db を作成しています。

real    1m33.999s
user    1m31.324s
sys     0m0.880s

sqlite3 形式の db 作成後の大きさ
-rw-r--r-- 1 umedoblock umedoblock 122M Mar  9 17:00 ./eijiro98.sqlite3
eijiro98 table 用の index 作成中

real    0m16.996s
user    0m12.365s
sys     0m1.797s

index 作成後の大きさ
-rw-r--r-- 1 umedoblock umedoblock 274M Mar  9 17:00 ./eijiro98.sqlite3

1|__namedtuples__|id typename field_names
2|eijiro98|id key value
1637342
1|!|【記号】感嘆符、びっくりマーク◆【同】exclamation point◆【語源】ギリシャ語の io（イオ）＝驚く
2|"|【記号】《長さの単位》インチ(inch)
3|"Best Product of the Year" award|「年間最優秀製品」賞
4|"go slow" convoy|のろのろ運転の車列、ゆっくり運転の車列
5|"it's me" fraud|おれおれ詐欺、なりすまし詐欺◆あちこちに電話をかけて、電話に出た人の子供（または孫）のふりをして、緊急に多額の金が必要になったと告げ、指定の口 座に銀行送金させるという詐欺。
6|"me too" price hikes|便乗値上げ
7|"piercing the corporate veil" doctrine|法人格否認の法理
8|#1 standard of excellence|王者、究極［至高・本物］の逸品
9|#1 | USE OF FIELD BY PERMIT ONLY|《野球場の看板》1番球場。許可を得ずに使用することを禁ずる。
10|$1 store|米国版100円ショップ

