# iasap の setup.py

from distutils.core import setup

setup(
    name = "iasap",
    packages = ["iasap"],
    version = "0.0.0",
    description = "interactive as sonn as possible",
    author = "梅濁酒(umedoblock)",
    author_email = "umedoblock@gmail.com",
    url='http://pypi.python.org/pypi/iasap/',
    download_url = "",
    license='BSD License',
    platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
    # see
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Japanese',
        'Operating System :: OS Independent',
        'Topic :: Education',
    ],
    long_description = """\
interactive as soon as possible (a.k.a asap)
-------------------------------------
迅速な回答を心がける、対話型辞書です。
key-value store というと、分かりやすいでしょうか。
incremental 検索機能付き辞書です。

key は、英数字を想定しています。
value は、日本語(=utf-8で非ascii文字)を想定しています。

想定している具体的な使い方は、英語の辞書です。
key に 英単語を、
value に 日本語訳を、
入力するという想定で開発しました。

開発者の私は、手元のPCで使える英語の辞書が欲しくて、
iasap を自作することになりました。
英辞郎をPCで辞書として使う方法について詳しくは、
同梱の README をご覧下さい。

このバージョンの iasap は、Python3.x で使用してください。
"""
)
