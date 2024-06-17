import random
from enum import Enum
import json
import numpy as np
from GCMixto import GenCongruencialMixto as gcm


def ControlarYSeleccionarCarga(camion, rechazada, peso, datos_camiones, dia):
  semilla = random.randint(1, 10)
  gcmClase = gcm()
  gcmClase.semilla = semilla

  cont = 0
  #Tipo de Chatarra
  tch = {'Chatarra': ['LISTA', 'OXICORTE', 'PRENSA']}  #Tipo de Chatarra
  b = {'Estado': ['ACEPTADA', 'REQUIERE_LIMPIEZA']}  #Estado de la Chatarra

  num = gcmClase.U_i()

  if num <= 0.1:
    mensaje = f"""
      Informe de Carga
      Camion N° {camion}
      Carga DESCARTADA
    """
    print(mensaje)
    rechazada += 1
    peso = 0
    return camion, rechazada, peso
  else:
    if num <= 0.8:
      est = b['Estado'][1]
      num = gcmClase.U_i()
      cont = 5 + 10 * num
    else:
      est = b['Estado'][0]
      num = gcmClase.U_i()
      cont = 0 + 5 * num
    num = gcmClase.U_i()
    if num <= 0.189:
      tipo_carga = tch['Chatarra'][0]
      peso = 0.05 + 0.15 * num
    elif num <= 0.578:
      tipo_carga = tch['Chatarra'][1]
      num = gcmClase.U_i()
      peso = 1 + 9 * num
    else:
      tipo_carga = tch['Chatarra'][2]
      num = gcmClase.U_i()
      peso = 0.5 + 2.5 * num

    mensaje = f"""
      Informe de Carga
      Camion N° {camion}
      Tipo de Carga: {tipo_carga}
      Esatdo de Carga {est}
      Impurezas Presentes Visibles: {cont}
      Peso de la Carga: {peso}
    """

    data = {
            "camion": camion,
            "tipo_carga": tipo_carga,
            "estado": est,
            "impurezas": cont,
            "peso": peso
        }

    if dia not in datos_camiones: 
            datos_camiones[dia] = []
    datos_camiones[dia].append(data)

    print(mensaje)
    return camion, rechazada, peso


def DefinirPresentacion(pca, lbr, lro, so):
  semilla = random.randint(1, 10)
  gcmClase = gcm()
  gcmClase.semilla = semilla

  so = so + pca
  num = gcmClase.U_i()

  if num <= 0.67:
    while so >= 1:
      num = gcmClase.U_i()
      plob = (1000 + 1000 * num) / 1000
      if so >= plob:
        so = so - plob
        lbr += 1
      else:
        break
  else:
    while so >= 1.5:
      plor = (np.random.normal(1500, 10)) / 1000
      if so >= plor:
        so = so - plor
        lro += 1
      else:
        break

  return pca, lbr, lro, so

#def CargarDatos(ce = 60, oa = 420000):
 # return ce, oa

def main(ce, oa):
  semilla = random.randint(1, 10)
  gcmClase = gcm()
  gcmClase.semilla = semilla

  dia = 1
  ta = 0  #Total Acero
  c = 0  #Camion N°x
  #ce = 60 #Entrada de Camiones
  pca = 0  #Peso de la Carga
  ptca = 0  #Peso Total de Chatarra Diaria
  tar = 0  #Total Acero Reciclado
  pcial = 0  #Porcentaje de Contaminante en Carga
  ccc = 0  #Cantidad de Contaminante de Carga
  cal = Enum('Acero', ['A440', 'A560', 'A630'])  #Calidad de Acero
  cacc = 0  #Cantida de Acero A440 Producido
  caqs = 0  #Cantida de Acero A560 Producido
  cast = 0  #Cantida de Acero A630 Producido
  so = 0  #Sobrante de Acero
  tc = 0  #Total Camiones
  lbr = 0  #Cantidad de Lotes de Barras Rectas
  plbr = 0  #Peso de Lotes de Barras Rectas
  lro = 0  #Cantidad de Lotes Rollos
  plro = 0  #Peso de Lotes Rollos
  #oa = 42000  #Objetivo Toneladas a Reciclar
  rech = 0  #Carga Rechazada en el dia
  #objCump = Enum('Objetivo',['OBJETIVO_CUMPLIDO','NO_SE_LOGRO_EL_OBJETIVO']) #Objetivo Cumplido
  objCump = ""
  pb = Enum('Barras', ['SI', 'NO'])  #Produccion de Barras?

  datos_camiones = {}

  while dia <= 30:
    #ce, oa = CargarDatos(ce,oa)
    tc = np.random.poisson(ce)
    c = 0
    rech = 0

    while c < tc:

      c, rech, pca = ControlarYSeleccionarCarga(c, rech, pca, datos_camiones, dia)

      if pca != 0:
        ptca = ptca + pca
        num = gcmClase.U_i()

        if num <= 0.48:
          cal = cal.A440
          num = gcmClase.U_i()
          cacc = cacc + pca
          ta = ta + cacc
          tar = tar + (cacc * 0.9)
        elif num <= 0.82:
          cal = cal.A560
          num = gcmClase.U_i()
          pcial = 0.4 + 0.8 * num
          caqs = caqs + pca
          ta = ta + caqs
          tar = tar + (caqs * 0.9)
        else:
          cal = cal.A630
          num = gcmClase.U_i()
          pcial = 0 + 0.4 * num
          cast = cast + pca
          ta = ta + cast
          tar = tar + (cast * 0.9)

        mensaje = f"""
          Calidad Final del Acero: {cal}
          Porcentaje de Contaminante Final Detectado en Acero: {pcial}
        """
        print(mensaje)
      num = gcmClase.U_i()

      if num <= 0.2:
        print("Se Producen Barras de Acero")
        pca, lbr, lro, so = DefinirPresentacion(pca, lbr, lro, so)
      else:
        print("Se producen Barras de Refuerzo")

      c += 1

    print(f"Carga Rechazada en el Dia {dia}: {rech}")
    dia += 1

  objCump = "Objetivo Cumplido!" if ta >= oa else "No se logro el objetivo"

  mensaje = f"""
    Informe Mensual

    {objCump}
    
    Total Acero Procesado: {ta}
    Total Acero Reciclado Producido: {tar}
    Total Acero A440 Producido: {cacc}
    Total Acero A560 Producido: {caqs}
    Total Acero A630 Producido: {cast}
    Total Lotes de Barras Rectas Producidos: {lbr}
    Total Lotes de Rollos Producidos: {lro}
  """
  informeMensual = {
            "objetivo": objCump,
            "total_acero_procesado": round(ta,2),
            "total_acero_reciclado_producido": round(tar,2),
            "total_acero_A440_producido": round(cacc,2),
            "total_acero_A560_producido": round(caqs,2),
            "total_acero_A630_producido": round(cast,2),
            "total_lotes_de_barras_rectas": lbr,
            "total_lotes_de_rollos": lro
        }

  print(mensaje)

  jsonFinal = {
    "Dias": datos_camiones,
    "Mes": informeMensual
  }

  with open('informe_camiones.json', 'w') as outfile:
        informe_camiones = json.dump(jsonFinal, outfile, indent=4)
  
  return jsonFinal

if __name__ == '__main__':
  ce = 60
  oa = 420000 
  main(ce,oa)
