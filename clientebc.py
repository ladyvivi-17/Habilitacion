#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from bs4 import BeautifulSoup
from requests import get
import Pyro4
from Tkinter import *
import ttk
import Tkinter as tk
import tkMessageBox
from PIL import ImageTk
from functools import partial
import sys, string, urllib
from urllib2 import urlopen
import re
import MySQLdb
import json
import ast
from functools import partial

@Pyro4.expose
class usuario():
	def __init__(self, id, usuario):
		self.id = id
		self.usuario = usuario
	def __str__(self):
		return self.usuario
class Cliente(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.initUI()

    def initUI(self):

         b = tk.Button()
         image = ImageTk.PhotoImage(file="login.png")
         b.config(image=image, bd=0)
         b.image = image
         b.pack()

         login = Frame(bd=4, relief='ridge')
         login.pack()

         Label(login, text="E-mail:", width=10, height=2, font=('MS', 10, 'bold')).pack()
         email = Entry(login)
         email.pack()

         Label(login, text="Password:", width=10, height=2, font=('MS', 10, 'bold')).pack()
         clave = Entry(login, show="*")
         clave.pack()


         f0 = tk.LabelFrame(login, width=100, height=100, relief='flat', borderwidth=4)
         f0.pack(padx=5, pady=5, side='left')
         Button(f0, text="Login", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda: self.ingresar(email, clave)).pack()

         f1 = tk.LabelFrame(login, width=100, height=100, relief='flat', borderwidth=4)
         f1.pack(padx=5, pady=5, side='left')
         Button(f1, text="Registrarse", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=self.registrar_usuario).pack()


    def registrar_usuario(self):

        self.idusuario = StringVar(value=1)

        register = Toplevel()

        Label(register, text="Nombre Completo:").pack()
        self.nombre = Entry(register)
        self.nombre.pack()

        Label(register, text="Apellidos:").pack()
        self.apellido = Entry(register)
        self.apellido.pack()

        Label(register, text="Password:").pack()
        self.clave = Entry(register, show="*")
        self.clave.pack()

        Label(register, text="E-mail:").pack()
        self.email = Entry(register)
        self.email.pack()

        Label(register, text="Cedula:").pack()
        self.cedula = Entry(register)
        self.cedula.pack()

        Label(register, text="Seleccione el tipo de  usuario").pack()
        self.cbotemporadas = ttk.Combobox(register, textvariable=self.idusuario, state="readonly")
        self.cbotemporadas.pack()
        self.cbotemporadas.bind("<<ComboboxSelected>>", self.usuario_tipo)
        self.valores = self._cargaFromObject(o_usuario, self.cbotemporadas, "usuario", "id", seleccionado, self.idusuario)


        Button(register, text="Crear", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2, command=self.usuario_tipo).pack()


    def _cargaFromObject(self, coleccion, objeto, campodesc, campoid, val2select, variable):
        misc, misv = [], []
        for vv in coleccion:
            misv.append(getattr(vv, campodesc))
            misc.append(getattr(vv, campoid))
            if getattr(vv, campoid) == val2select: variable.set(getattr(vv, campodesc))
        objeto["values"] = misv
        return dict(zip(misv, misc))  # Crea diccionario



    def ingresar(self, email, clave):

        mail = email.get()
        pasw = clave.get()

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")# conexion servidor

        tipo = ingreso.login_usuario(mail, pasw)
        id_us = ingreso.obtener_idus(mail, pasw)
        if (tipo==0):
            tkMessageBox.showerror(title="Ingresar", message="Usuario o contraseña incorrecta")
        if (tipo==1):
            self.master.destroy()
            self.usuario_cliente(id_us)
        if (tipo==2):
            self.master.destroy()
            self.usuario_admin()


    def usuario_tipo(self):

        grabar = 1
        val = self.idusuario.get()
        id = self.valores[val]

        nom = self.nombre.get()
        ape = self.apellido.get()
        cl = self.clave.get()
        em = self.email.get()

        ced = self.cedula.get()
        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        if em == '' or cl == '':

           grabar = 0

        if grabar == 1:
            result = ingreso.login_register(nom, ape, id, cl, em, ced)

            if (result==0):
               tkMessageBox.showinfo(title="Info", message="Usuario creado con exito")

            else:
               tkMessageBox.showerror(title="Error", message="Error al crear usuario")
        else:
            tkMessageBox.showinfo(title="Info", message="Todos los campos son obligatorios")




    def usuario_cliente(self, id_us):

        ventana_cliente = Tk()
        prod = producto()
        a = tk.Button(ventana_cliente)
        image = ImageTk.PhotoImage(file="prestamos.png")
        a.config(image=image, command=lambda: prod.ges_prestamoc(id_us), bd=0)
        a.image = image
        a.pack()

        b = tk.Button(ventana_cliente)
        image = ImageTk.PhotoImage(file="ahorros.png")
        b.config(image=image, command=lambda : prod.ges_ahorroc(id_us), bd=0)
        b.image = image
        b.pack()

        c = tk.Button(ventana_cliente)
        image = ImageTk.PhotoImage(file="factura.png")
        c.config(image=image, command=lambda: self.factura_ver(id_us), bd=0)
        c.image = image
        c.pack()

        d = tk.Button(ventana_cliente)
        image = ImageTk.PhotoImage(file="salir.png")
        d.config(image=image, command=ventana_cliente.destroy, bd=0)
        d.image = image
        d.pack()

    def usuario_admin(self):

        ventana_admin = Tk()
        prod = producto()

        a = tk.Button(ventana_admin)
        image = ImageTk.PhotoImage(file="alertas.png")
        a.config(image=image, bd=0)
        a.image = image
        a.pack()

        b = tk.Button(ventana_admin)
        image = ImageTk.PhotoImage(file="prestamos.png")
        b.config(image=image, bd=0, command=lambda: prod.ges_prestamo())
        b.image = image
        b.pack()

        c = tk.Button(ventana_admin)
        image = ImageTk.PhotoImage(file="ahorros.png")
        c.config(image=image, bd=0, command=lambda: prod.ges_ahorro())
        c.image = image
        c.pack()

        d = tk.Button(ventana_admin)
        image = ImageTk.PhotoImage(file="usuario.png")
        d.config(image=image, bd=0, command=lambda: prod.listar_usuarios())
        d.image = image
        d.pack()

        e = tk.Button(ventana_admin)
        image = ImageTk.PhotoImage(file="log.png")
        e.config(image=image, bd=0, command=self.log_usuarios)
        e.image = image
        e.pack()

        f = tk.Button(ventana_admin)
        image = ImageTk.PhotoImage(file="salir.png")
        f.config(image=image, command=ventana_admin.destroy, bd=0)
        f.image = image
        f.pack()


    def log_usuarios(self):



        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        result = ingreso.listar_log()
        self.ventana_log = Tk()



        vu = tk.LabelFrame(self.ventana_log, width=550, height=100, relief='flat', borderwidth=4)
        vu.grid(row=1, column=0, padx=10, pady=2)

        Title = Label(vu, text='Fecha', bg='DodgerBlue4', fg='white', width=22, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vu, text='Login', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vu, text='IP', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vu, text='Evento', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)

        vl = tk.LabelFrame(self.ventana_log, width=650, height=20, relief='flat', borderwidth=4)
        vl.grid(row=2, column=0, padx=10, pady=2)

        try:
            i = 1

            for registro in result:
                fecha = registro[1]
                ip = registro[2]
                evento = registro[3]
                login = registro[4]

                # Imprimimos los resultados obtenidos

                Contenido = Label(vl, justify=LEFT, text="%s" % (fecha), bg='turquoise3', fg='white', width=20,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido1 = Label(vl, justify=LEFT, text="%s" % (login), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido2 = Label(vl, justify=LEFT, text="%s" % (ip), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido3 = Label(vl, justify=LEFT, text="%s" % (evento), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1, padx=2, pady=2)



                i = i + 1

        except:
            print("Error")


def creavalores():
	c = usuario(1,"Cliente")
	o_usuario.append(c)
	c = usuario(2,"Administrador")
	o_usuario.append(c)

o_usuario = []
seleccionado = 2

class producto(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.servidorp = Pyro4.Proxy("PYRONAME:Leidy.Producto")  # conexion servidor

    def ges_prestamo(self):

        self.ventana = Tk()
        self.ventana.geometry("800x450+400+400")
        Button(self.ventana, text="Nuevo", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2,
               command=lambda:self.nuevo_prestamo()).grid(row=0, column=0, columnspan=1,
                                                                                      rowspan=1)
        self.grid_prestamo()
    def grid_prestamo(self):
        result = self.servidorp.listar(0)
        vu = tk.LabelFrame(self.ventana, width=550, height=100, relief='flat', borderwidth=4)
        vu.grid(row=1, column=0, padx=10, pady=2)

        Title = Label(vu, text='Codigo', bg='DodgerBlue4', fg='white', width=16, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vu, text='Descripción', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vu, text='Tasa', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vu, text='Tiempo', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)



        vl = tk.LabelFrame(self.ventana, width=650, height=20, relief='flat', borderwidth=4)
        vl.grid(row=2, column=0, padx=10, pady=2)

        try:
            i = 1
            contenido4 = []
            for registro in result:
                codigo = registro[0]
                descripcion = registro[1]
                tasa = registro[2]
                tiempo = registro[3]


                # Imprimimos los resultados obtenidos

                Contenido = Label(vl, justify=LEFT, text="%s" % (codigo), bg='turquoise3', fg='white', width=15,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido1 = Label(vl, justify=LEFT, text="%s" % (descripcion), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido2 = Label(vl, justify=LEFT, text="%s" % (tasa), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido3 = Label(vl, justify=LEFT, text="%s" % (tiempo), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1, padx=2, pady=2)

                contenido4.append(Button(vl, text="Editar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda codigo=codigo: self.editar_prestamo(codigo)).grid(row="%d" % (i), column=4, columnspan=1, rowspan=1))

                i = i + 1

        except:
            print("Error")

    def ges_prestamoc(self, id_us):

        self.ventana2 = Tk()
        self.ventana2.geometry("800x450+400+400")
        self.grid_prestamoc(id_us)
    def grid_prestamoc(self, id_us):
        result = self.servidorp.listar(0)
        vu = tk.LabelFrame(self.ventana2, width=550, height=100, relief='flat', borderwidth=4)
        vu.grid(row=0, column=0, padx=10, pady=2)

        Title = Label(vu, text='Codigo', bg='DodgerBlue4', fg='white', width=16, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vu, text='Descripción', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vu, text='Tasa', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vu, text='Tiempo', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)



        vl = tk.LabelFrame(self.ventana2, width=650, height=20, relief='flat', borderwidth=4)
        vl.grid(row=1, column=0, padx=10, pady=2)

        try:
            i = 1
            contenido4 = []

            for registro in result:
                codigo = registro[0]
                descripcion = registro[1]
                tasa = registro[2]
                tiempo = registro[3]


                # Imprimimos los resultados obtenidos

                Contenido = Label(vl, justify=LEFT, text="%s" % (codigo), bg='turquoise3', fg='white', width=15,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido1 = Label(vl, justify=LEFT, text="%s" % (descripcion), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido2 = Label(vl, justify=LEFT, text="%s" % (tasa), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido3 = Label(vl, justify=LEFT, text="%s" % (tiempo), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1, padx=2, pady=2)

                contenido4.append(Button(vl, text="Solicitar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda id_us = id_us, codigo=codigo:self.valor_solicitu(codigo, id_us)).grid(row="%d" % (i), column=4, columnspan=1, rowspan=1))

                i = i + 1

        except:
            print("Error")

        vpq2 = tk.LabelFrame(self.ventana2, width=450, height=50, relief='flat', borderwidth=4)
        vpq2.grid(row=2, column=0, padx=10, pady=2)
        Button(vpq2, text="Consultar Estado Prestamos", bg="turquoise4", bd=0, fg='white', font=('MS', 12, 'bold'),
               activebackground="turquoise3", width=30, height=5,
               command=lambda: self.consultar_estado(id_us)).grid(row=2, column=1, columnspan=1, rowspan=1)

    def ges_ahorro(self):

        self.ventana3 = Tk()
        self.ventana3.geometry("800x450+400+400")
        Button(self.ventana3, text="Nuevo", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2,
               command=lambda: self.nuevo_ahorro()).grid(row=0, column=0, columnspan=1,
                                                           rowspan=1)
        self.grid_ahorro()

    def grid_ahorro(self):
        result = self.servidorp.listar_ahorro(1)
        vu = tk.LabelFrame(self.ventana3, width=550, height=100, relief='flat', borderwidth=4)
        vu.grid(row=1, column=0, padx=10, pady=2)

        Title = Label(vu, text='Codigo', bg='DodgerBlue4', fg='white', width=16, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vu, text='Descripción', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vu, text='Tasa', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vu, text='Tiempo', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)

        vl = tk.LabelFrame(self.ventana3, width=650, height=20, relief='flat', borderwidth=4)
        vl.grid(row=2, column=0, padx=10, pady=2)

        try:
            i = 1
            contenido4 = []
            for registro in result:
                codigo = registro[0]
                descripcion = registro[1]
                tasa = registro[2]
                tiempo = registro[3]

                # Imprimimos los resultados obtenidos

                Contenido = Label(vl, justify=LEFT, text="%s" % (codigo), bg='turquoise3', fg='white', width=15,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido1 = Label(vl, justify=LEFT, text="%s" % (descripcion), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido2 = Label(vl, justify=LEFT, text="%s" % (tasa), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido3 = Label(vl, justify=LEFT, text="%s" % (tiempo), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1, padx=2, pady=2)

                contenido4.append(Button(vl, text="Editar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
                                         activebackground="turquoise3", width=10, height=2,
                                         command=lambda codigo=codigo: self.editar_ahorro(codigo)).grid(
                    row="%d" % (i), column=4, columnspan=1, rowspan=1))

                i = i + 1

        except:
            print("Error")


    def ges_ahorroc(self, id_us):

        self.ventana5 = Tk()
        self.ventana5.geometry("800x450+400+400")
        self.grid_ahorroc(id_us)
    def grid_ahorroc(self, id_us):
        result = self.servidorp.listar_ahorro(1)
        vu = tk.LabelFrame(self.ventana5, width=550, height=100, relief='flat', borderwidth=4)
        vu.grid(row=0, column=0, padx=10, pady=2)

        Title = Label(vu, text='Codigo', bg='DodgerBlue4', fg='white', width=16, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vu, text='Descripción', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vu, text='Tasa', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vu, text='Tiempo', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)



        vl = tk.LabelFrame(self.ventana5, width=650, height=20, relief='flat', borderwidth=4)
        vl.grid(row=1, column=0, padx=10, pady=2)

        try:
            i = 1
            contenido4 = []

            for registro in result:
                codigo = registro[0]
                descripcion = registro[1]
                tasa = registro[2]
                tiempo = registro[3]


                # Imprimimos los resultados obtenidos

                Contenido = Label(vl, justify=LEFT, text="%s" % (codigo), bg='turquoise3', fg='white', width=15,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido1 = Label(vl, justify=LEFT, text="%s" % (descripcion), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido2 = Label(vl, justify=LEFT, text="%s" % (tasa), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido3 = Label(vl, justify=LEFT, text="%s" % (tiempo), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1, padx=2, pady=2)

                contenido4.append(Button(vl, text="Abrir Cuenta", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=15, height=2, command=lambda id_us = id_us, codigo=codigo:self.valor_solicitu_ahorro(codigo, id_us)).grid(row="%d" % (i), column=4, columnspan=1, rowspan=1))

                i = i + 1

        except:
            print("Error")

        vpq2 = tk.LabelFrame(self.ventana5, width=450, height=50, relief='flat', borderwidth=4)
        vpq2.grid(row=2, column=0, padx=10, pady=2)
        Button(vpq2, text="Consultar Estado de Ahorros", bg="turquoise4", bd=0, fg='white', font=('MS', 12, 'bold'),
               activebackground="turquoise3", width=30, height=5,
               command=lambda: self.consultar_estado_ahorro(id_us)).grid(row=2, column=1, columnspan=1, rowspan=1)

    def nuevo_ahorro(self):
        self.top = Toplevel(self.ventana3)
        self.top.geometry('650x200+20+20')
        self.top.focus_set()
        self.top.grab_set()
        self.top.transient(master=self.ventana3)

        vpq = tk.LabelFrame(self.top, width=450, height=50, relief='flat', borderwidth=4)
        vpq.grid(row=0, column=0, padx=10, pady=2)
        Label(vpq, text="Descripción:", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=0, columnspan=1, rowspan=1)
        descripcion = Entry(vpq)
        descripcion.grid(row=2, column=0, columnspan=1, rowspan=1)
        Label(vpq, text="Interes", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=1, columnspan=1, rowspan=1)
        tasa = Entry(vpq)
        tasa.grid(row=2, column=1, columnspan=1, rowspan=1)
        Label(vpq, text="Tiempo", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=2, columnspan=1, rowspan=1)
        tiempo = Entry(vpq)
        tiempo.grid(row=2, column=2, columnspan=1, rowspan=1)
        Button(vpq, text="Crear", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda:self.insertar_ahorro(descripcion, tasa, tiempo)).grid(row=2, column=4, columnspan=1, rowspan=1)


    def nuevo_prestamo(self):
        self.top = Toplevel(self.ventana)
        self.top.geometry('650x200+20+20')
        self.top.focus_set()
        self.top.grab_set()
        self.top.transient(master=self.ventana)

        vpq = tk.LabelFrame(self.top, width=450, height=50, relief='flat', borderwidth=4)
        vpq.grid(row=0, column=0, padx=10, pady=2)
        Label(vpq, text="Descripción:", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=0, columnspan=1, rowspan=1)
        descripcion = Entry(vpq)
        descripcion.grid(row=2, column=0, columnspan=1, rowspan=1)
        Label(vpq, text="Interes", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=1, columnspan=1, rowspan=1)
        tasa = Entry(vpq)
        tasa.grid(row=2, column=1, columnspan=1, rowspan=1)
        Label(vpq, text="Tiempo", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=2, columnspan=1, rowspan=1)
        tiempo = Entry(vpq)
        tiempo.grid(row=2, column=2, columnspan=1, rowspan=1)
        Button(vpq, text="Crear", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda:self.insertar_prestramo(descripcion, tasa, tiempo)).grid(row=2, column=4, columnspan=1, rowspan=1)

        #Button(vpq, text="Actualizar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2).grid(row=2, column=5, columnspan=1, rowspan=1)

    def valor_solicitu(self, id, id_usuario):
        self.top3 = Toplevel(self.ventana2)
        self.top3.geometry('200x200+20+20')
        self.top3.focus_set()
        self.top3.grab_set()
        self.top3.transient(master=self.ventana2)
        vpq = tk.LabelFrame(self.top3, width=450, height=50, relief='flat', borderwidth=4)
        vpq.grid(row=0, column=0, padx=10, pady=2)
        Label(vpq, text="Monto solicitado:", width=20, height=2, font=('MS', 10, 'bold')).grid(row=1, column=0, columnspan=1,
                                                                                          rowspan=1)
        monto = Entry(vpq)
        monto.grid(row=2, column=0, columnspan=1, rowspan=1)


        Button(vpq, text="Enviar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2,
               command=lambda: self.enviar_prestamos(id, id_usuario, monto)).grid(row=3, column=0, columnspan=1,

                                                                                        rowspan=1)

    def valor_solicitu_ahorro(self, id, id_usuario):
        self.top3 = Toplevel(self.ventana5)
        self.top3.geometry('200x200+20+20')
        self.top3.focus_set()
        self.top3.grab_set()
        self.top3.transient(master=self.ventana5)
        vpq = tk.LabelFrame(self.top3, width=450, height=50, relief='flat', borderwidth=4)
        vpq.grid(row=0, column=0, padx=10, pady=2)
        Label(vpq, text="Capital Inicial:", width=20, height=2, font=('MS', 10, 'bold')).grid(row=1, column=0, columnspan=1,
                                                                                          rowspan=1)
        monto = Entry(vpq)
        monto.grid(row=2, column=0, columnspan=1, rowspan=1)


        Button(vpq, text="Enviar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2,
               command=lambda: self.enviar_ahorro(id, id_usuario, monto)).grid(row=3, column=0, columnspan=1,

                                                                                        rowspan=1)
    def consultar_estado(self, id):

        self.top4 = Toplevel(self.ventana2)
        self.top4.geometry('980x200+20+20')
        self.top4.focus_set()
        self.top4.grab_set()
        self.top4.transient(master=self.ventana2)
        result = self.servidorp.estado_prestamo(id, 0)
        vu = tk.LabelFrame(self.top4, width=550, height=300, relief='flat', borderwidth=4)
        vu.grid(row=0, column=0, padx=10, pady=2)

        Title = Label(vu, text='Fecha Solicitud', bg='DodgerBlue4', fg='white', width=16, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vu, text='Descripción', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vu, text='Tasa', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vu, text='Cuotas', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)

        Title4 = Label(vu, text='Valor', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title4.grid(row=0, column=4, columnspan=1, rowspan=1)

        Title5 = Label(vu, text='Estado', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title5.grid(row=0, column=5, columnspan=1, rowspan=1)

        vl = tk.LabelFrame(self.top4, width=850, height=200, relief='flat', borderwidth=4)
        vl.grid(row=1, column=0, padx=10, pady=2)

        try:
            i = 1


            for registro in result:

                t_estado = registro[14]

                if t_estado == 0:
                    tipoestado = "Pendiente"

                if t_estado == 1:
                    tipoestado = "Aprobado"

                fecha= registro[12]
                descripcion = registro[2]
                tasa = registro[11]
                cuotas = registro[5]
                valor= registro[4]

                # Imprimimos los resultados obtenidos

                Contenido = Label(vl, justify=LEFT, text="%s" % (fecha), bg='turquoise3', fg='white', width=15,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido1 = Label(vl, justify=LEFT, text="%s" % (descripcion), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido2 = Label(vl, justify=LEFT, text="%s" % (tasa), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido3 = Label(vl, justify=LEFT, text="%s" % (cuotas), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido4 = Label(vl, justify=LEFT, text="%s" % (valor), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido4.grid(row="%d" % (i), column=4, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido5 = Label(vl, justify=LEFT, text="%s" % (tipoestado), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido5.grid(row="%d" % (i), column=5, columnspan=1, rowspan=1, padx=2, pady=2)

                i = i + 1

        except:
            print("Error")
    def consultar_estado_ahorro(self, id_us):

        self.top4 = Toplevel(self.ventana5)
        self.top4.geometry('600x200+20+20')
        self.top4.focus_set()
        self.top4.grab_set()
        self.top4.transient(master=self.ventana5)
        result = self.servidorp.estado_ahorro(id, 1)
        vu = tk.LabelFrame(self.top4, width=550, height=300, relief='flat', borderwidth=4)
        vu.grid(row=0, column=0, padx=10, pady=2)

        Title = Label(vu, text='Fecha Solicitud', bg='DodgerBlue4', fg='white', width=16, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vu, text='Descripción', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vu, text='Tasa', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vu, text='Cuotas', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)

        Title4 = Label(vu, text='Valor', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title4.grid(row=0, column=4, columnspan=1, rowspan=1)

        Title5 = Label(vu, text='Estado', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title5.grid(row=0, column=5, columnspan=1, rowspan=1)

        vl = tk.LabelFrame(self.top4, width=850, height=200, relief='flat', borderwidth=4)
        vl.grid(row=1, column=0, padx=10, pady=2)

        try:
            i = 1


            for registro in result:

                t_estado = registro[14]

                if t_estado == 0:
                    tipoestado = "Pendiente"

                if t_estado == 1:
                    tipoestado = "Aprobado"

                fecha= registro[12]
                descripcion = registro[2]
                tasa = registro[11]
                cuotas = registro[5]
                valor= registro[4]

                # Imprimimos los resultados obtenidos

                Contenido = Label(vl, justify=LEFT, text="%s" % (fecha), bg='turquoise3', fg='white', width=15,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido1 = Label(vl, justify=LEFT, text="%s" % (descripcion), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido2 = Label(vl, justify=LEFT, text="%s" % (tasa), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido3 = Label(vl, justify=LEFT, text="%s" % (cuotas), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido4 = Label(vl, justify=LEFT, text="%s" % (valor), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido4.grid(row="%d" % (i), column=4, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido5 = Label(vl, justify=LEFT, text="%s" % (tipoestado), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido5.grid(row="%d" % (i), column=5, columnspan=1, rowspan=1, padx=2, pady=2)

                i = i + 1

        except:
            print("Error")
    def enviar_prestamos(self, id , id_usuario, monto):
        capital = monto.get()
        result = self.servidorp.solicitar_prestamo(id, id_usuario, capital)
        self.top3.destroy()
    def enviar_ahorro(self, id , id_usuario, monto):
        capital = monto.get()
        result = self.servidorp.solicitar_ahorro(id, id_usuario, capital)
        self.top3.destroy()
    def editar_ahorro(self, id):

        self.top2 = Toplevel(self.ventana3)
        self.top2.geometry('650x200+20+20')
        self.top2.focus_set()
        self.top2.grab_set()
        self.top2.transient(master=self.ventana3)

        result = self.servidorp.obtener_producto(id)
        for registro in result:
            pcodigo = registro[0]
            pdescripcion = registro[1]
            ptasa = registro[2]
            ptiempo = registro[3]


        vpq = tk.LabelFrame(self.top2, width=450, height=50, relief='flat', borderwidth=4)
        vpq.grid(row=0, column=0, padx=10, pady=2)
        Label(vpq, text="Descripción:", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=0, columnspan=1, rowspan=1)
        descripcion = ttk.Entry(vpq)
        descripcion.insert(INSERT, pdescripcion)

        descripcion.grid(row=2, column=0, columnspan=1, rowspan=1)
        Label(vpq, text="Interes", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=1, columnspan=1, rowspan=1)
        tasa =ttk.Entry(vpq, textvariable=ptasa)
        tasa.insert(INSERT, ptasa)
        tasa.grid(row=2, column=1, columnspan=1, rowspan=1)
        Label(vpq, text="Tiempo", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=2, columnspan=1, rowspan=1)
        tiempo = ttk.Entry(vpq)
        tiempo.insert(INSERT, ptiempo)

        tiempo.grid(row=2, column=2, columnspan=1, rowspan=1)
        Button(vpq, text="Actualizar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda: self.grabar_ahorro(pcodigo, descripcion, tasa, tiempo)).grid(row=2, column=4, columnspan=1, rowspan=1)



    def editar_prestamo(self, id):

        self.top2 = Toplevel(self.ventana)
        self.top2.geometry('650x200+20+20')
        self.top2.focus_set()
        self.top2.grab_set()
        self.top2.transient(master=self.ventana)

        result = self.servidorp.obtener_producto(id)
        for registro in result:
            pcodigo = registro[0]
            pdescripcion = registro[1]
            ptasa = registro[2]
            ptiempo = registro[3]


        vpq = tk.LabelFrame(self.top2, width=450, height=50, relief='flat', borderwidth=4)
        vpq.grid(row=0, column=0, padx=10, pady=2)
        Label(vpq, text="Descripción:", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=0, columnspan=1, rowspan=1)
        descripcion = ttk.Entry(vpq)
        descripcion.insert(INSERT, pdescripcion)

        descripcion.grid(row=2, column=0, columnspan=1, rowspan=1)
        Label(vpq, text="Interes", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=1, columnspan=1, rowspan=1)
        tasa =ttk.Entry(vpq, textvariable=ptasa)
        tasa.insert(INSERT, ptasa)
        tasa.grid(row=2, column=1, columnspan=1, rowspan=1)
        Label(vpq, text="Tiempo", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=2, columnspan=1, rowspan=1)
        tiempo = ttk.Entry(vpq)
        tiempo.insert(INSERT, ptiempo)

        tiempo.grid(row=2, column=2, columnspan=1, rowspan=1)
        Button(vpq, text="Actualizar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda: self.grabar_prestamo(pcodigo, descripcion, tasa, tiempo)).grid(row=2, column=4, columnspan=1, rowspan=1)

    def insertar_ahorro(self, descripcion, tasa, tiempo):
        pdesc = descripcion.get()
        ptasa = tasa.get()
        ptiempo = tiempo.get()
        res = self.servidorp.insertar_ahorro(pdesc, ptasa, ptiempo)

        self.top.destroy()
    def insertar_prestramo(self, descripcion, tasa, tiempo):
         pdesc = descripcion.get()
         ptasa = tasa.get()
         ptiempo = tiempo.get()
         res = self.servidorp.insertar_prestamos(pdesc, ptasa, ptiempo)

         self.top.destroy()

    def grabar_prestamo(self, id, descripcion, tasa, tiempo):
        pdesc = descripcion.get()
        ptasa = tasa.get()
        ptiempo = tiempo.get()
        res = self.servidorp.actualizar_prestamos(id, pdesc, ptasa, ptiempo)

        self.top2.destroy()
        self.grid_prestamo()

    def grabar_ahorro(self, id, descripcion, tasa, tiempo):
        pdesc = descripcion.get()
        ptasa = tasa.get()
        ptiempo = tiempo.get()
        res = self.servidorp.actualizar_ahorro(id, pdesc, ptasa, ptiempo)

        self.top2.destroy()
        self.grid_ahorro()

    def listar_usuarios(self):


        result = self.servidorp.usuarios_listar()

        self.ventanausuarios = Tk()
        self.ventanausuarios.geometry("950x450+400+400")


        vu = tk.LabelFrame(self.ventanausuarios, width=550, height=100, relief='flat', borderwidth=4)
        vu.grid(row=0, column=0, padx=10, pady=2)

        Title = Label(vu, text='Tipo de Usuario', bg='DodgerBlue4', fg='white', width=16, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vu, text='Nombre', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vu, text='Apellido', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vu, text='Cedula', bg='DodgerBlue4', fg='white', width=16,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)

        Title4 = Label(vu, text='E-mail', bg='DodgerBlue4', fg='white', width=21,
                       font=('MS', 10, 'bold'))
        Title4.grid(row=0, column=4, columnspan=1, rowspan=1)



        vl = tk.LabelFrame(self.ventanausuarios, width=650, height=20, relief='flat', borderwidth=4)
        vl.grid(row=1, column=0, padx=10, pady=2)


        try:
            i = 1

            for registro in result:

                t_usuario = registro[7]

                if t_usuario == 2:
                    tipousuario = "Administrador"

                else:
                    tipousuario = "cliente"



                nombre = registro[4]
                apellido = registro[5]
                documento = registro[6]
                email = registro[1]


                # Imprimimos los resultados obtenidos

                Contenido = Label(vl, justify=LEFT, text="%s" % (tipousuario), bg='turquoise3', fg='white', width=15,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido1 = Label(vl, justify=LEFT, text="%s" % (nombre), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido2 = Label(vl, justify=LEFT, text="%s" % (apellido), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido3 = Label(vl, justify=LEFT, text="%s" % (documento), bg='turquoise3', fg='white', width=15,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1, padx=2, pady=2)

                Contenido4 = Label(vl, justify=LEFT, text="%s" % (email), bg='turquoise3', fg='white', width=20,
                                   font=('MS', 10, 'bold'))
                Contenido4.grid(row="%d" % (i), column=4, columnspan=1, rowspan=1, padx=2, pady=2)



                i = i + 1

        except:
            print ("Error")







def main():
    creavalores()
    ventana = Tk()
    app = Cliente(ventana)
    ventana.geometry("400x480+300+300")
    ventana.mainloop()

if __name__ == '__main__':
    main()