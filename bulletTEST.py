import requests
from bs4 import BeautifulSoup
import os
import time
import smtplib
import json
from dotenv import load_dotenv

TOKEN_PUSHBULLET = 'o.hyHXS4zCeOrJj8egJi63KklzDss9xOsO'


def checker(URL, cadeira):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    }
    try:
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find("h5").get_text()
        title = title.strip()
    except:
        title = ''

    writepath = f'./T{cadeira}.txt'
    mode = 'r' if os.path.exists(writepath) else 'w'
    with open(writepath, mode) as f:
        try:
            f.write(title)
        except:
            pass

    if title == open(writepath).read():
        pote = False
    else:
        pote = title
    return pote


def textDelete(cadeira):
    if os.path.exists(f"./T{cadeira}.txt"):
        os.remove(f"./T{cadeira}.txt")


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
        print('Message sent!')
        print(body)


cadeiras = {
    'https://fenix.tecnico.ulisboa.pt/disciplinas/IAED1011132646/2020-2021/2-semestre':
    'IAED',  #IAED
    'https://fenix.tecnico.ulisboa.pt/disciplinas/AL2011132646/2020-2021/2-semestre':
    'AL',  #AL
    'https://fenix.tecnico.ulisboa.pt/disciplinas/IETI11132646/2020-2021/2-semestre':
    'IETI',  #IETI
    'https://fenix.tecnico.ulisboa.pt/disciplinas/ACom1011132646/2020-2021/2-semestre':
    'AC',  #AC
    'https://fenix.tecnico.ulisboa.pt/disciplinas/MO1511132646/2020-2021/2-semestre':
    'MO'  #MO
}

while True:
    for cadeira in cadeiras.keys():
        if checker(cadeira, cadeiras[cadeira]):
            pushbullet_message('Novo Anuncio!',
                               checker(cadeira, cadeiras[cadeira]))
            textDelete(cadeiras[cadeira])
    time.sleep(10)