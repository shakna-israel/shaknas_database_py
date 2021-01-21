# shakna's database.py

A modern, sensible and backwards-compatible database API for Python.

---

## A Taste

```
import sqlite3
import database

def connect():
	d = database.Database(sqlite3, "data.db")

	# Forum data...
	d.execute("""CREATE TABLE IF NOT EXISTS "comments" (
		"thread"	BLOB NOT NULL,
		"content"	BLOB NOT NULL,
		"username"	BLOB NOT NULL,
		"time"	REAL NOT NULL
	);""")

	return d

db = connect()

for row in db.execute("SELECT * from comments"):
	print(row)
	print(row[1])
	print(row.content)
	print(row['content'])

print(db.connection)
```

---

## API

`class database.Database(self, sql_engine, path, row_factory=None, *args, **kwargs)`

* `sql_engine` should be a DB-API 2.0 compatible interface, like `sqlite3`, etc. Most Python database libraries will follow this API.

* If you _don't_ supply a `row_factory`, then you'll get the magic that lets you access rows by index, string key or attribute. (e.g. `row[0] == row['thread'] == row.thread` in the above example).

	* An unknown value being accessed will raise a `KeyError`.

* If you supply a `row_factory`, then it'll be installed as per usual.

* Other arguments are passed to the `connect` function of `sql_engine`.

* When a `database.Database` goes out of scope, or is deleted, it will check if it needs to do a commit, and then self-close.

* When accessing a method or attribute, `database.Database` will check if we have an override, then check the underlying database object, and then a cursor object for that database object. It'll take the first one it finds. (e.g. `db.connection` will probably come from the `cursor` object).

---

## License

See the `LICENSE` file for the legal text.

3-Clause BSD at time of writing.
