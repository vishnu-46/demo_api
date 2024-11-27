#from crypt import methods
#from msilib import Table
#from crypt import methods

from flask import Flask,request
import psycopg2

app = Flask(__name__)

def connection():
    conn = psycopg2.connect(
        database ="postgres",
        user ="postgres",
        password = "2002",
        host = "localhost",
        port = "5432"
    )

    return conn
# cur.execute('''
#     CREATE TABLE Sample_data
#     (id SERIAL PRIMARY KEY,
#     name varchar(100),
#     price INT);'''
# )
#
# cur.execute('''
#     INSERT INTO Sample_data (name,price)
#     values ('Apple',50), ('Orange',40), ('grapes',20)
# ''')
#
# conn.commit()
# cur.close()
# conn.close()



@app.route('/View')
def index():

    cur = connection().cursor()
    cur.execute('''SELECT * FROM Sample_data 
    ORDER BY id''')

    data = cur.fetchall()

    cur.close()

    return {"result":data}

@app.route('/create', methods = ['POST'])
def create():
    con = connection()
    cur = con.cursor()
    data = request.json
    name = data.get('name', None)
    price = data.get('price', None)

    cur.execute('''INSERT INTO Sample_data (name,price)
    values (%s,%s)''',(name,price))
    con.commit()
    cur.close()
    con.close()
    return {
        'success':True,
        'message': "Insert record succesfully"
    }

@app.route('/update', methods=["POST"])
def update():
    con =connection()
    cur = con.cursor()
    data = request.json
    name = data.get('name', None)
    price = data.get('price', None)
    id = data.get('id', None)

    cur.execute('''
    UPDATE Sample_data SET name=%s,price = %s where id = %s ''',(name,price,id)
    )
    con.commit()
    cur.close()
    con.close()
    return {
        'succes':True,
        'message':"Table Updated"

    }

@app.route('/delete', methods=["POST"])
def delete():
    conn = connection()
    cur = conn.cursor()
    data = request.json
    name = data.get("name")
    price = data.get("price", None)
    id = data.get("id")

    cur.execute('''DELETE FROM Sample_Data WHERE id = %s''',(id,))
    conn.commit()
    cur.close()
    conn.close()
    return {
        "succes":True,
        "message":"Deleted sucessfully"
    }


if __name__ == '__main__':
    app.run(debug=True)

