import funções as f
import requests as r
import datetime as dt
import csv

url = 'https://api.covid19api.com/dayone/country/brazil'
# requisitando/get a url
req = r.get(url)

# verificando se foi bem sucedida a requisição/get
# quando retorna 200 significa que deu certo
# print (req.status_code)

# guardando em um arquivo .json
jason = req.json()
# print (jason[0])

# colocando apenas as 5 informações uteis do arquivo .json em uma lista
lista_final = []
for info in jason:
    lista_final.append([info['Confirmed'], info['Deaths'], info['Recovered'], info['Active'], info['Date']]) # cada ação dessa forma uma lista dentro da lista_final
# print (lista_final)

# inserindo o cabeçalho na lista_final
lista_final.insert(0, ['Confirmados', 'Mortes', 'Recuperados', 'Ativos', 'Data'])
#for linha in lista_final:
    #print (linha)

# tranformando os indices da lista em nomes apenas para ficar mais facil a manipulação
CONFIRMADOS = 0
MORTES = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4

# range começa do 1 para pular o 0 que é o cabeçalho da lista
for posição in range(1, len(lista_final)):
    lista_final[posição][DATA] = lista_final[posição][DATA][:10] # guarda apenas os 9 primeiros digitos
# print (lista_final)

# criando um arquivo csv e colocando as informações da lista_final dentro dele
with open('brasil-covid.csv', 'w', newline='') as file_covid:
    escrita = csv.writer(file_covid)
    escrita.writerows(lista_final)

# transformando a data da lista_final que está como string em um objeto datetime
for posição in range(1, len(lista_final)):
    lista_final[posição][DATA] = dt.datetime.strptime(lista_final[posição][DATA], '%Y-%m-%d')
# print (lista_final)


# CRIANDO UM GRÁFICO COM AS INFORMAÇÕES ACIMA:
# documentação da api ultilizada para o grafico: https://quickchart.io/documentation/

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

# criando QR CODE do grafico
url_base = 'https://quickchart.io/chart'
link = f'{url_base}?c={str(chart)}'
f.save_image('qr-code.png', f.get_api_qrcode(link))
f.display_image('qr-code.png')