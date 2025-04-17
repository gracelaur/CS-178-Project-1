from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
import pymysql
import creds
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

TABLE_NAME = "Users"
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthday = request.form['birthday']
        
        print("First Name:", first_name, "Last Name:", last_name, "Birthday:", birthday)
        try:
            table.put_item(
                Item={
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Birthday': birthday
                })
            flash('User added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding user: {str(e)}', 'danger')
        return redirect(url_for('home'))
    else:
        return render_template('add_user.html')

@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        print("First Name:", first_name, "Last Name:", last_name)
        try:
            table.delete_item(
                Key={
                    'First Name': first_name,
                    'Last Name': last_name
                })
            flash('User deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting user: {str(e)}', 'danger')
        return redirect(url_for('home'))
    else:
        return render_template('delete_user.html')

@app.route('/display-users')
def display_users():
    response = table.scan()
    users = response.get('Items', [])
    return render_template('display_users.html', users=users)

@app.route('/update-user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        field_to_update = request.form['field_to_update']
        new_value = request.form['new_value']
        print("Updating user:", first_name, last_name, "Field:", field_to_update, "New value:", new_value)
        try:
            table.update_item(
                Key={
                    'First Name': first_name,
                    'Last Name': last_name
                },
                UpdateExpression=f"SET #{field_to_update} = :val",
                ExpressionAttributeNames={f"#{field_to_update}": field_to_update},
                ExpressionAttributeValues={':val': new_value}
            )
            flash('User updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating user: {str(e)}', 'danger')
        return redirect(url_for('home'))
    else:
        return render_template('update_user.html')

def get_conn():
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
        port=3306
    )
    return conn

def connect_movies_db():
    return pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
        port=3306
    )

@app.route('/names', methods=['GET', 'POST'])
def names():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        print(f"Searching for first name: {first_name}")  # Debug print

        # Query MySQL for actors with that first name (case-insensitive)
        movies_conn = connect_movies_db()
        with movies_conn.cursor() as cur:
            cur.execute("""
                SELECT person_name,
                       GROUP_CONCAT(DISTINCT title ORDER BY title ASC SEPARATOR ', ') AS movie_titles
                FROM person
                JOIN movie_cast USING(person_id)
                JOIN movie USING(movie_id)
                WHERE LOWER(person_name) LIKE LOWER(%s)
                GROUP BY person_name
            """, (f"%{first_name}%",))  # Ensure wildcards for partial match
            rows = cur.fetchall()
        movies_conn.close()

        print(f"Results: {rows}")  # Debug print for the query result

        if not rows:
            flash(f'No actors found with the first name: {first_name}.', 'warning')
        return render_template('names.html', results=rows, first_name=first_name, name_options=get_user_first_names())

    return render_template('names.html', results=None, first_name=None, name_options=get_user_first_names())

@app.route('/birthday', methods=['GET', 'POST'])
def birthday():
    if request.method == 'POST':
        birthday = request.form.get('birthday')

        movies_conn = connect_movies_db()
        with movies_conn.cursor() as cur:
            cur.execute("""
                SELECT GROUP_CONCAT(DISTINCT title ORDER BY title ASC SEPARATOR ', ') AS movie_titles
                FROM movie
                WHERE LOWER(person_name) LIKE LOWER(%s)
                GROUP BY person_name
            """, (f"%{first_name}%",))  # Ensure wildcards for partial match
            rows = cur.fetchall()
        movies_conn.close()

        print(f"Results: {rows}")  # Debug print for the query result

        if not rows:
            flash(f'No actors found with the first name: {first_name}.', 'warning')
        return render_template('names.html', results=rows, first_name=first_name, name_options=get_user_first_names())

    return render_template('names.html', results=None, first_name=None, name_options=get_user_first_names())


def get_user_first_names():
    response = table.scan(
        ProjectionExpression='#first_name',  # Use a placeholder for the attribute name
        ExpressionAttributeNames={'#first_name': 'First Name'}  # Map the placeholder to 'First Name'
    )
    names = {item['First Name'] for item in response.get('Items', []) if 'First Name' in item}
    return sorted(names)

def execute_query(query, args=()):
    cur = get_conn().cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
