# -*- coding:utf-8 -*-
import pymysql

def connect():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='yongheng',
        db='webspyder',
        charset='utf8'
    )
    return conn

def insert_textinfo(infolist):
    conn = connect()
    cur = conn.cursor()
    sql = 'insert into news VALUES(%s,%s,%s);'
    cur.execute(sql, infolist)
    cur.close()
    conn.commit()
    conn.close()

def create_tfidf():
    conn = connect()
    cur = conn.cursor()
    string = []
    for i in range(1, 669):
        string.append('w%i double' % (i))
    sql = 'create table tfidf(' + ','.join(string) + ')'
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
    print('OK')

def insert_tfidf(wordlist):
    conn = connect()
    cur = conn.cursor()
    string = []
    for i in range(1, 669):
        string.append(str(wordlist[i-1]))
    string = ','.join(string)
    sql = 'insert into tfidf VALUES(' + string + ');'
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()

def iter_tfidf():
    conn = connect()
    cur = conn.cursor()
    sql = 'select * from tfidf;'
    cur.execute(sql)
    items = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return items









