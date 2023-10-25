import openai
import apikey
import speech_recognition as sr
import pyttsx3
import os

openai.api_key = apikey.apikey

print('''
\033[92m      ___         _     __       _      ________             ___          ___      ________    __    __    __     ___  ___   ________      _     __         ___     __     __   ________      _     __       ___         _     __\033[00m
\033[92m    //   ) )     //    / /     // | |  /__  ___/           //   ) )     //   ) )  /__  ___/    ||   /  |  / /       / /     /__  ___/     //    / /       //   ) )  \ \   / /  /__  ___/     //    / /     //   ) )     /|    / /\033[00m
\033[92m   //           //___ / /     //__| |    / /              //           //___/ /     / /        ||  /   | / /       / /        / /        //___ / /       //___/ /    \ \ / /     / /        //___ / /     //   / /     //|   / /\033[00m
\033[92m  //           / ___   /     / ___  |   / /      ____    //  ____     / ____ /     / /         || / /| |/ /       / /        / /        / ___   /       / ____ /      \ / /     / /        / ___   /     //   / /     // |  / /\033[00m
\033[92m //           //    / /     //    | |  / /              //    / /    //           / /          ||/ / |   /       / /        / /        //    / /       //              / /     / /        //    / /     //   / /     //  | / /\033[00m
\033[92m((____/ /    //    /_/     //     |_| /_/              ((____/ /    //           /_/           |__/  |__/     __/ /___     /_/        //    /_/       //              /_/     /_/        //    /_/     ((___/ /     //   |/_/\033[00m\n''')

def capturar_fala():
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Fale sua pergunta:")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            texto = recognizer.recognize_google(audio, language='pt-BR')
            print("Você disse:", texto)
            return texto
        except sr.UnknownValueError:
            mensagem = [1]
            mensagem.pop(0)
            mensagem.insert(0, 'Desculpe, não consegui entender o que você disse. Por favor, tente novamente.')
            print('Desculpe, não consegui entender o que você disse. Por favor, tente novamente.')
            falar(mensagem)
        except sr.RequestError as e:
            print("Erro na solicitação ao serviço de reconhecimento de fala; {0}".format(e))

def falar(mensagem):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'pt-br')  # Seleciona uma voz em português
    engine.say(mensagem)
    engine.runAndWait()

quer_continuar = 's'
repetir_continuar_ecolha_voz_texto = 's'
fala_ou_texto_mesma = 's'

while quer_continuar.lower() =='s':
    fala_ou_texto=input('voce quer escrever ou falar sua pergunta? falar|escrever ')
    fala_ou_texto_mesma = 's'

    while fala_ou_texto_mesma.lower() == 's' :
        if fala_ou_texto.lower() == 'falar':
            entrada_voz = capturar_fala()
            saida_voz = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": entrada_voz}])
            print(saida_voz.choices[0].message.content)
            mensagem_voz = [saida_voz.choices[0].message.content]
            falar(mensagem_voz)
            repetir_continuar = 's'

        elif fala_ou_texto.lower()=='escrever':
            entrada_texto=input('digite o que voce quer saber: ')
            saida_texto = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": entrada_texto}])
            print(saida_texto.choices[0].message.content)
            mensagem_voz = [saida_texto.choices[0].message.content]
            falar(mensagem_voz)
            repetir_continuar = 's'

        else:
            print('não entendi, digite novamente')
            repetir_continuar = 'n'
            quer_continuar = 's'
            repetir_continuar_ecolha_voz_texto = 'n'
            fala_ou_texto_mesma = 'n'
            os.system('clear')


        while repetir_continuar.lower() == 's':
            quer_continuar = input('quer continuar? S|N ')

            if quer_continuar.lower() == 's' or quer_continuar.lower()=='sim':

                while repetir_continuar_ecolha_voz_texto.lower() == 's':
                    repetir_continuar_ecolha_voz_texto = input(f'quer continuar com sua escolha de {fala_ou_texto} para o uso do chat? S|N ' )
                    if repetir_continuar_ecolha_voz_texto.lower() == 's' or repetir_continuar_ecolha_voz_texto.lower() == 'sim':
                        repetir_continuar = 'n'
                        quer_continuar = 'n'
                        repetir_continuar_ecolha_voz_texto = 'n'
                        fala_ou_texto_mesma = 's'
                        os.system('clear')

                    elif repetir_continuar_ecolha_voz_texto.lower() == 'n' or repetir_continuar_ecolha_voz_texto.lower() == 'nao' or repetir_continuar_ecolha_voz_texto.lower() == 'não':
                        repetir_continuar = 'n'
                        quer_continuar = 's'
                        repetir_continuar_ecolha_voz_texto = 'n'
                        fala_ou_texto_mesma = 'n'
                        os.system('clear')
                    else:
                            print('não entendi, digite novamente')
                            repetir_continuar_ecolha_voz_texto = 's'

            elif quer_continuar.lower() == 'n' or quer_continuar.lower()=='nao' or quer_continuar.lower()=='não':
                repetir_continuar = 'n'
                quer_continuar = 'n'
                fala_ou_texto_mesma = 'n'
                break

            else:
                print('não entendi, digite novamente')
                repetir_continuar = 's'
                repetir_continuar_ecolha_voz_texto = 's'