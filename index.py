from flask import Flask, render_template,request,session, flash,redirect,url_for
from functools import wraps
from flask_mysqldb import MySQL
from datetime import datetime
import hashlib

#Configuración de flask para MySQL
app = Flask(__name__)
app.secret_key = 't1burones'
app.config['MYSQL_HOST'] = 'sql7.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql7833363'
app.config['MYSQL_PASSWORD'] = 'ClWLMIf2m8'
app.config['MYSQL_DB'] = 'sql7833363'
mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica si el usuario no tiene la sesión activa
        if 'loggedin' not in session:
            flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return(render_template('home.html'))

@app.route('/cerrar-sesion')
def fnSalir():
    # Elimina los datos de la sesión
    ID = session['id']
    token = session['token']
    cursor  = mysql.connection.cursor()
    cursor.execute('UPDATE token SET lActivo=0 WHERE idUsuario=%s AND cToken=%s',(ID,token))
    mysql.connection.commit()
    cursor.close()
    ActualizaToken("salida")
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('user', None)
    session.pop('token', None)
    # Redirige al login
    return redirect(url_for('login'))

def ActualizaToken(tipo):
    ID = session['id']
    token = session['token']
    fecha = datetime.now()
    cursor  = mysql.connection.cursor()
    if tipo == "salida":
        cursor.execute('UPDATE token SET dFechaSalida=%s WHERE idUsuario=%s AND cToken=%s',(fecha,ID,token))
    else:
        cursor.execute('UPDATE token SET dFecha=%s WHERE idUsuario=%s AND cToken=%s',(fecha,ID,token))
    mysql.connection.commit()
    cursor.close()

@app.route('/productos')
def productos():
    ActualizaToken("normal")
    return(render_template('productos.html'))

@app.route('/valida-usuario',methods=['POST'] )
def ValidaUsuario():
    usuario = request.form.get('usuario')
    clave   = request.form.get('clave')
    usuariomd5 = hashlib.md5(usuario.encode('utf-8')).hexdigest()
    clavemd5 = hashlib.md5(clave.encode('utf-8')).hexdigest()
    cursor  = mysql.connection.cursor()
    cursor.execute('SELECT idUsuario,cUsuario FROM usuario WHERE cUsuario = %s AND cClave = %s', (usuariomd5,clavemd5))
    account = cursor.fetchone()
    if account:
        fecha = datetime.now()
        token = hashlib.md5(fecha.isoformat().encode('utf-8')).hexdigest()
        session['loggedin'] = True
        session['id'] = account[0]
        session['user'] = account[1]
        session['token'] = token   

        cursor.execute('INSERT INTO token(idUsuario,cToken,dFecha) VALUES(%s,%s,%s)', (session['id'],token,fecha))
        mysql.connection.commit()
        respuesta = str(session['id'])
    else:
        respuesta = "usuario incorrecto"
    cursor.close()
    if respuesta == "1":
        return redirect(url_for('clientes'))
    else:
        return redirect(url_for('login'))
   

@app.route('/crear-cliente', methods=['POST'])
def crearCliente():
    cursor = mysql.connection.cursor()

    Nombres = request.form.get('Nombres')
    Apellidos = request.form.get('Apellidos')
    Edad = request.form.get('Edad')
    try:
        cursor.execute('INSERT INTO cliente(cNombres,cApellidos,iEdad) VALUES(%s,%s,%s)', (Nombres,Apellidos,Edad))
        mysql.connection.commit()
        return {"Resultado":"ok"}
    except Exception as e:
        mysql.connection.rollback()
        error = "Ocurrio un error: {e}"
        return {"Resultado":error}


    return {"nombres":nombres,"apellidos":apellidos}

@app.route('/clientes')
@login_required
def clientes():
    ActualizaToken("normal")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cliente WHERE lActivo=1")
    data = cur.fetchall() 
    return render_template('clientes.html', Clientes = data)
    
@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/editar-cliente')
def editarcliente():
    return ('editar cliente')

if __name__ == '__main__':
    app.run(port=3000, debug=True)