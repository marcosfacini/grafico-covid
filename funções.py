import requests as r
from PIL import Image
from IPython.display import display
from urllib.parse import quote

def get_datasets(y, labels):
    if type(y[0]) == list:
        datasets = []
        for i in range(len(y)):
            datasets.append({'label': labels[i],
                            'data': y[i]})
        return datasets
    else:
        return [{'label': labels[0],
                'data': y}]


def set_title(title=''):
    if title != '':
        display = 'true'
    else:
        display = 'false'
    return {'title': title,
            'display': display}


def create_chart(x, y, labels, kind='bar',title=''):
    datasets = get_datasets(y, labels)
    options = set_title(title)
    chart = {'type': kind,
            'date': {'labels': x,
                    'datasets': datasets},
            'options': options}
    return chart 
            
            
def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    resp = r.get(f'{url_base}?c={str(chart)}')
    return resp.content


def save_image(path, content):
    with open(path, 'wb') as image:
        image.write(content)


def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)


def get_api_qrcode(link):
    text = quote(link) # parsing de link para url
    url_base = 'https://quickchart.io/qr'
    resp = r.get(f'{url_base}?text={text}')
    return resp.content 




