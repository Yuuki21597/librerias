from typing import Any
from PyQt6.QtWidgets import QWidget


class WidgetMaestro(QWidget):
	def __init__(self, *args: Any, **kwargs: Any) -> None:
		super().__init__(
			parent = (
				kwargs.get(
					'superior',
					kwargs.get('parent')
				)
			)
		)
		self.initCV(*args, **kwargs)
		self.initUI(*args, **kwargs)
		self.initPP(*args, **kwargs)

	def initCV(self, *args: Any, **kwargs: Any) -> None:
		"""
		Mejor conocido como "initialize Class Variables".
		"""
		self.superior: QWidget | None = kwargs.get('superior')

	def initUI(self, *args: Any, **kwargs: Any) -> None:
		"""
		Mejor conocido como "initialize User Interface".
		"""
		pass

	def initPP(self, *args: Any, **kwargs: Any) -> None:
		"""
		Mejor conocido como "initialize Post Process". Esta función es para trabajar con valores que se crean tras ejecutarse initUI.
		"""
		pass