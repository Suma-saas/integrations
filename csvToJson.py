import csv, json
import requests
 
urlApi = 'http://192.168.57.123:8080/'
data = {}
textoJson = ""


try:
	#Lee el archivo
	with open(r'c:\temp\\example.csv','r') as csvFile:
	    csvReader = csv.DictReader(csvFile)
	    for csvRow in csvReader:     	   
	    	a = csvRow['id']	    
	    	data[a]  = csvRow

except Exception as e:
	print("Error a el leer el archivo")


try:	
	#Escribir archivo json
	with open(r'c:\temp\\examplejson.json','w') as jsonFile:
		textoJson = json.dumps(data) 	
		jsonFile.write(textoJson)	
except Exception as e:
	print("Error escribir json")

try:	
	with open(r'\\192.168.57.38\temp\Ejemplojson.json','w') as jsonFileErwin:
		textoJsonErwin = json.dumps(data)	
		jsonFileErwin.write(textoJsonErwin)	

except Exception as e:
	print("Error escribir el archivo json en el servidor 192.168.57.38")



try:
	responseApi = requests.post(urlApi, data=textoJson, headers={'content-type': 'application/json'})
	print("Respuesta " + responseApi.text)
except Exception as e:
	print("Error a el enviar la informacion a el Api Url: " + urlApi)

