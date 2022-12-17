---
title: "SQL injecion prevention with Python"
date: 2022-12-17T17:15:18+09:00
description: "Your Python SQL cursor execute code might be vulnerable to SQL injections! Here's how to prevent it."
tags: [python, sql]
---

Your Python SQL cursor execute code might be vulnerable to SQL injections! Here's how to prevent it.

## My experience

I had a script that used a SQL database and I recently found out that the code was vulnerable to SQL injections. I quickly fixed the script after that, though.

## The problem

I had a script that had something like this:

```python
domain = input()
harmless, malicious = search(domain)
con = pymysql.connect(
    db='db',
    user='user',
    passwd='passwd',
    host='localhost'
)
try:
    with con.cursor() as cur:
        cur.execute(f"INSERT INTO URLs (Domain, Harmless, Malicious) VALUES ('{domain}', '{harmless}', '{malicious}')")
        con.commit()
        return cur.fetchall()
finally:
    con.close()
```

As you can see, this code is vulnerable to SQL injections as it's passing the variable `domain`, `harmless`, and `malicious` into `cur.execute`. You can probably think of ways to SQL inject.

## SQL injection

From the first line, the variable domain is being user-inputted. One way to SQL inject this is writing `a',1,1);DROP TABLE URLs;` in the input stream. This will drop the table `URLs` and remove all the data from `URLs`. Even worse, you can write `a',1,1);DROP DATABASE db;` in the input stream and it will drop the database `db` and remove all the data.

## So, how do you prevent this?

You can prevent this by change the line `cur.execute(f"INSERT INTO URLs (Domain, Harmless, Malicious) VALUES ('{domain}', '{harmless}', '{malicious}')")` into `cur.execute("INSERT INTO URLs (Domain, Harmless, Malicious) VALUES (%s, %s, %s)", [domain, harmless, malicious])`. This will directly pass the arguments `domain`, `harmless`, and `malicious` into `cur.execute` so there is no possible way to SQL inject this piece of code.

## Conclusion

A lot of people don't know about SQL injections or they have a misunderstanding of it. So, you guys should be careful about it. I hope this blog will help people fix SQL injections. Thanks for reading!
