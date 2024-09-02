from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="karyawan"
)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_karyawan_data():
    nama = request.form['nama']
    jabatan = request.form['jabatan']
    gaji = request.form['gaji']
    tanggal_masuk = request.form['tanggal_masuk']

    sql = "INSERT INTO karyawan (nama, jabatan, gaji, tanggal_masuk) VALUES (%s, %s, %s, %s)"
    val = (nama, jabatan, gaji, tanggal_masuk)

    cursor = db.cursor()
    cursor.execute(sql, val)
    db.commit()

    return redirect(url_for('show_data'))

@app.route('/data')
def show_data():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM karyawan")
    results = cursor.fetchall()
    return render_template('data.html', karyawan=results)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_data(id):
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        nama = request.form['nama']
        jabatan = request.form['jabatan']
        gaji = request.form['gaji']
        tanggal_masuk = request.form['tanggal_masuk']

        sql = "UPDATE karyawan SET nama=%s, jabatan=%s, gaji=%s, tanggal_masuk=%s WHERE id=%s"
        val = (nama, jabatan, gaji, tanggal_masuk, id)
        cursor.execute(sql, val)
        db.commit()

        return redirect(url_for('show_data'))
    
    else:
        cursor.execute("SELECT * FROM karyawan WHERE id = %s", (id,))
        karyawan = cursor.fetchone()
        return render_template('edit.html', karyawan=karyawan)

@app.route('/delete/<int:id>')
def delete_data(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM karyawan WHERE id = %s", (id,))
    db.commit()

    return redirect(url_for('show_data'))

if __name__ == '__main__':
    app.run(debug=True)
