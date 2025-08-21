# Proyecto Final de Curso Asir

### Descripción

Este proyecto es el resultado final del curso de ASIR. El objetivo del proyecto es realizar una aplicación web para comprar productos relacionados con la música electrónica.
### Tecnologias utilizadas: 
##### Front-End:
- Javascript
- Vue.js
- Element.ui
- HTML5
- CSS3
##### Back-End:
- Python
- Django
- Djnago rest framework
- JWT


##### Instalación del back:
1. INSTALAMOS BREW:
- /bin/bash -c "$(curl
- fsSL ttps://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2\.	INSTALAMOS PYTHON:

- brew install python
- export PATH="/opt/homebrew/bin:$PATH"
- source ~/.zshrc

3\.	INSTALAMOS DJANGO Y TODAS LAS DEPENDENCIAS:

- pip3 install -r requirements.txt

4\.	INSTALAMOS MYSQL:

- brew install mysql

arrancamos el servicio:

- brew services start mysql
- Iniciamos sesión: mysql -u root
- Creamos la BD: CREATE DATABASE WhileShadows;
- Creamos el usuario de la BD: CREATE USER 'Miguel'@'127.0.0.1' IDENTIFIED BY 'Miguel';
- Concedemos los permisos:
- GRANT ALL PRIVILEGES ON WhileShadows.\* TO 'Miguel'@'127.0.0.1';FLUSH PRIVILEGES;

5\.	VOLCAMOS EL BACKUP CON ESTE COMANDO: mysql -u root -p WhileShadows < /ruta\_del\_archivo/whileshadows\_backup.sql

6\.	PARA ACTIVAR EL CERTIFICADO Y PODER ENVIAR CORREOS: Debemos irnos al contenido del paquete de python y ejecutamos el archivo:

- Install Certificates.command

7\.	INICIAMOS EL BACK: python3 manage.py runserver


##### Instalación del font:
1. INSTALAMOS BREW:
- /bin/bash -c "$(curl fsSL ttps://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2\.	INSTALAMOS NODE:

- brew install node

3\.	NOS DIRIGIMOS A LA RUTA DEL DIRECTORIO DE VUE

4\.	INSTALAMOS YARN:

- brew install yarn

5\.   INSTALAMOS LAS DEPENDENCIAS:

- yarn install

6\.   EJECUTAMOS EL FRONT:

- yarn serve

##### Nota obtenida del proyecto : 9.5

#####  Por último, Para más detalles, consulta la [documentación completa](https://github.com/migueligle/While-Shadows/blob/089c98486badcb7281dddd6878224eaced8763d3/memoria-2023-miguel-iglesias-asir.pdf).

