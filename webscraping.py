import requests
from bs4 import BeautifulSoup
import os
import time
import smtplib
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN_MAIL = os.getenv('MAIL_TOKEN')
TOKEN_PUSHBULLET = os.getenv('PUSHBULLET_TOKEN')


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


def emailSender(URL, cadeira):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('pedropereira972@gmail.com', TOKEN_MAIL)

    subject = f'Novo Anuncio! ({cadeira})'
    body = f'Novo Anuncio em: \n {URL}'
    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail('pedropereira972@gmail.com', 'pedropereira972@gmail.com',
                    msg)
    server.sendmail('pedropereira972@gmail.com',
                    'p.vaz.pereira@tecnico.ulisboa.pt', msg)
    print('SENT!')
    server.quit()


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
    'https://fenix.tecnico.ulisboa.pt/disciplinas/FP179577/2020-2021/1-semestre':
    'FP',  #FP
    'https://fenix.tecnico.ulisboa.pt/disciplinas/AL291795137/2020-2021/1-semestre':
    'AL',  #AL
    'https://fenix.tecnico.ulisboa.pt/disciplinas/EMD/2020-2021/1-semestre':
    'EMD',  #EMD
    'https://fenix.tecnico.ulisboa.pt/disciplinas/SD9179577/2020-2021/1-semestre':
    'SD'  #SD
}

while True:
    for cadeira in cadeiras.keys():
        if not checker(cadeira, cadeiras[cadeira]):
            emailSender(cadeira, cadeiras[cadeira])
            pushbullet_message(
                'Novo Anuncio!',
                f'Novo anuncio em ({cadeiras[cadeira]}):\n {cadeira}')
            textDelete(cadeiras[cadeira])
    time.sleep(5 * 60)
