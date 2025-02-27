<h1 align="center">Monitoreos residenciales en ENRG mediante DTU y API. 
</h1>

<p align="center">
<img  align="center" src="./logo.png">
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
    <summary>Tabla de Contenidos</summary>
    <ol>
        <li><a href="#about-the-project">Acerca del proyecto</a></li>
        <li><a href="#Funcionamiento_general">Funcionamiento general</a>
            <ul>
                <li><a href="#structure_project">Estructura del proyecto </a></li>
                <li><a href="#app">App</a></li>
                <li><a href="#utils">Utils</a></li>
            </ul>
        </li>
        <li><a href="#requirements">Requerimientos instalación </a></li>
        <li><a href="#License">Licencia</a></li>
        <li><a href="#Derechos">Derechos</a></li>
    </ol>
</details>



<p id="about-the-project">
</p>



## Acerca del proyecto

<div style="text-align:justify">

Se ha desarrollado una aplicación tipo script para la recopilación y envío de información sobre la generación de energía en múltiples plantas fotovoltaicas que operan con microinversores de la empresa Hoymiles. Actualmente, los datos de estos microinversores se almacenan en la base de datos de Hoymiles.

Este proyecto surge con el objetivo de aprovechar la API propia de Hoymiles para consultar la información de generación de energía de los microinversores y transferirla a la base de datos de Erco Energy. De esta manera, se facilita la integración de estos datos en la plataforma de monitoreo, permitiendo un seguimiento más eficiente del rendimiento energético.

</div>


<p id="Funcionamiento_general">
</p>

# Funcionamiento general

## Descripción  
Este proyecto cuenta con un script principal encargado de la ejecución de la aplicación. Define las clases y métodos necesarios para la recolección de datos de Hoymiles, su procesamiento y el posterior envío a la base de datos de monitoreo de Erco Energy.  



<p id="structure_project">
</p>

## Estructura del Proyecto  

<p id="app">
</p>

### 📂 `App`  
Contiene la clase principal encargada de la consulta y procesamiento de datos.  

#### **Clase `HoymileReport`**  
- `get_list_plants()`: Retorna las plantas asociadas a la cuenta de Hoymiles.  
- `get_list_microinverters_per_plant()`: Consulta la lista de plantas y devuelve aquellas con sus respectivos microinversores.  
- `get_data_microinverters_per_plant()`:  
  - Obtiene la información de generación de energía de cada microinversor.  
  - Almacena los datos organizados por planta.  
  - Retorna una lista con la información recopilada.  
- `information_processing()`: Procesa la información recopilada y la estructura en el formato adecuado para su envío a la base de datos de Erco Energy.  

<p id="utils">
</p>

### 📂 `utils`  
Contiene clases y métodos reutilizables dentro del proyecto.  

- **`LoggerHandler`**: Registra errores, información general y mensajes de depuración.  
- **`ConfigHandler`**: Obtiene datos del archivo `config.ini`, incluyendo las URLs necesarias para consultar la API de Hoymiles.  
- **`ConfigHandlerKey`**: Administra la clave de autenticación requerida para realizar consultas a la API de Hoymiles. **Por razones de seguridad, esta clave no está disponible directamente en el proyecto.**  

## 📌 Objetivo  
Garantizar la correcta integración y transferencia de datos de generación de energía desde Hoymiles a la base de datos de Erco Energy, facilitando su monitoreo y análisis.  

<p id="requirements" >
    
</p>

## Requerimientos instalación
Para utilizar este proyecto, es necesario cumplir con los siguientes requisitos:  

1. **Python 3.9 o superior** debe estar instalado en el sistema.  
2. Solicitar a la persona encargada el archivo `key.ini`, que contiene la API Key necesaria para el uso de la aplicación de Hoymiles.  
3. Instalar las librerías requeridas ejecutando el siguiente comando en la terminal:  

   ```sh
   pip install -r requirements.txt


<p id="License">
</p>

## Licencias

Este proyecto ha sido desarrollado utilizando **lenguaje de programación y librerías de código abierto (open source)**. No se requirieron licencias adicionales para su implementación.  


<p id="Derechos" >
    
</p>

## Derechos de autor

Todos los derechos son reservados para Erco Energy 2025.