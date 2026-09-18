# pyright: reportIncompatibleMethodOverride = false

from typing import Any
from PyQt6.QtWidgets import QVBoxLayout, QFormLayout, QHBoxLayout, QFileDialog, QWidget, QLineEdit, QPushButton, QLabel, QDialog, QDialogButtonBox, QLayout, QWidgetItem
from PyQt6.QtCore import QRect, QSize

from lib_widget_base_pyqt import WidgetMaestro


class QDefLayout(QLayout):
	"""
	Q Defined Layout: Crea un organizador en un espacio definido.
	"""
	def __init__(self, superior: QWidget | None = None, medidas: list[tuple[int, ...]] | None = None, tipo_de_ajuste: list[tuple[str, str]] | None = None, escala_global: int = 1, márgenes: list[int] | None = None, espaciado = 0) -> None:
		kwargs: dict[str, Any] = locals()
		del kwargs['self']
		del kwargs['__class__']
		args: list[Any] = []

		super().__init__(
			parent = (
				kwargs.get(
					'superior',
					kwargs.get('parent', None)
				)
			)
		)
		self.initCV(*args, **kwargs)
		self.initUI(*args, **kwargs)
		self.initPP(*args, **kwargs)

	def initCV(self, *args: Any, **kwargs: Any) -> None:
		self.superior: QWidget | None = kwargs.get('superior')
		self.medidas: list[tuple[int, ...]] | None = kwargs.get('medidas')
		self.tipo_de_ajuste: list[tuple[str, str]] | None = kwargs.get('tipo de ajuste')
		self.escala_global: int = kwargs.get('escala_global', 1)

		if not self.medidas:
			valor_x: int = 0
			valor_y: int = 0
			if self.superior is not None:
				valor_x = self.superior.size().width()
				valor_y = self.superior.size().height()

			self.medidas = [(0, 0, valor_x, valor_y)]

		if not self.tipo_de_ajuste:
			self.tipo_de_ajuste = []
			for x in range(len(self.medidas)):
				ajuste: tuple[str, str] = ('ninguno', 'ninguno')
				self.tipo_de_ajuste.append(ajuste)

	def initUI(self, *args: Any, **kwargs: Any) -> None:
		self.márgenes = kwargs.get('márgenes') or [0, 0, 0, 0]
		espaciado = kwargs.get('espaciado', 0)
		self.setSpacing(espaciado)
		
		self.lista_de_objetos: list[QWidget] = []

	def initPP(self, *args: Any, **kwargs: Any) -> None:
		pass

	def addItem(self, objeto: Any) -> None:
		self.lista_de_objetos.append(objeto)

	def count(self) -> int:
		return len(self.lista_de_objetos)

	def comprobación(self, índice: int) -> bool:
		if índice > ((self.count() - 1) * -1) and índice < self.count():
			return True

		return False

	def itemAt(self, índice: int) -> QWidget | None:
		if self.comprobación(índice):	
			return self.lista_de_objetos[índice]

		return None

	def takeAt(self, índice: int) -> QWidget | None:
		if self.comprobación(índice):
			return self.lista_de_objetos.pop(índice)

		return None

	def setGeometry(self, área: QRect) -> None:
		super().setGeometry(área)
		if (self.medidas is None) or (self.tipo_de_ajuste is None):
			raise RuntimeError('self.medidas o self.tipo de ajuste es None. Esto no debe ser posible.')

		área_x: int = int(self.medidas[0][0] * self.escala_global) + self.márgenes[0]
		área_y: int = int(self.medidas[0][1] * self.escala_global) + self.márgenes[1]
		área_ancho: int = int(self.medidas[0][2] * self.escala_global) - self.márgenes[2]
		área_alto: int = int(self.medidas[0][3] * self.escala_global) - self.márgenes[3]
		área = QRect(área_x, área_y, área_ancho, área_alto)

		áreas_restringidas: list[QRect] = []
		for indice, tupla in enumerate(self.medidas):
			if indice != 0:
				área_res_x = int(tupla[0] * self.escala_global)
				área_res_y = int(tupla[1] * self.escala_global)
				área_res_ancho = int((tupla[2] - tupla[0]) * self.escala_global)
				área_res_alto = int((tupla[2] - tupla[0]) * self.escala_global)

				áreas_restringidas.append(
					QRect(área_res_x, área_res_y, área_res_ancho, área_res_alto)
				)

		for elemento in self.lista_de_objetos:
			if not isinstance(elemento, QWidgetItem): continue
			widget = elemento.widget()

			if not isinstance(widget, QWidget):
				raise TypeError('El elemento que se intenta asignar no es subsintancia de la clase QWidget.')
			tamaño: QSize = widget.sizeHint()

			ancho: int = min(tamaño.width(), área_ancho)
			alto: int = min(tamaño.height(), área_alto)

			nuevo_x: int = área_x + ((área_ancho - área_x - ancho) // 2)
			nuevo_y: int = área_y

			espacio: QRect = QRect(nuevo_x, nuevo_y, ancho, alto)

			for índice, área_restringida in enumerate(áreas_restringidas):
				if espacio.intersects(área_restringida):
					recorte: QRect = espacio.intersected(área_restringida)
					if self.tipo_de_ajuste[índice][0] == 'restar':
						nuevo_x -= recorte.width()
					if self.tipo_de_ajuste[índice][0] == 'sumar':
						nuevo_x += recorte.width()

					if self.tipo_de_ajuste[índice][1] == 'restar':
						nuevo_y -= recorte.width()
					if self.tipo_de_ajuste[índice][1] == 'sumar':
						nuevo_y += recorte.width()

			ancho = ancho if (ancho + nuevo_x) < área_ancho else (área_ancho - nuevo_x)
			alto = alto if (alto + nuevo_y) < área_alto else (área_alto - nuevo_y)

			espacio = QRect(nuevo_x, nuevo_y, ancho, alto)
			widget.setGeometry(espacio)
			área_y = min(área_alto, nuevo_y + tamaño.height() + self.spacing())


def crearOrganizador(tipo: str = 'Horizontal', márgenes: list[int] | int | None = None, espaciado: int | tuple[int, int] = 0, *args, **kwargs) -> QVBoxLayout | QFormLayout | QHBoxLayout | QDefLayout:
	"""
	Crea y da formato a un organizador —mejor conocido como: layout—.
	"""
	organizador: QVBoxLayout | QFormLayout | QHBoxLayout | QDefLayout
	if tipo == 'Vertical':
		organizador = QVBoxLayout()
	elif tipo == 'Formulario':
		organizador = QFormLayout()
	elif tipo == 'Definido':
		organizador = QDefLayout(*args, **kwargs)
	else:
		organizador = QHBoxLayout()

	márgenes_finales: list[int]
	if márgenes is None:
		márgenes_finales = [0] * 4
	elif isinstance(márgenes, int):
		márgenes_finales = [márgenes] * 4
	else:
		márgenes_finales = márgenes

	organizador.setContentsMargins(*márgenes_finales)

	if isinstance(organizador, QFormLayout) and isinstance(espaciado, tuple):
		organizador.setHorizontalSpacing(espaciado[0])
		organizador.setVerticalSpacing(espaciado[1])
	elif isinstance(espaciado, int):
		organizador.setSpacing(espaciado)

	return organizador

def crearEtiqueta(texto: str, fuente: str, tamaño: int, color: str = 'black', superior: QWidget | None = None) -> QLabel:
	etiqueta: QLabel = QLabel(texto, superior)
	etiqueta.setStyleSheet(
		f'color: {color};'
		f"font: {tamaño}px {fuente}"
	)

	return etiqueta


class Selector(WidgetMaestro):
	def initCV(self, *args: Any, **kwargs: Any) -> None:
		super().initCV(*args, **kwargs)
		self.tipo = kwargs.get('tipo') or 'archivos'
		self.filtros = kwargs.get('filtros', '')
	
	def initUI(self, *args: Any, **kwargs: Any) -> None:
		self.organizador = crearOrganizador()
		self.setLayout(self.organizador)

		self.linea_de_texto: QLineEdit = QLineEdit(self)
		self.boton: QPushButton = QPushButton("...", self)
		self.boton.setFixedWidth(30)
		
		self.organizador.addWidget(self.linea_de_texto)
		self.organizador.addWidget(self.boton)

		self.boton.clicked.connect(self.seleccionar)

	def initPP(self, *args: Any, **kwargs: Any) -> None:
		ruta: str = kwargs.get('ruta') or ''

		if ruta.strip():
			self.setText(ruta)

	def seleccionar(self) -> None:
		mensaje: str = "Selecciona un elemento"
		selección: str | tuple[str, str]

		if self.tipo == 'archivos':
			selección = QFileDialog.getOpenFileName(self, mensaje, filter = self.filtros)
		else:
			selección = QFileDialog.getExistingDirectory(self, mensaje)

		if isinstance(selección, tuple):
			selección = selección[0]

		self.initPP(ruta = selección)
	
	def text(self) -> str:
		return self.linea_de_texto.text()
	
	def setText(self, texto) -> None:
		self.linea_de_texto.setText(texto)


class FormularioBase(QDialog):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(
					parent = kwargs.get(
						'superior',
						kwargs.get('parent', None)
					)
				)
		self.initCV(*args, **kwargs)
		self.initUI(*args, **kwargs)
		self.initPP(*args, **kwargs)

	def initCV(self, *args, **kwargs) -> None:
		self.superior: QWidget | WidgetMaestro | None = kwargs.get('superior', None)
		self.vista_previa: QLabel

	def initUI(self, *args, **kwargs) -> None:
		self.organizador = crearOrganizador('Vertical', márgenes = 10)
		self.organizador_2 = crearOrganizador('Formulario', espaciado = (10, 0))

		if not isinstance(self.organizador, QVBoxLayout) or not isinstance(self.organizador_2, QFormLayout):
			raise RuntimeError('Algún organizador del reloj es de clase incorrecta.')

		self.setLayout(self.organizador)
		self.organizador.addLayout(self.organizador_2)

		self.interfaz_de_subinstancias()

		self.botones: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
		self.botones.accepted.connect(self.aceptar)
		self.botones.rejected.connect(self.cancelar)
		self.botones.setCenterButtons(True)

		self.organizador.addWidget(self.botones)

		self.configurar_campos(self.organizador_2, *args, **kwargs)

	def initPP(self, *args, **kwargs) -> None:
		self.setWindowTitle('Formulario')

	def interfaz_de_subinstancias(self) -> None:
		pass

	def configurar_campos(self, organizador, *args, **kwargs) -> None:
		pass

	def aceptar(self) -> None:
		self.close()

	def cancelar(self) -> None:
		self.close()


class FormularioUniCampo(FormularioBase):
	def configurar_campos(self, organizador, *args, **kwargs) -> None:
		self.campos: dict[str, Any] = {
			'Selector': Selector(self, tipo = kwargs.get('tipo', ''), filtros = kwargs.get('filtros', ''))
		}

		for nombre, campo in self.campos.items():
			organizador.addRow(nombre, campo)

	def text(self) -> str:
		return self.campos['Selector'].text()

	def aceptar(self) -> None:
		self.campos['Selector'].initPP()
		super().aceptar()