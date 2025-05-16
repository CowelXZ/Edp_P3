import sys
from PyQt5 import QtWidgets, uic, QtCore
import serial

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Departamental.ui", self)  # Carga el archivo .ui

        self.txt_com.setText("COM4")

        # Variables para Arduino y control
        self.arduino = None
        self.datos = []
        self.bandera = 0

        # Umbral inicial
        self.umbral = 500
        self.lbl_umbral.setText(f"Umbral Actual: {self.umbral}")

        # Timer para lecturas del Arduino
        self.segundoPlano = QtCore.QTimer()
        self.segundoPlano.timeout.connect(self.lecturas)

        # Conexiones botones
        self.btn_accion.clicked.connect(self.accion)
        #self.btn_control.clicked.connect(self.control)

        # Conexión slider vertical
        self.slider_umbral.valueChanged.connect(self.cambiar_umbral_desde_slider)

    def accion(self):
        texto = self.btn_accion.text()
        com = self.txt_com.text()

        try:
            if texto == "CONECTAR":
                self.arduino = serial.Serial(com, baudrate=9600, timeout=1)
                self.segundoPlano.start(100)
                self.btn_accion.setText("DESCONECTAR")
                self.txt_estado.setText("CONECTADO")
            elif texto == "DESCONECTAR":
                if self.arduino and self.arduino.isOpen():
                    self.segundoPlano.stop()
                    self.arduino.close()
                self.btn_accion.setText("RECONECTAR")
                self.txt_estado.setText("DESCONECTADO")
            elif texto == "RECONECTAR":
                if self.arduino and not self.arduino.isOpen():
                    self.arduino.open()
                    self.segundoPlano.start(100)
                    self.btn_accion.setText("DESCONECTAR")
                    self.txt_estado.setText("RECONECTADO")
        except Exception as e:
            print(f"Error en la conexión: {e}")

    def control(self):
        texto = self.btn_control.text()
        if self.arduino and self.arduino.isOpen():
            if texto == "PRENDER":
                self.btn_control.setText("APAGAR")
                self.arduino.write("1".encode())
            else:
                self.btn_control.setText("PRENDER")
                self.arduino.write("0".encode())

    def lecturas(self):
        if self.arduino and self.arduino.isOpen():
            if self.arduino.inWaiting():
                cadena = self.arduino.readline().decode().strip()
                if cadena:
                    self.datos.append(cadena)
                    if self.bandera == 0:
                        cadena_split = cadena.split("-")
                        if len(cadena_split) >= 3:
                            valores = cadena_split[:-1]
                            try:
                                valor_ldr = int(cadena_split[0])
                                estado_luz = cadena_split[1]
                                estado_led = int(cadena_split[2])

                                # Puedes imprimirlo o usarlo en etiquetas:
                                print(
                                    f"LDR: {valor_ldr}, Luz: {estado_luz}, LED: {'Encendido' if estado_led else 'Apagado'}")


                            except Exception as e:
                                print(f"Error al convertir valores: {e}")

    def cambiar_umbral_desde_slider(self):
        self.umbral = self.slider_umbral.value()
        self.lbl_umbral.setText(f"Umbral Actual: {self.umbral}")
        if self.arduino and self.arduino.isOpen():
            comando = f"UMBRAL:{self.umbral}\n"
            self.arduino.write(comando.encode())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = MyApp()
    ventana.show()
    sys.exit(app.exec_())
