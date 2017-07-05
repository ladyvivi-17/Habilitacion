#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import Pyro4
from bs4 import BeautifulSoup
import bs4 as bs
from requests import get
import json
import MySQLdb
etiquetas_imagenes= list()
import re, string
import mysql.connector


@Pyro4.expose
class Servidor(object):

    @Pyro4.expose

    def conexionbd(self):
        HOST = 'localhost'
        USER = 'root'
        PASSWORD = ''
        DATABASE = 'banco'
        conexion = (HOST, USER, PASSWORD, DATABASE)
        conn = MySQLdb.connect(*conexion)  # Conectar a la base de datos
        return conn

    @property
    def run_query(self, query):
        cursor = self.conexionbd()
        cursor.execute(query)  # Ejecutar una consulta
        if query.upper().startswith('SELECT'):
            data = self.cursor.fetchall()  # Traer los resultados de un select
        else:
            conn.commit()  # Hacer efectiva la escritura de datos
            data = None

        cursor.close()  # Cerrar el cursor
        conn.close()  # Cerrar la conexión
        return data


    @Pyro4.expose
    def login_usuario(self, email, clave):#login

        conexion= self.conexionbd()
        cursor = conexion.cursor()


        sql = "SELECT id_tipo FROM usuario WHERE login = '%s' AND clave = '%s'" % (email, clave)
        cursor.execute(sql)  # Ejecutar una consulta

        result = cursor.fetchall()

        if result:
            for registro in result:
                datos = registro[0]


        else:
            datos = 0

        return datos


    def obtener_idus(self, email, clave):# obtener id_usuario

        conexion= self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT id_usuario FROM usuario WHERE login  = '%s' AND clave = '%s'" % (email, clave)
        cursor.execute(sql)  # Ejecutar una consulta
        result = cursor.fetchall()
        if result:
            for registro in result:
                datos = registro[0]


        else:
            datos = 0


        return datos


    def login_register(self, nombre, apellido, id, clave, email, cedula): #insertar registros de usuario

        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor

        sql = "INSERT INTO usuario (nombre, apellido, clave, id_tipo, login, fecha_reg, cedula ) VALUES ('%s','%s','%s',%d,'%s',curdate(),'%s')" % (nombre, apellido, clave, id, email, cedula)

        cursor.execute(sql)
        conexion.commit()
        result = cursor.fetchall()

        if result:
            for registro in result:
                datos = registro[0]

        else:
            datos = 0

        self.log(email, 3, '192.168.0.101')
        return datos


    def obtener_cliente(self, id_us):
        conexion = self.conexionbd()
        cursor = conexion.cursor()

        sql = "SELECT cedula, nombre, apellido, telefono, direccion FROM usuario WHERE id_usuario = '%s'" % (id_us)

        print (sql)
        cursor.execute(sql)  # Ejecutar una consulta

        result = cursor.fetchall()

        return result

    def log(self, login, id_event, ip):

        if id_event == 1:
            event = 'Inicio de Sección'
        if id_event == 2:
            event = 'Cerrar Sección'
        if id_event == 3:
            event = 'Crear cuenta'
        if id_event == 4:
            event = 'login fallido'

        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "INSERT INTO log (fecha_hora, login, ip, evento) VALUES(curdate(),'%s','%s','%s')" % (login, ip, event)
        print(sql)
        cursor.execute(sql)
        conexion.commit()

    def listar_log(self):
        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT * FROM log"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return resultados




def main():
    demonio = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = demonio.register(Servidor)
    ns.register("Leidy.Cristian", uri)
    print ("estoy corriendo")
    demonio.requestLoop()


if __name__ == "__main__":
    main()
