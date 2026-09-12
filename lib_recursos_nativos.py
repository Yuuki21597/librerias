from subprocess import run as subproceso, Popen as asíncrono, PIPE as tubería

def notificación(cuerpo: str, ícono: str = '', título: str = 'Notificación', urgencia: str = 'normal', aplicación: str = '') -> None:
	"""
	Plantilla base para enviar notificaciones en Linux. Si se usa repetidas veces a lo largo de una aplicación, puede envolverse en otra función para definir los parámetros repetitivos.
	"""
	comando = ['notify-send', título, cuerpo]

	comando += ['-h', f'string:desktop-entry:{aplicación}']
	comando += ['-i', ícono]
	comando += ['-u', urgencia]

	subproceso(comando)

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