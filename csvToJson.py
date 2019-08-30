import csv, json
import requests
 

urlApi = 'http://192.168.57.123:8080/'
data = {}
textoJson = ""

#Lee el archivo
with open(r'c:\temp\\example.csv','r') as csvFile:
    csvReader = csv.DictReader(csvFile)
    for csvRow in csvReader:     	   
    	a = csvRow['id']	    
    	data[a]  = csvRow

#Escribir archivo json
with open(r'c:\temp\\examplejson.json','w') as jsonFile:
	textoJson = json.dumps(data) 	
	jsonFile.write(textoJson)	



with open(r'\\192.168.57.38\temp\Ejemplojson.json','w') as jsonFileErwin:
	textoJsonErwin = json.dumps(data)	
	jsonFileErwin.write(textoJsonErwin)	




responseApi = requests.post(urlApi, data=textoJson, headers={'content-type': 'application/json'})
print("Respuesta " + responseApi.text)




