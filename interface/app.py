from flask import Flask, render_template, request, redirect
import mysql.connector
from config import db_config

app = Flask(__name__)


def connect_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    return conn, cursor

@app.route('/')
def index():
    return redirect('/design')

@app.route('/design', methods=['GET', 'POST'])
def add_design():
    if request.method == 'POST':
        form_type = request.form.get('form_type')

        conn, cursor = connect_db()

        if form_type == 'design':
            name_design = request.form['design_name']
            pdb_id = request.form['pdb_id']
            ref_link = request.form['ref_link']


            cursor.execute("INSERT INTO design (design_name, pdb_id, ref_link) VALUES (%s, %s, %s)",
                        (name_design, pdb_id, ref_link))
        
        elif form_type == 'categories':
            category_name = request.form['category_name']

            cursor.execute("INSERT INTO categories (category_name) VALUES (%s)", (category_name,))

        
        conn.commit()
        
        cursor.close()
        conn.close()

        return redirect('/design')


     # GET request
    conn, cursor = connect_db()

    cursor.execute("SELECT * FROM design")
    designs = cursor.fetchall()

    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('form_design.html', designs=designs, categories=categories)

if __name__ == '__main__':
    app.run(debug=True)