import socket, os, json
from pathlib import Path
from subprocess import run as subproceso, Popen as asíncrono, PIPE as tubería
from typing import Any


def notificación(cuerpo: str, ícono: str = '', título: str = 'Notificación', urgencia: str = 'normal', aplicación: str = '') -> None:
	"""
	Plantilla base para enviar notificaciones en Linux. Si se usa repetidas veces a lo largo de una aplicación, puede envolverse en otra función para definir los parámetros repetitivos.
	"""
	comando = ['notify-send', título, cuerpo]

	comando += ['-h', f'string:desktop-entry:{aplicación}']
	comando += ['-i', ícono]
	comando += ['-u', urgencia]

	subproceso(comando)

def comprobar_conexión_a_internet(host: str = "8.8.8.8", port: int = 53, timeout: int = 3) -> bool:
	"""
	Intenta conectar a un puerto común para verificar si hay internet. Usa el puerto 53 (DNS) de Google por ser ultra-rápido y estable.
	"""
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except OSError:
		return False

def pipas(*args: list[str] | str) -> None:
	"""
	Ejecuta comandos en pipas en la forma recomendada.
	"""
	proceso: asíncrono | None = None
	for comando in args:
		if isinstance(comando, str):
			comando = comando.split()

		if proceso is None:
			proceso = asíncrono(comando, stdout = tubería)
		else:
			proceso = asíncrono(comando, stdin = proceso.stdout)

def reemplazar_string(plantilla: Any, reemplazos: dict[str, str]) -> Any:
	"""
	Esta función emula f-strings que pueden guardarse en archivos de configuración de texto plano. Usa tags entre corchetes en la variable string "plantilla" y el tag debe tener el mismo nombre que la llave el "reemplazos".

	"Plantilla" también puede ser una tupla, un diccionario o una lista, ya que revisa en cada uno de sus elementos por strings a los que aplicar el cambio.

	Los elementos que no sean de los tipos mencionados antes los devuelve tal cual.
	"""
	if isinstance(plantilla, tuple):
		plantilla = [reemplazar_string(elemento, reemplazos) for elemento in plantilla]
		plantilla = tuple(plantilla)
	elif isinstance(plantilla, dict):
		plantilla = {
			llave: reemplazar_string(elemento, reemplazos) for llave, elemento in plantilla.items()
		}
	elif isinstance(plantilla, list):
		plantilla = [
			reemplazar_string(elemento, reemplazos) for elemento in plantilla
		]
	elif isinstance(plantilla, str):
		for llave, valor in reemplazos.items():
			if isinstance(valor, str):
				plantilla = plantilla.replace(f'[{llave}]', valor)
	
	return plantilla

def serializador(objeto: Any) -> Any:
	if isinstance(objeto, tuple):
		objeto = {
			'tipo': 'tupla',
			'objetos': [serializador(elemento) for elemento in objeto]
		}
	elif isinstance(objeto, dict):
		objeto = {
			llave: serializador(elemento) for llave, elemento in objeto.items()
		}
	elif isinstance(objeto, list):
		objeto = [
			serializador(elemento) for elemento in objeto
		]
	elif hasattr(objeto, 'serializador'):
		objeto = objeto.serializador()
	
	return objeto

def deserializador(objeto: Any) -> Any:
	if isinstance(objeto, dict):
		if objeto.get('tipo') == 'tupla':
			objeto = tuple(objeto['objetos'])
	elif hasattr(objeto, 'deserializador'):
		objeto = objeto.deserializador()
		
	return objeto

def abrir_json(ruta: str) -> dict[str, Any]:
	if not os.path.exists(ruta):
		print('Archivo no proporcionado, creando uno.')
		return {}

	with open(ruta, 'r', encoding = 'utf-8') as archivo:
		return json.load(archivo, object_hook = deserializador)

def guardar_json(ruta: str, data: dict[str, Any]) -> None:
	data = serializador(data)

	with open(ruta, 'w', encoding = 'utf-8') as archivo:
		json.dump(data, archivo, indent = 4, ensure_ascii = False)

def listado_de_archivos(ruta: str) -> list[str]:
	return [f.name for f in Path(ruta).iterdir() if f.is_file()]