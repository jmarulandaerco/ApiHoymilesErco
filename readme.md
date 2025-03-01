<h1 align="center">Residential monitoring in ENRG using DTU and API. 
</h1>

<p align="center">
<img  align="center" src="./logo.png">
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
    <summary>Table of Contents</summary>
    <ol>
        <li><a href="#about-the-project">About the project</a></li>
        <li><a href="#Funcionamiento_general">General operation</a>
            <ul>
                <li><a href="#structure_project">Project structure </a></li>
                <li><a href="#app">App</a></li>
                <li><a href="#utils">Utils</a></li>
            </ul>
        </li>
        <li><a href="#requirements">Installation requirements </a></li>
        <li><a href="#License">License</a></li>
        <li><a href="#Derechos">Copyrights</a></li>
    </ol>
</details>



<p id="about-the-project">
</p>



## About the project

<div style="text-align:justify">

A script-like application has been developed for collecting and sending information about power generation in multiple photovoltaic plants operating with microinverters of the company Hoymiles. Currently, the data from these microinverters are stored in the Hoymiles database.

This project arises with the objective of taking advantage of Hoymiles' own API to query the power generation information of the microinverters and transfer it to Erco Energy's database. In this way, the integration of this data into the monitoring platform is facilitated, allowing a more efficient tracking of energy performance.
</div>


<p id="Funcionamiento_general">
</p>

# General operation

## Description  
This project has a main script in charge of the application execution. It defines the classes and methods needed to collect Hoymiles data, process it and send it to Erco Energy's monitoring database.  


<p id="structure_project">
</p>

## Project structure

<p id="app">
</p>

### 📂 `App`  
It contains the main class in charge of querying and processing data.  

#### **Clase `HoymileReport`**  
- `get_list_plants()`: Returns the plants associated with the Hoymiles account.    
- `get_list_microinverters_per_plant()`: Consult the list of plants and return those with their respective microinverters.  
- `get_data_microinverters_per_plant()`:  
  - Obtains power generation information for each microinverter.  
  - Stores data organized by plant.   
  - Returns a list with the collected information.  
- `information_processing()`: Processes the collected information and structures it in the appropriate format for submission to Erco Energy's database.

<p id="utils">
</p>

### 📂 `utils`  
It contains reusable classes and methods within the project.  

- **`LoggerHandler`**: Logs errors, general information and debugging messages.
- **`ConfigHandler`**: Gets data from the file `config.ini`, including the URLs needed to query the Hoymiles API.  
- **`ConfigHandlerKey`**: Manages the authentication key required for querying the Hoymiles API. **For security reasons, this key is not available directly in the project.**
**  

## 📌 Target  
  
Ensure the correct integration and transfer of power generation data from Hoymiles to Erco Energy's database, facilitating its monitoring and analysis.  
<p id="requirements" >
    
</p>

## Requerimientos instalación
To use this project, the following requirements must be met: 

1. **Python 3.9 o superior** must be installed on the system.    
2. Ask the person in charge for the `key.ini` file, which contains the API Key needed to use the Hoymiles application.  
3. Install the required libraries by executing the following command in the terminal:  

   ```sh
   pip install -r requirements.txt


<p id="License">
</p>

## Licences

This project has been developed using **open source programming language and libraries**. No additional licenses were required for its implementation.  

<p id="Derechos" >
    
</p>

## Copyrights

All rights reserved for Erco Energy 2025.
