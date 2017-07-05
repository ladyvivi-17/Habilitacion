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
class Producto (object):

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

    def insertar_prestamos(self, descripcion, tasa, tiempo):

        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor
        sql = "INSERT INTO producto (descripcion, tasa_interes, tiempo, tipo) VALUES ('%s','%s','%s',0)" % (descripcion, tasa, tiempo)

        print (sql)
        cursor.execute(sql)
        conexion.commit()

    @Pyro4.expose
    def listar(self, tipo):
        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT * FROM producto WHERE tipo = %d" % (tipo)
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return resultados

    @Pyro4.expose
    def obtener_producto(self, id):
        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT * FROM producto WHERE id_producto = %d" % (id)
        print (sql)
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return resultados


    def actualizar_prestamos(self, id, descripcion, tasa, tiempo):

        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor
        sql = "UPDATE producto SET descripcion = '%s', tasa_interes = %s, tiempo = %s WHERE id_producto = %d " % (descripcion, tasa, tiempo, id)

        print (sql)
        cursor.execute(sql)
        conexion.commit()

    def solicitar_prestamo(self, id_producto, id_us, capital):

        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "INSERT INTO usuario_producto (id_usuario, id_producto, descripcion, tipo, valor_capital, cuotas_total, cuotas_pagas, cuotas_pend, valor_interes, valor_pagado, valor_pendiente, tasa_interes, fecha_inicio, fecha_fin, estado) SELECT %s as id_usuario,id_producto, descripcion, tipo, %s as valor_capital, tiempo as cuotas_total, 0 as cuotas_pagas, tiempo as cuotas_pend, tasa_interes/100 * %s * tiempo as valor_interes, 0 as valor_pagado, %s + (tasa_interes/100 * %s * tiempo) as valor_pendiente,tasa_interes, curdate() as fecha_inicio, date_add(curdate(), INTERVAL tiempo MONTH) as fecha_fin, 0 as estado from producto WHERE id_producto = %s" % (id_us, capital, capital, capital, capital, id_producto)
        print(sql)
        cursor.execute(sql)
        conexion.commit()

    @Pyro4.expose
    def estado_prestamo(self, id, tipo):
        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT * FROM usuario_producto WHERE id_usuario = %s AND tipo = %d" % (id, tipo)
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return resultados

    @Pyro4.expose
    def insertar_ahorro(self, descripcion, tasa, tiempo):

        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor
        sql = "INSERT INTO producto (descripcion, tasa_interes, tiempo, tipo) VALUES ('%s','%s','%s',1)" % (
        descripcion, tasa, tiempo)

        print(sql)
        cursor.execute(sql)
        conexion.commit()

    @Pyro4.expose
    def listar_ahorro(self, tipo):
        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT * FROM producto WHERE tipo = %d" % (tipo)
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return resultados

    @Pyro4.expose
    def actualizar_ahorro(self, id, descripcion, tasa, tiempo):

        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor
        sql = "UPDATE producto SET descripcion = '%s', tasa_interes = %s, tiempo = %s WHERE id_producto = %d " % (
        descripcion, tasa, tiempo, id)

        print(sql)
        cursor.execute(sql)
        conexion.commit()

    def solicitar_ahorro(self, id_producto, id_us, capital):

        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "INSERT INTO usuario_producto (id_usuario, id_producto, descripcion, tipo, valor_capital, cuotas_total, cuotas_pagas, cuotas_pend, valor_interes, valor_pagado, valor_pendiente, tasa_interes, fecha_inicio, fecha_fin, estado) SELECT %s as id_usuario,id_producto, descripcion, tipo, %s as valor_capital, tiempo as cuotas_total, 0 as cuotas_pagas, tiempo as cuotas_pend, tasa_interes/100 * %s * tiempo as valor_interes, 0 as valor_pagado, %s + (tasa_interes/100 * %s * tiempo) as valor_pendiente,tasa_interes, curdate() as fecha_inicio, date_add(curdate(), INTERVAL tiempo MONTH) as fecha_fin, 0 as estado from producto WHERE id_producto = %s" % (
        id_us, capital, capital, capital, capital, id_producto)
        print(sql)
        cursor.execute(sql)
        conexion.commit()

    @Pyro4.expose
    def estado_ahorro(self, id, tipo):
        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT * FROM usuario_producto WHERE id_usuario = %s AND tipo = %d" % (id, tipo)
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return resultados

    @Pyro4.expose
    def usuarios_listar(self):
        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT * FROM usuario"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return resultados








def main():
    demonio = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = demonio.register(Producto)
    ns.register("Leidy.Producto", uri)
    print ("estoy corriendo")
    demonio.requestLoop()


if __name__ == "__main__":
    main()
