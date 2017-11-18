# UESMO - Urban Energy System Modeling using OSeMOSYS

## Background

OSeMOSYS is an open source energy system optimization model developed by KTH-Desa. OSeMOSYS is designed to find the most cost effective way to meet an energy demand through a system submitted to constraints. All informations about the model are available at: http://www.osemosys.org/ 

In this project, OSeMOSYS's code has been modified in order to design of a spacial optimization model for urban energy planning. The model has been tested on the Metropolitan Comunity of Montreal. This projects has been led by a team of researchers from UQAM (Montreal) and GERAD (Montreal) and has been funded by the CRSNG.

## Documents

UESMO_model_explanation.pdf: UESMO's modeling approach is slightly different from the one of OSeMOSYS. This file presents all the model specificities.  

MUESMO_V1.txt: This is the model's file. he modified version of OSeMOSYS. 

UESMO_CMM.txt: This is the input file. It's a database containing all information needed from the model. 

model result/model_result.py: Piece of code in python to format the model's results. 
model result/model_result.ipynb: Jupyter version of the previous file. 

model_format.py: (work in progress) piece of code in python to format a GIS database into a txt file readable by the model. 

