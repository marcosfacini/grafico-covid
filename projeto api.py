import funções as f
import requests as r
import datetime as dt
import csv

url = 'https://api.covid19api.com/dayone/country/brazil'
req = r.get(url)
print (req.status_code)
jason = req.json()

lista_final = []
for info in jason:
    lista_final.append([info['Confirmed'], info['Deaths'], info['Recovered'], info['Active'], info['Date']]) 

lista_final.insert(0, ['Confirmados', 'Mortes', 'Recuperados', 'Ativos', 'Data'])

CONFIRMADOS = 0
MORTES = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4

for posição in range(1, len(lista_final)):
    lista_final[posição][DATA] = lista_final[posição][DATA][:10] 

with open('brasil-covid.csv', 'w', newline='') as file_covid:
    escrita = csv.writer(file_covid)
    escrita.writerows(lista_final)

for posição in range(1, len(lista_final)):
    lista_final[posição][DATA] = dt.datetime.strptime(lista_final[posição][DATA], '%Y-%m-%d')

y_data_1 = []
for obs in lista_final[1::10]:
    y_data_1.append(obs[CONFIRMADOS])

y_data_2 = []
for obs in lista_final[1::10]:
    y_data_2.append(obs[RECUPERADOS])

labels = ['Confirmados', 'Recuperados']

x = []
for obs in lista_final[1::10]:
    x.append(obs[DATA].strftime('%d/%m/%Y'))

chart = f.create_chart(x, [y_data_1, y_data_2], labels, title='Grafico Confirmados vc Recuperados')
chart_content = f.get_api_chart(chart)
f.save_image('grafico-covid.png', chart_content)
f.display_image('grafico-covid.png')

url_base = 'https://quickchart.io/chart'
link = f'{url_base}?c={str(chart)}'
f.save_image('qr-code.png', f.get_api_qrcode(link))
f.display_image('qr-code.png')





