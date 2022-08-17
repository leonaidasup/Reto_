import webbrowser
from Extract import extract, Steam, Insta
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QAbstractAnimation
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QDialog, QComboBox, QGraphicsBlurEffect, QPlainTextEdit

class Boton(QPushButton):
    def __init__(self,parent=None):
        QPushButton.__init__(self, parent)        
        self.setMouseTracking(True)
        self.setStyleSheet('border-width: 20; border-radius: 10; background-color: #3D403F; border: none; color: #FFFFFF')
        self.fuente = self.font()
        self.posicionX = int
        self.posicionY = int

    def enterEvent(self, event):
        self.posicionX = self.pos().x()
        self.posicionY = self.pos().y()
        self.animacionCursor = QPropertyAnimation(self, b"geometry")
        self.animacionCursor.setDuration(100)
        self.animacionCursor.setEndValue(QRect(self.posicionX-11, self.posicionY-4, 121, 40))
        self.animacionCursor.start(QAbstractAnimation.DeleteWhenStopped)        
        self.fuente.setPointSize(15)
        self.setFont(self.fuente)

    def leaveEvent(self, event):
        self.fuente.setPointSize(13)
        self.setFont(self.fuente)        
        self.animacionNoCursor = QPropertyAnimation(self, b"geometry")
        self.animacionNoCursor.setDuration(100)
        self.animacionNoCursor.setEndValue(QRect(self.posicionX, self.posicionY, 100, 30))
        self.animacionNoCursor.start(QAbstractAnimation.DeleteWhenStopped)
    
# ================================================================

class Reto(QDialog):
    def __init__(self, parent=None):
        super(Reto, self).__init__(parent) 
        self.setWindowTitle("Reto")      
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(888,576)

        self.t_titulo,self.t_descripcion,self.t_fecha,self.t_precio,self.t_desarrollador,self.t_distribuidor,self.t_link,self.t_posicion=extract()
        self.historial = [[self.t_posicion, self.t_link]]
        self.estado = 0
        self.init()

    def init(self):
        fuente = QFont()
        fuente.setFamily("Bahnschrift")

        #fondo
        fondo = QLabel(self)
        fondo.setStyleSheet('background-color: #242424')
        fondo.setGeometry(0, 240, 888, 336)      

        #Imagen fondo
        self.imagen_fondo = QLabel(self)
        img = QPixmap('image.png')
        self.imagen_fondo.setPixmap(img.scaled(888, 428))
        self.imagen_fondo.setGeometry(0, 0, 888, 240)
        self.blur_effect = QGraphicsBlurEffect()   
        self.blur_effect.setBlurRadius(15)      
        self.imagen_fondo.setGraphicsEffect(self.blur_effect) 
        
        #Imagen
        self.imagen = QLabel(self)
        self.imagen.setPixmap(img)
        self.imagen.setGeometry(30, 150, 460, 215)
        borde = QLabel(self)
        borde.setStyleSheet("border-color: #242424; border-width: 10; border-radius: 20; border-style : solid")
        borde.setGeometry(24, 144, 472, 227)

        #Titulo
        self.titulo = QLabel(self.t_titulo,self)
        self.titulo.setStyleSheet("color: #FFFFFF")
        self.titulo.setGeometry(30, 371, 477, 40)
        fuente.setPointSize(19)
        self.titulo.setFont(fuente)  
        
        #Boton anterior
        self.anterior = Boton(self)
        self.anterior.setText("Anterior")
        self.anterior.setCursor(Qt.PointingHandCursor)
        self.anterior.setAutoDefault(False)
        self.anterior.setGeometry(517, 250, 100, 30)
        self.anterior.clicked.connect(self.Anterior_)

        #Boton nuevo
        self.nuevo = Boton(self)
        self.nuevo.setText("Nuevo")
        self.nuevo.setCursor(Qt.PointingHandCursor)
        self.nuevo.setAutoDefault(False)
        self.nuevo.setGeometry(640, 250, 100, 30)
        self.nuevo.clicked.connect(self.Nuevo_)

        #Boton suguiente
        self.anterior = Boton(self)
        self.anterior.setText("Siguiente")
        self.anterior.setCursor(Qt.PointingHandCursor)
        self.anterior.setAutoDefault(False)
        self.anterior.setGeometry(763, 250, 100, 30)
        self.anterior.clicked.connect(self.Siguiente_)
  
        #Menu
        self.Genero = QComboBox(self)
        self.Genero.addItems(['Todos',"Acción", "Aventura", "Fps", "Arcade", "Indie", "Un jugador", "Rpg", "Estrategia"])
        self.Genero.setStyleSheet("QComboBox::!on:hover{background-color: lightgreen;}")
        fuente.setPointSize(11)
        fuente.setFamily("Bahnschrift")
        self.Genero.setFont(fuente)
        self.Genero.setStyleSheet('border-width: 10; border-radius: 10;background-color: #3D403F; color: #FFFFFF')
        self.Genero.setGeometry(763, 20, 100, 30)
        
        #Descripcion
        self.descripcion = QPlainTextEdit(self)
        self.descripcion.insertPlainText(self.t_descripcion)
        self.descripcion.setReadOnly(True)
        self.descripcion.setStyleSheet('border: none;background-color: #242424; color: #C0C0C0')
        self.descripcion.setLayoutDirection(Qt.RightToLeft)
        self.descripcion.setGeometry(517, 290, 361, 266)
        
        #fecha_desarrollador_distribuidor
        Datos = QLabel('Fecha de lanzamiento\nDesarrollador\nDistribuidor',self)
        Datos.setStyleSheet('color: #808080')
        Datos.setGeometry(30, 411, 160, 70)

        self.fec_des_dis = QLabel(self.t_fecha+'\n'+self.t_desarrollador+'\n'+self.t_distribuidor,self)
        self.fec_des_dis.setStyleSheet('color: #FFFFFF')
        self.fec_des_dis.setGeometry(200, 411, 307, 70)
        
        #Boton comprar
        self.comprar = Boton(self)
        self.comprar.setText("Comprar")
        self.comprar.setCursor(Qt.PointingHandCursor)
        self.comprar.setAutoDefault(False)
        self.comprar.setGeometry(30, 491, 100, 30)
        self.comprar.clicked.connect(lambda x: webbrowser.open(self.t_link))

        self.precio = QLabel(self.t_precio,self)
        self.precio.setStyleSheet('color: #808080')
        self.precio.setGeometry(145, 491, 100, 30)

    # ================================================================

    def Nuevo_(self):      
        i=self.Genero.currentIndex()
        if i==0:
            self.t_titulo,self.t_descripcion,self.t_fecha,self.t_precio,self.t_desarrollador,self.t_distribuidor,self.t_link,self.t_posicion=extract()
            
        else:
            self.t_titulo,self.t_descripcion,self.t_fecha,self.t_precio,self.t_desarrollador,self.t_distribuidor,self.t_link,self.t_posicion=extract(posicion_genero=i-1)
    
        self.actualizar()
        self.historial = self.historial[:self.estado+1]+[[self.t_posicion, self.t_link]]
        self.estado += 1
     
    def Anterior_(self):
        if self.estado != 0:
            self.estado -= 1
            Dato = self.historial[self.estado]
            pagina = Dato[0]
            self.t_link = Dato[1]
            if pagina == 0:
                self.t_titulo,self.t_descripcion,self.t_fecha,self.t_precio,self.t_desarrollador,self.t_distribuidor = Steam(self.t_link)

            else:
                self.t_titulo,self.t_descripcion,self.t_fecha,self.t_precio,self.t_desarrollador,self.t_distribuidor = Insta(self.t_link)
            self.actualizar()

    def Siguiente_(self):
        if self.estado+1 != len(self.historial):
            self.estado += 1
            Dato = self.historial[self.estado]
            pagina = Dato[0]
            self.t_link = Dato[1]
            if pagina == 0:
                self.t_titulo,self.t_descripcion,self.t_fecha,self.t_precio,self.t_desarrollador,self.t_distribuidor = Steam(self.t_link)
            
            else:
                self.t_titulo,self.t_descripcion,self.t_fecha,self.t_precio,self.t_desarrollador,self.t_distribuidor = Insta(self.t_link)
            self.actualizar()

    
    def actualizar(self):
        self.titulo.setText(self.t_titulo)
        self.descripcion.clear()
        self.descripcion.insertPlainText(self.t_descripcion)
        self.fec_des_dis.setText(self.t_fecha+'\n'+self.t_desarrollador+'\n'+self.t_distribuidor)
        self.precio.setText(self.t_precio)

        self.imagen.setPixmap(QPixmap('image.png').scaled(460, 215))
        self.imagen_fondo.setPixmap(QPixmap('image.png').scaled(888, 576))

# ================================================================

if __name__ == '__main__':    
    import sys  
    aplicacion = QApplication(sys.argv)
    fuente = QFont()
    fuente.setPointSize(13)
    fuente.setFamily("Bahnschrift")
    aplicacion.setFont(fuente)    
    ventana = Reto()
    ventana.show()      
    sys.exit(aplicacion.exec_())
    