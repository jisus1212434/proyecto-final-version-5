
import sqlite3

conexion = sqlite3.connect("hospital.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pacientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    edad TEXT,
    sexo TEXT,
    enfermedad TEXT,
    sintoma TEXT,
    telefono TEXT,
    triaje TEXT,
    fecha TEXT
)
""")

conexion.commit()

def guardar_paciente_sqlite(nombre, edad, sexo, enfermedad, sintoma, telefono, triaje, fecha):
    cursor.execute(
        "INSERT INTO pacientes(nombre,edad,sexo,enfermedad,sintoma,telefono,triaje,fecha) VALUES(?,?,?,?,?,?,?,?)",
        (nombre, edad, sexo, enfermedad, sintoma, telefono, triaje, fecha)
    )
    conexion.commit()

def cargar_pacientes_sqlite():
    try:
        for fila in tabla_pacientes.get_children():
            tabla_pacientes.delete(fila)

        cursor.execute("SELECT nombre,edad,sexo,enfermedad,sintoma,triaje FROM pacientes")
        for row in cursor.fetchall():
            tabla_pacientes.insert("", END, values=row)
    except:
        pass


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime


pacientes = []
medicos = []
medicamentos = []
citas = []
habitaciones = []
facturas = []
usuarios = []

usuario_actual = ""
rol_actual = ""

ADMIN_USER = "admin"
ADMIN_PASS = "123456"

import sys

def cerrar_login():
    sys.exit()




def limpiar():
    entrada_nombre.delete(0, END)
    entrada_edad.delete(0, END)
    entrada_sexo.delete(0, END)
    entrada_enfermedad.delete(0, END)
    entrada_sintoma.delete(0, END)
    entrada_telefono.delete(0, END)



def registrar_paciente():

    nombre = entrada_nombre.get()
    edad = entrada_edad.get()
    sexo = entrada_sexo.get()
    enfermedad = entrada_enfermedad.get()
    sintoma = entrada_sintoma.get()
    telefono = entrada_telefono.get()

    if (
        nombre == "" or
        edad == "" or
        sexo == "" or
        enfermedad == "" or
        sintoma == ""
    ):
        messagebox.showerror(
            "Error",
            "Complete Nombre, Edad y Sexo"
        )
        return

    nivel = "LEVE"

    graves = [
        "hemorragia",
        "convulsiones",
        "dificultad respiratoria",
        "desmayo",
        "fractura"
    ]

    if sintoma.lower() in graves:
        nivel = "GRAVE"

    paciente = {
        "nombre": nombre,
        "edad": edad,
        "sexo": sexo,
        "enfermedad": enfermedad,
        "sintoma": sintoma,
        "telefono": telefono,
        "triaje": nivel,
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "historial": []
    }

    pacientes.append(paciente)

    guardar_paciente_sqlite(
        nombre, edad, sexo,
        enfermedad, sintoma,
        telefono, nivel,
        datetime.now().strftime("%d/%m/%Y")
    )

    tabla_pacientes.insert(
        "",
        END,
        values=(
            nombre,
            edad,
            sexo,
            enfermedad,
            sintoma,
            nivel
        )
    )

    messagebox.showinfo(
        "Hospital",
        "Paciente registrado correctamente"
    )

    limpiar()



def mostrar_pacientes():

    cuadro_texto.delete("1.0", END)

    for p in pacientes:

        datos = (
            "================================\n"
            f"Nombre: {p['nombre']}\n"
            f"Edad: {p['edad']}\n"
            f"Sexo: {p['sexo']}\n"
            f"Enfermedad: {p['enfermedad']}\n"
            f"Sintoma: {p['sintoma']}\n"
            f"Telefono: {p['telefono']}\n"
            f"Triaje: {p['triaje']}\n"
            f"Fecha: {p['fecha']}\n"
        )

        cuadro_texto.insert(END, datos)



def eliminar_paciente():

    nombre = entrada_busqueda.get()

    encontrado = False

    for paciente in pacientes:

        if paciente["nombre"] == nombre:

            pacientes.remove(paciente)
            encontrado = True

            messagebox.showinfo(
                "Hospital",
                "Paciente eliminado"
            )

            actualizar_tabla()

            break

    if encontrado == False:

        messagebox.showerror(
            "Error",
            "Paciente no encontrado"
        )



def actualizar_tabla():

    for fila in tabla_pacientes.get_children():
        tabla_pacientes.delete(fila)

    for p in pacientes:

        tabla_pacientes.insert(
            "",
            END,
            values=(
                p["nombre"],
                p["edad"],
                p["sexo"],
                p["enfermedad"],
                p["sintoma"],
                p["triaje"]
            )
        )



def buscar_paciente():

    nombre = entrada_busqueda.get()

    cuadro_texto.delete("1.0", END)

    for p in pacientes:

        if p["nombre"] == nombre:

            texto = (
                f"Nombre: {p['nombre']}\n"
                f"Edad: {p['edad']}\n"
                f"Sexo: {p['sexo']}\n"
                f"Enfermedad: {p['enfermedad']}\n"
                f"Sintoma: {p['sintoma']}\n"
                f"Telefono: {p['telefono']}\n"
                f"Triaje: {p['triaje']}\n"
            )

            cuadro_texto.insert(END, texto)


def registrar_medico():

    nombre = entry_medico.get()
    especialidad = entry_especialidad.get()

    medico = {
        "nombre": nombre,
        "especialidad": especialidad
    }

    medicos.append(medico)

    lista_medicos.insert(
        END,
        f"{nombre} - {especialidad}"
    )

    entry_medico.delete(0, END)
    entry_especialidad.delete(0, END)



def registrar_medicamento():

    nombre = entry_medicamento.get()
    cantidad = entry_cantidad.get()

    medicamento = {
        "nombre": nombre,
        "cantidad": cantidad
    }

    medicamentos.append(medicamento)

    lista_medicamentos.insert(
        END,
        f"{nombre} - Stock: {cantidad}"
    )


def agregar_historial():

    nombre = entrada_busqueda.get()
    nota = texto_historial.get("1.0", END)

    for p in pacientes:

        if p["nombre"] == nombre:

            p["historial"].append(nota)

            messagebox.showinfo(
                "Hospital",
                "Nota agregada"
            )



def estadisticas():

    graves = 0
    leves = 0
    hombres = 0
    mujeres = 0

    for p in pacientes:

        if p["triaje"] == "GRAVE":
            graves += 1
        else:
            leves += 1

        if p["sexo"].lower() == "hombre":
            hombres += 1
        else:
            mujeres += 1

    texto = (
        f"TOTAL PACIENTES: {len(pacientes)}\n\n"
        f"CASOS GRAVES: {graves}\n"
        f"CASOS LEVES: {leves}\n\n"
        f"HOMBRES: {hombres}\n"
        f"MUJERES: {mujeres}\n\n"
        f"MEDICOS: {len(medicos)}\n"
        f"MEDICAMENTOS: {len(medicamentos)}"
    )

    messagebox.showinfo(
        "Estadisticas",
        texto
    )



def registrar_cita():

    paciente = entry_cita_paciente.get()
    fecha = entry_cita_fecha.get()
    hora = entry_cita_hora.get()

    cita = {
        "paciente": paciente,
        "fecha": fecha,
        "hora": hora
    }

    citas.append(cita)

    lista_citas.insert(
        END,
        f"{paciente} - {fecha} - {hora}"
    )



def generar_factura():

    paciente = entry_factura_nombre.get()
    monto = entry_factura_monto.get()

    factura = {
        "paciente": paciente,
        "monto": monto
    }

    facturas.append(factura)

    lista_facturas.insert(
        END,
        f"{paciente} - ${monto}"
    )


def registrar_usuario():

    usuario = entry_usuario.get()
    password = entry_password.get()

    usuarios.append({
        "usuario": usuario,
        "password": password
    })

    messagebox.showinfo(
        "Sistema",
        "Usuario registrado"
    )




def iniciar_sesion():
    global usuario_actual, rol_actual

    nombre = entry_login_nombre.get().strip()
    rol = combo_login_rol.get().strip()
    password = entry_login_password.get()

    if nombre == "" or rol == "" or password == "":
        messagebox.showerror("Acceso","Complete todos los campos")
        return

    if len(password) < 6:
        messagebox.showerror(
            "Acceso",
            "La contraseña debe tener al menos 6 caracteres"
        )
        return

    if nombre == ADMIN_USER and password != ADMIN_PASS:
        messagebox.showerror(
            "Acceso",
            "Contraseña de administrador incorrecta"
        )
        return

    usuario_actual = nombre
    rol_actual = rol
    login.destroy()

login = Tk()
login.protocol("WM_DELETE_WINDOW", cerrar_login)
login.title("Acceso Hospitalario")
login.geometry("500x400")
login.config(bg="#1E3A5F")

Label(login,text="ACCESO HOSPITALARIO",font=("Arial",20,"bold"),bg="#1E3A5F",fg="white").pack(pady=20)
Label(login,text="Nombre",bg="#1E3A5F",fg="white").pack()
entry_login_nombre = Entry(login,width=30)
entry_login_nombre.pack()

Label(login,text="Rol Médico",bg="#1E3A5F",fg="white").pack()
combo_login_rol = ttk.Combobox(login,values=["Administrador","Doctor","Enfermero","Recepcionista","Farmaceutico"])
combo_login_rol.pack()

Label(login,text="Contraseña",bg="#1E3A5F",fg="white").pack()
entry_login_password = Entry(login,show="*",width=30)
entry_login_password.pack()

Button(login,text="Ingresar",bg="#28A745",fg="white",command=iniciar_sesion).pack(pady=20)
login.mainloop()


ventana = Tk()

ventana.title("SISTEMA HOSPITALARIO INTEGRAL")
ventana.geometry("1600x900")
ventana.config(bg="#CDEEFF")

titulo = Label(
    ventana,
    text="SISTEMA HOSPITALARIO INTEGRAL",
    font=("Arial",28,"bold"),
    bg="#B3E5FC",
    fg="#003366"
)

titulo.pack(pady=10)

Label(ventana,text=f"Usuario: {usuario_actual} | Rol: {rol_actual}",font=("Arial",12,"bold"),bg="#CDEEFF",fg="#003366").pack()



tabs = ttk.Notebook(ventana)
tabs.pack(fill="both", expand=True)



tab1 = Frame(tabs,bg="white")
tabs.add(tab1,text="Pacientes")

Label(tab1,text="Nombre").grid(row=0,column=0,padx=10,pady=10)
entrada_nombre = Entry(tab1)
entrada_nombre.grid(row=0,column=1)

Label(tab1,text="Edad").grid(row=1,column=0)
entrada_edad = ttk.Combobox(
    tab1,
    values=[str(i) for i in range(0,121)],
    width=10
)
entrada_edad.grid(row=1,column=1)

Label(tab1,text="Sexo").grid(row=2,column=0)
entrada_sexo = ttk.Combobox(tab1, values=["Hombre","Mujer","Otro","Prefiero no decirlo"])
entrada_sexo.grid(row=2,column=1)

Label(tab1,text="Enfermedad").grid(row=3,column=0)
entrada_enfermedad = ttk.Combobox(
    tab1,
    values=[
        "Gripe","COVID-19","Diabetes","Hipertension",
        "Asma","Migraña","Gastritis","Neumonia",
        "Infeccion Urinaria","Alergia","Fractura","Otra"
    ],
    width=25
)
entrada_enfermedad.grid(row=3,column=1)

Label(tab1,text="Sintoma").grid(row=4,column=0)
entrada_sintoma = ttk.Combobox(
    tab1,
    values=[
        "Fiebre","Tos","Dolor de cabeza",
        "Dificultad respiratoria","Hemorragia",
        "Convulsiones","Desmayo","Fractura",
        "Nauseas","Vomito","Dolor abdominal",
        "Mareo","Fatiga","Otro"
    ],
    width=25
)
entrada_sintoma.grid(row=4,column=1)

Label(tab1,text="Telefono").grid(row=5,column=0)
entrada_telefono = Entry(tab1)
entrada_telefono.grid(row=5,column=1)

Button(
    tab1,
    text="➕ Registrar Paciente",
    bg="#28A745",
    fg="white",
    command=registrar_paciente
).grid(row=6,column=0,pady=20)

Button(
    tab1,
    text="Mostrar Pacientes",
    bg="#007BFF",
    fg="white",
    command=mostrar_pacientes
).grid(row=6,column=1)



tabla_pacientes = ttk.Treeview(
    tab1,
    columns=(
        "Nombre",
        "Edad",
        "Sexo",
        "Enfermedad",
        "Sintoma",
        "Triaje"
    ),
    show="headings"
)

tabla_pacientes.heading("Nombre",text="Nombre")
tabla_pacientes.heading("Edad",text="Edad")
tabla_pacientes.heading("Sexo",text="Sexo")
tabla_pacientes.heading("Enfermedad",text="Enfermedad")
tabla_pacientes.heading("Sintoma",text="Sintoma")
tabla_pacientes.heading("Triaje",text="Triaje")

tabla_pacientes.grid(
    row=7,
    column=0,
    columnspan=4,
    pady=20
)


tab2 = Frame(tabs,bg="white")
tabs.add(tab2,text="Busqueda")

Label(tab2,text="Buscar paciente").pack(pady=10)

entrada_busqueda = Entry(tab2,width=40)
entrada_busqueda.pack()

Button(
    tab2,
    text="Buscar",
    command=buscar_paciente
).pack(pady=10)

Button(
    tab2,
    text="Eliminar",
    command=eliminar_paciente
).pack()

cuadro_texto = Text(
    tab2,
    width=100,
    height=25
)

cuadro_texto.pack(pady=20)



tab3 = Frame(tabs,bg="white")
tabs.add(tab3,text="Medicos")

Label(tab3,text="Nombre").pack()

entry_medico = Entry(tab3)
entry_medico.pack()

Label(tab3,text="Especialidad").pack()

entry_especialidad = ttk.Combobox(tab3, values=["Medicina General","Pediatria","Cardiologia","Neurologia","Dermatologia","Traumatologia","Ginecologia","Oncologia","Psiquiatria","Urologia","Cirugia General","Oftalmologia"])
entry_especialidad.pack()

Button(
    tab3,
    text="👨‍⚕️ Registrar Médico",
    command=registrar_medico
).pack(pady=10)

lista_medicos = Listbox(tab3,width=70,height=20)
lista_medicos.pack()



tab4 = Frame(tabs,bg="white")
tabs.add(tab4,text="Medicamentos")

Label(tab4,text="Medicamento").pack()

entry_medicamento = Entry(tab4)
entry_medicamento.pack()

Label(tab4,text="Cantidad").pack()

entry_cantidad = Entry(tab4)
entry_cantidad.pack()

Button(
    tab4,
    text="💊 Registrar Medicamento",
    command=registrar_medicamento
).pack(pady=10)

lista_medicamentos = Listbox(tab4,width=70,height=20)
lista_medicamentos.pack()


tab5 = Frame(tabs,bg="white")
tabs.add(tab5,text="Historial")

texto_historial = Text(
    tab5,
    width=70,
    height=15
)

texto_historial.pack(pady=20)

Button(
    tab5,
    text="Agregar Historial",
    command=agregar_historial
).pack()



tab6 = Frame(tabs,bg="white")
tabs.add(tab6,text="Estadisticas")

Button(
    tab6,
    text="📊 Mostrar Estadísticas",
    bg="#FF9800",
    command=estadisticas
).pack(pady=100)



tab7 = Frame(tabs,bg="white")
tabs.add(tab7,text="Citas")

Label(tab7,text="Paciente").pack()

entry_cita_paciente = Entry(tab7)
entry_cita_paciente.pack()

Label(tab7,text="Fecha").pack()

entry_cita_fecha = Entry(tab7)
entry_cita_fecha.pack()

Label(tab7,text="Hora").pack()

entry_cita_hora = Entry(tab7)
entry_cita_hora.pack()

Button(
    tab7,
    text="Registrar Cita",
    command=registrar_cita
).pack(pady=10)

lista_citas = Listbox(tab7,width=70,height=20)
lista_citas.pack()





tab9 = Frame(tabs,bg="white")
tabs.add(tab9,text="Facturacion")

Label(tab9,text="Paciente").pack()

entry_factura_nombre = Entry(tab9)
entry_factura_nombre.pack()

Label(tab9,text="Monto").pack()

entry_factura_monto = Entry(tab9)
entry_factura_monto.pack()

Button(
    tab9,
    text="Generar Factura",
    command=generar_factura
).pack(pady=10)

lista_facturas = Listbox(tab9,width=70,height=20)
lista_facturas.pack()

tab10 = Frame(tabs,bg="white")
tabs.add(tab10,text="Usuarios")

Label(tab10,text="Usuario").pack()

entry_usuario = Entry(tab10)
entry_usuario.pack()

Label(tab10,text="Contraseña").pack()

entry_password = Entry(tab10,show="*")
entry_password.pack()

Button(
    tab10,
    text="Registrar Usuario",
    command=registrar_usuario
).pack(pady=10)


tab11 = Frame(tabs,bg="white")
tabs.add(tab11,text="Informacion")

info = """
SISTEMA HOSPITALARIO INTEGRAL

Funciones:
- Registro de pacientes
- Triaje automatico
- Historial clinico
- Control medico
- Medicamentos
- Habitaciones
- Facturacion
- Estadisticas
"""

Label(
    tab11,
    text=info,
    font=("Arial",14),
    bg="white",
    justify=LEFT
).pack(pady=50)


tab12 = Frame(tabs,bg="white")
tabs.add(tab12,text="Salir")

Button(
    tab12,
    text="🚪 Cerrar Sistema",
    bg="#DC3545",
    fg="white",
    font=("Arial",16),
    command=ventana.destroy
).pack(pady=200)



cargar_pacientes_sqlite()

ventana.mainloop()


# COLORES PROFESIONALES
COLOR_FONDO = "#0F172A"
COLOR_PANEL = "#1E293B"
COLOR_BOTON = "#2563EB"
COLOR_TEXTO = "white"
COLOR_EXITO = "#10B981"

# LOGO TEXTO
logo_hospital = "🏥 HOSPITAL INTEGRAL PLUS"

try:
    ventana.configure(bg=COLOR_FONDO)
except:
    pass

# FUNCION DE CARGA VISUAL
def animacion_inicio():
    try:
        splash = Toplevel()
        splash.title("Cargando Sistema")
        splash.geometry("500x250")
        splash.configure(bg=COLOR_FONDO)

        Label(
            splash,
            text="🏥 Iniciando Hospital Integral Plus...",
            font=("Arial",18,"bold"),
            bg=COLOR_FONDO,
            fg="white"
        ).pack(pady=40)

        barra = ttk.Progressbar(
            splash,
            orient="horizontal",
            length=300,
            mode="indeterminate"
        )
        barra.pack(pady=20)
        barra.start(10)

        splash.after(2500, splash.destroy)
        splash.update()

    except:
        pass

animacion_inicio()

# ENCABEZADO
try:
    encabezado = Label(
        ventana,
        text=logo_hospital,
        font=("Arial",22,"bold"),
        bg=COLOR_FONDO,
        fg="#38BDF8"
    )
    encabezado.pack(pady=10)
except:
    pass

# BOTONES MODERNOS
def aplicar_estilo_boton(btn):
    try:
        btn.configure(
            bg=COLOR_BOTON,
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Arial",11,"bold")
        )
    except:
        pass

# GRAFICAS
def mostrar_grafica():
    try:
        import matplotlib.pyplot as plt

        categorias = ["Pacientes","Medicos","Medicamentos","Citas"]
        valores = [
            len(pacientes),
            len(medicos),
            len(medicamentos),
            len(citas)
        ]

        plt.figure(figsize=(6,4))
        plt.bar(categorias,valores)
        plt.title("Estadisticas Hospitalarias")
        plt.xlabel("Categorias")
        plt.ylabel("Cantidad")
        plt.show()

    except Exception as e:
        messagebox.showerror("Error",str(e))



try:
    from tkinter import *
    from tkinter import ttk
except:
    pass

# ESTILO GENERAL MODERNO
try:
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "TFrame",
        background="#0F172A"
    )

    style.configure(
        "TLabel",
        background="#0F172A",
        foreground="white",
        font=("Segoe UI", 11)
    )

    style.configure(
        "Titulo.TLabel",
        font=("Segoe UI", 26, "bold"),
        foreground="#38BDF8",
        background="#0F172A"
    )

    style.configure(
        "Card.TFrame",
        background="#1E293B",
        relief="flat"
    )

    style.configure(
        "Modern.TButton",
        font=("Segoe UI", 11, "bold"),
        padding=12,
        background="#2563EB",
        foreground="white",
        borderwidth=0
    )

    style.map(
        "Modern.TButton",
        background=[("active", "#1D4ED8")]
    )

except:
    pass


def crear_tarjeta(parent, texto):
    frame = Frame(
        parent,
        bg="#1E293B",
        bd=0,
        highlightthickness=2,
        highlightbackground="#334155"
    )

    Label(
        frame,
        text=texto,
        bg="#1E293B",
        fg="white",
        font=("Segoe UI", 12, "bold")
    ).pack(padx=20, pady=20)

    return frame



def hover_in(e):
    try:
        e.widget["bg"] = "#1D4ED8"
    except:
        pass

def hover_out(e):
    try:
        e.widget["bg"] = "#2563EB"
    except:
        pass


try:
    for widget in ventana.winfo_children():
        if isinstance(widget, Button):
            widget.configure(
                bg="#2563EB",
                fg="white",
                activebackground="#1D4ED8",
                activeforeground="white",
                font=("Segoe UI", 11, "bold"),
                relief="flat",
                cursor="hand2",
                padx=15,
                pady=10
            )

            widget.bind("<Enter>", hover_in)
            widget.bind("<Leave>", hover_out)

except:
    pass



try:
    barra_superior = Frame(
        ventana,
        bg="#111827",
        height=60
    )

    barra_superior.pack(fill="x")

    titulo_visual = Label(
        barra_superior,
        text="🏥 HOSPITAL INTEGRAL PREMIUM",
        bg="#111827",
        fg="#38BDF8",
        font=("Segoe UI", 24, "bold")
    )

    titulo_visual.pack(pady=10)

except:
    pass



try:
    footer = Label(
        ventana,
        text="Sistema Médico Profesional v12",
        bg="#0F172A",
        fg="#94A3B8",
        font=("Segoe UI", 9)
    )

    footer.pack(side="bottom", pady=10)

except:
    pass


try:
    bienvenida = Label(
        ventana,
        text="✨ Bienvenido al sistema hospitalario inteligente",
        bg="#0F172A",
        fg="#E2E8F0",
        font=("Segoe UI", 13, "italic")
    )

    bienvenida.pack(pady=5)

except:
    pass

