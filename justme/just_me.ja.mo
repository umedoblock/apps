Þ          Ü                 4     |   Ò      O  Ï   p  N   @  P        à     ò       !     u   8  :   ®  "   é           -     D     U     h  1   x     ª     ¾     Ù     ö  Q    -   ^       A   '  P  i  W   º	  ¥  
  )   ¸  +   â  /     -   >  Ú   l  ?   G  A     \   É     &     @  0   V  (     ;   °  1   ì  +     -   J  3   x   Another process/instance of {0} is already running.
 Detect multiple running of JustMe through sqlite3 transaction
        behavior when insert record to just_me table.
         How to inherit the JustMe class. Prohibit to run two process/instance at same time.
    To use a transaction behavior via sqlite3.
    Developver DO change lock_db_path, table_name.
    Developver DO NOT change just_me table structure.
     acquire lock instance.
        if you cannot lock, raise CannotRun().
         attr.__doc__ = gettext(attr.__doc__)
    convert and translate to use gettext(). automatic lock(). automatic unlock(). delete lock db. detect multiplu running. occured. dump db order by id desc.
        And set limit records of number.
        And you can write a where clause.
         initilize attributes and create database to lock database. make sql sentence for lock/unlock. reduce record to remains of num. release lock instance. see method name. unkown type_ "{}". vacuum lock db. you should change this method in inherited class. {0} pid={1} locked. {0} pid={1} trying lock(). {0} pid={1} trying unlock(). {0} pid={1} unlocked. Project-Id-Version: 1.1.2
POT-Creation-Date: 2013-02-12 19:26+JST
PO-Revision-Date: 2013-02-16 21:19+JST
Last-Translator: æ¢ã©ã¶ãã(umedoblock) umedoblock@gmail.com
Language-Team: Japanese umedoblock@gmail.com
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Generated-By: pygettext.py 1.5
 ä»ã® {0} ãæ¢ã«èµ·åãã¦ãã¾ãã
 record ã just_me table ã¸ insert ããæã«ã
        sqlite3 ã® transaction æ©è½ ãä½¿ããã¨ã§ãå¤éèµ·åãæ¤åºãã¾ãã
         ã©ããã£ã¦ JustMe class ãç¶æ¿ããããç¤ºãã¾ãã Python script ã®åæèµ·åãé²æ­¢ãã¾ãã
    åæèµ·åãé²æ­¢ããããã«ãsqlite3 ã® transaction ãå©ç¨ãã¦ãã¾ãã
    éçºèã®æ¹ãç¶æ¿åã§å¤æ´ããã®ã¯ãlock_db_path, table_name ã¨ãªãã¾ãã
    éçºèã®æ¹ã¯ãjust_me table æ§é ãå¤æ´ããªãããã«ãã¦ä¸ããã
 lockãè©¦ãã¾ããlockåºæ¥ãªãå ´åãCannotRun ä¾å¤ãçºçããã¾ãã attr.__doc__ ã gettext() ã«ã¦ç¿»è¨³ããã

    attr() ã¨ãã¦ attr ãå¼ã³åºãå¯è½ã§ããã°ã
    attr ã«çµã³ä»ã __doc__ å±æ§ã msgid ã¨ãã
    ä»¥ä¸ãå®è¡ããã
    msgstr = gettext(msgid)
    å®è¡å¾ãattr ã«çµã³ã¤ã __doc__ å±æ§ã®å¤ããmsgstr ã§ä¸æ¸ãããã

    attr() ã¨ãã¦ attr ãå¼ã³åºãå¯è½ã§ãªãå ´åã
    ä½ãå®è¡ããªãã
     èªåçã« lock() ãå®è¡ãã¾ãã èªåçã« unlock() ãå®è¡ãã¾ãã lock db file ãdiskä¸ããåé¤ãã¾ãã å¤éèµ·åæ¤åºæã«çºçããä¾å¤ã db ã®åå®¹ã id ã®å¤ã§æé ã«ä¸¦ã³æ¿ããè¡¨ç¤ºãã¾ãã
        è¡¨ç¤ºããä»¶æ°ãlimit=Nã¨ãã¦æå®ãããã¨ãå¯è½ã§ãã
        where å¥ãæå®ãããã¨ãå¯è½ã§ãã
         å±æ§ã®åæåã¨lockç¨databaseã®ä½æãè¡ãã¾ãã lock/unlock/prelock/ã§å¿è¦ã¨ãªãsqlåãä½æãã¾ãã db ã®æ®ãã® record æ°ã remains ä»¶ ã¨ãªãããã«ã
record ãåé¤ãã¾ãã lockãè§£é¤ãã¾ãã methodåãè¦ãã "{}" ã¯ãæ³å®ãã¦ããªã type_ ã§ãã lock db ã« vacuum ãå®è¡ãã¾ãã ç¶æ¿åã®classã§ãã®methodãå¤æ´ãã¦ä¸ããã {0} pid={1} ããlock() ã«æåãã¾ããã {0} pid={1} ããlock() ãè©¦ãã¾ãã {0} pid={1} ããunlock() ãè©¦ãã¾ãã {0} pid={1} ããunlock() ã«æåãã¾ããã 