import pymysql
import creds 
from flask import Flask

app = Flask(__name__)

def mysqlconnect():
    # To connect MySQL database
    conn = pymysql.connect(
        host= creds.host,
        user= creds.user, 
        password = creds.password,
        db=creds.db,
        )
    cur = conn.cursor()

def get_conn():
    conn = pymysql.connect(
        host= creds.host,
        user= creds.user,
        password= creds.password,
        db= creds.db,
        )
    return conn

def execute_query(query, args=()):
    cur = get_conn().cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def display_html(rows):
    html = ""
    html += """<table><tr><th>Release Date</th></tr>"""

    for r in rows:
        html += "<tr><td>" + str(r[0]) + "</td><tr>"
    html += "</table></body>"
    return html

@app.route("/")
def viewdb():
    rows = execute_query("""SELECT release_date
                FROM movie
                Limit 10""")

    return display_html(rows)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)