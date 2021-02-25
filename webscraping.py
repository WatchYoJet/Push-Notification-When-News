import requests
from bs4 import BeautifulSoup
import os
import time
import smtplib
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN_PUSHBULLET = 'o.hyHXS4zCeOrJj8egJi63KklzDss9xOsO'


def checker(URL, cadeira):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    }
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id='content-block').get_text()
    title = title.strip()

    htmlText = ''
    j = 16
    while title[j] not in ('123456789'):
        htmlText += title[j]
        j += 1

    writepath = f'./htmlText{cadeira}.txt'
    mode = 'r' if os.path.exists(writepath) else 'w'
    with open(writepath, mode) as f:
        try:
            f.write(htmlText)
        except:
            pass

    if htmlText == open(writepath).read():
        pote = True
    else:
        pote = False
    return pote


def textDelete(cadeira):
    if os.path.exists(f"htmlText{cadeira}.txt"):
        os.remove(f"htmlText{cadeira}.txt")


def pushbullet_message(title, body):
    msg = {"type": "note", "title": title, "body": body}
    resp = requests.post('https://api.pushbullet.com/v2/pushes',
                         data=json.dumps(msg),
                         headers={
                             'Authorization': 'Bearer ' + TOKEN_PUSHBULLET,
                             'Content-Type': 'application/json'
                         })
    if resp.status_code != 200:
        raise Exception('Error', resp.status_code)
    else:
        print('Message sent')


cadeiras = {
    'https://fenix.tecnico.ulisboa.pt/disciplinas/IAED1011132646/2020-2021/2-semestre':
    'IAED',  #IAED
    'https://fenix.tecnico.ulisboa.pt/disciplinas/AL2011132646/2020-2021/2-semestre':
    'AL',  #AL
    'https://fenix.tecnico.ulisboa.pt/disciplinas/IETI11132646/2020-2021/2-semestre':
    'IETI',  #EMD
    'https://fenix.tecnico.ulisboa.pt/disciplinas/ACom1011132646/2020-2021/2-semestre':
    'AC',  #SD
    'https://fenix.tecnico.ulisboa.pt/disciplinas/MO1511132646/2020-2021/2-semestre':
    'MO'
}

while True:
    for cadeira in cadeiras.keys():
        if not checker(cadeira, cadeiras[cadeira]):
            pushbullet_message(
                'Novo Anuncio!',
                f'Novo anuncio em ({cadeiras[cadeira]}):\n {cadeira}')
            textDelete(cadeiras[cadeira])
    time.sleep(5 * 60)
