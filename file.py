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

# Execute Query
'''
    cur.execute("""SELECT *
                FROM movie
                Limit 5""")
    output = cur.fetchall()
    
    # Print Results
    for row in output:
        print(row[0], "\t", row[1], "\t", row[2], "\t", row[3])
  
    # To close the connection
    conn.close()
'''

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
    html += """<table><tr><th>Movie ID</th><th>Title</th><th>Popularity</th></tr>"""

    for r in rows:
        html += "<tr><td>" + str(r[0]) + "</td><td>" + str(r[1]) + "</td><td>" + str(r[2]) + "</td><tr>"
    html += "</table></body>"
    return html

@app.route("/")
def viewdb():
    rows = execute_query("""SELECT movie_id, title, popularity
                FROM movie
                ORDER BY popularity desc
                Limit 10""")

    return display_html(rows)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)