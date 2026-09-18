# pyright: reportMissingImports = false, reportMissingModuleSource = false, reportAttributeAccessIssue = false, reportUndefinedVariable = false

from platform import system
from typing import Any
from PyQt6.QtCore import Qt

from lib_widget_base_pyqt import WidgetMaestro


class LVentana(WidgetMaestro):
	def initCV(self, *args: Any, **kwargs: Any) -> None:
		super().initCV(*args, **kwargs)
		self.título: str = self.__class__.__name__
		self.os: str = system()
		self.es_subventana: bool = kwargs.get('subventana', False)
		self.es_widget: bool = kwargs.get('es_widget', False)

	def initPP(self, *args, **kwargs) -> None:
		super().initPP(*args, **kwargs)
		self.configurar_nombre(self.título)
		self.configuración_base('Linux')
		self.show()
		self.configuración_base('Windows')

	def configuración_base(self, sistema_operativo: str) -> None:
		if not self.es_widget:
			return
		
		self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

		if sistema_operativo == self.os == 'Windows':
			import win23gui, win32con # TO_DO: Revisar y debuggear para Windows.
			from ctypes import windll

			win32gui.SetWindowPos(self.winId(), win32con.HWND_BOTTOM, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
			hwnd: Any = win32gui.GetWindow(win32gui.GetWindow(windll.user32.GetTopWindow(0), win32con.GW_HWNDLAST), win32con.GW_CHILD)
			win32gui.SetWindowLong(self.winId(), win32con.GWL_HWNDPARENT, hwnd)

		elif sistema_operativo == self.os == 'Linux':
			if not self.es_subventana:
				self.setWindowFlag(Qt.WindowType.Tool)
			self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
			self.setAttribute(Qt.WidgetAttribute.WA_X11DoNotAcceptFocus, True)

	def configurar_nombre(self, nombre: str) -> None:
		self.setWindowTitle(nombre)