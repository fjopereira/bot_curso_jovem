import json
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.authtoken.models import Token

from telefone.models import Telefone
from log.models import Log
from interacao.models import Interacao
from mensagens.models import Mensagem


def post_envio(number, message):
    url = "http://127.0.0.1:8001/send-message"

    payload = {'number': number,
               'message': message}

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        objeto_json = json.loads(response.text)

        status = objeto_json['status']
        mensagem_api = objeto_json['message']
        de = objeto_json['response']['_data']['from']['user']
        para = objeto_json['response']['_data']['id']['remote']['user']
        mensagem_enviada = objeto_json['response']['body']
        retorno_post = {'status_code': response.status_code,
                        'status': status,
                        'mensagem_api': mensagem_api,
                        'de': de,
                        'para': para,
                        'mensagem_enviada': mensagem_enviada}

        # print(response.headers)
        # print(response.text)
        # print(retorno_post)
        return retorno_post

    except Exception as e:
        print(f"Erro ao enviar mensagem, verificar a api: {str(e)}")


def post_envio_audio(number, file):
    url = "http://127.0.0.1:8001/send-record"

    payload = {'number': number,
               'file': file}

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        objeto_json = json.loads(response.text)

        status = objeto_json['status']
        mensagem_api = objeto_json['message']
        de = objeto_json['response']['_data']['from']['user']
        para = objeto_json['response']['_data']['id']['remote']['user']
        mensagem_enviada = objeto_json['response']['body']
        retorno_post = {'status_code': response.status_code,
                        'status': status,
                        'mensagem_api': mensagem_api,
                        'de': de,
                        'para': para,
                        'mensagem_enviada': mensagem_enviada}

        # print(response.headers)
        # print(response.text)
        # print(retorno_post)
        return retorno_post

    except Exception as e:
        print(f"Erro ao enviar mensagem, verificar a api: {str(e)}")


def post_envio_media(number, caption, file):
    url = "http://127.0.0.1:8001/send-media"

    payload = {'number': number,
               'caption': caption,
               'file': file}


    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        objeto_json = json.loads(response.text)

        status = objeto_json['status']
        mensagem_api = objeto_json['message']
        de = objeto_json['response']['_data']['from']['user']
        para = objeto_json['response']['_data']['id']['remote']['user']
        mensagem_enviada = objeto_json['response']['body']
        retorno_post = {'status_code': response.status_code,
                        'status': status,
                        'mensagem_api': mensagem_api,
                        'de': de,
                        'para': para,
                        'mensagem_enviada': mensagem_enviada}

        # print(response.headers)
        # print(response.text)
        # print(retorno_post)
        return retorno_post

    except Exception as e:
        print(f"Erro ao enviar mensagem, verificar a api: {str(e)}")


@csrf_exempt
def post_entrada(request):
    if request.method == 'POST':
        token_header = request.META.get('HTTP_AUTHORIZATION')
        if token_header and token_header.startswith('Token '):
            token_key = token_header.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                request.user = token.user
            except Token.DoesNotExist:
                return HttpResponse("Token inválido.", status=401)
        else:
            return HttpResponse("Token não fornecido.", status=401)

        try:
            data = json.loads(request.body.decode('utf-8'))
            telefone_entrada = data.get('number')
            retorno_entrada = data.get('message')

            log = Log(telefone=telefone_entrada, tipo='in', mensagem=retorno_entrada)
            log.save()

            if telefone_entrada is not None and retorno_entrada is not None:
                try:
                    telefone = Telefone.objects.get(numero_telefone=telefone_entrada)
                    p_ordem = float(telefone.ordem)

                except Telefone.DoesNotExist:
                    telefone = Telefone(numero_telefone=telefone_entrada, ordem=0)
                    telefone.save()
                    p_ordem = 0

                bot_respostas(telefone_entrada, retorno_entrada, p_ordem)
                return JsonResponse({'status': 'success', 'message': 'Mensagem recebida com sucesso pela api!'})

            return JsonResponse({'status': 'error', 'message': 'Verificar os dados passados no post da api'})

        except Exception as e:
            print(f"Erro ao receber as informações da API: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Erro ao tratar o retorno da API'})


def clean(p_campo):
    palavras = p_campo.strip()
    palavras = palavras.split()
    palavras_formatadas = [palavra.strip().capitalize() for palavra in palavras]
    vsretorno = ' '.join(palavras_formatadas)
    return vsretorno

def valida_int(valor):
    try:
        numero_inteiro = int(valor)
        return numero_inteiro
    except ValueError:
        return None

def bot_respostas(p_telefone_chat, p_retorno_chat, p_ordem):
    print(p_telefone_chat, p_retorno_chat, p_ordem)

    mensagem = Mensagem.objects.filter(id=1).first()
    telefone = Telefone.objects.get(numero_telefone=p_telefone_chat)

    mensagem_erro = 'N'
    mensagem_erro_generica = 'Opção fora das apresentadas. ' \
                                'Vamos tentar novamente!'

    if p_retorno_chat == '#admin-bot-desativar#':
        mensagem.bot = False
        mensagem.save()

        mensagem = "Bot desativado"

        post_envio(p_telefone_chat, mensagem)

        log = Log(telefone=p_telefone_chat, tipo='out', mensagem=mensagem)
        log.save()

    elif p_retorno_chat == '#admin-bot-ativar#':
        mensagem.bot = True
        mensagem.save()

        mensagem = "Bot ativado"

        post_envio(p_telefone_chat, mensagem)

        log = Log(telefone=p_telefone_chat, tipo='out', mensagem=mensagem)
        log.save()

    # saudação
    elif p_ordem == 0 and mensagem.bot is True:
        telefone.ordem = 2.0
        telefone.save()

        interacao = Interacao.objects.get(ordem=1)

        post_envio(p_telefone_chat, interacao.mensagem)

        log = Log(telefone=p_telefone_chat, tipo='out', mensagem=interacao.mensagem)
        log.save()

    #audios explicação
    elif p_ordem == 2.0 and mensagem.bot is True:
        if valida_int(p_retorno_chat) is not None:
            if int(p_retorno_chat) in (1, 2):
                if int(p_retorno_chat) == 1:
                    #envia o audio sim
                    interacao = Interacao.objects.get(ordem=2.0)
                    post_envio_audio(p_telefone_chat, interacao.audio)

                    log = Log(telefone=p_telefone_chat, tipo='out', mensagem=interacao.audio)
                    log.save()

                    #envia mensagem confirmação para continuar o cadastro
                    interacao = Interacao.objects.get(ordem=2.1)
                    post_envio(p_telefone_chat, interacao.mensagem)

                    log = Log(telefone=p_telefone_chat, tipo='out', mensagem=interacao.mensagem)
                    log.save()

                    telefone.ordem = 2.1
                    telefone.save()

                else:
                    # envia o audio não
                    interacao = Interacao.objects.get(ordem=2.2)
                    post_envio_audio(p_telefone_chat, interacao.audio)

                    log = Log(telefone=p_telefone_chat, tipo='out', mensagem=interacao.audio)
                    log.save()

                    #envia a imagem
                    interacao = Interacao.objects.get(ordem=2.3)
                    post_envio_media(p_telefone_chat, interacao.mensagem, interacao.img)

                    log = Log(telefone=p_telefone_chat, tipo='out', mensagem=interacao.img)
                    log.save()

                    # envia mensagem de agradecimento
                    interacao = Interacao.objects.get(ordem=2.4)
                    post_envio(p_telefone_chat, interacao.mensagem)

                    log = Log(telefone=p_telefone_chat, tipo='out', mensagem=interacao.mensagem)
                    log.save()

                    #ordem para mensagem dados salvos
                    telefone.ordem = 0
                    telefone.save()

            else:
                mensagem_erro = mensagem_erro_generica

        else:
            mensagem_erro = 'Você precisa informar uma das opções apresentadas. ' \
                            'Vamos tentar novamente!'

    #confirma inscrição
    elif p_ordem == 2.1 and mensagem.bot is True:
        if valida_int(p_retorno_chat) is not None:
            if int(p_retorno_chat) in (1, 2):
                if int(p_retorno_chat) == 1:
                    # envia mesangem de incrição
                    interacao = Interacao.objects.get(ordem=3.0)
                    post_envio(p_telefone_chat, interacao.mensagem)

                    log = Log(telefone=p_telefone_chat, tipo='out', mensagem=interacao.mensagem)
                    log.save()

                    # envia mesangam como gostaria de ser chamado
                    interacao = Interacao.objects.get(ordem=4.0)
                    post_envio(p_telefone_chat, interacao.mensagem)

                    log = Log(telefone=p_telefone_chat, tipo='out', mensagem=interacao.mensagem)
                    log.save()

                    telefone.ordem = 4.0
                    telefone.save()

                else:
                    # envia o audio não
                    interacao = Interacao.objects.get(ordem=2.2)
                    post_envio_audio(p_telefone_chat, interacao.audio)

                    log = Log(telefone=p_telefone_chat, tipo='out', mensagem=interacao.audio)
                    log.save()

                    # envia a imagem
                    interacao = Interacao.objects.get(ordem=2.3)
                    post_envio_media(p_telefone_chat, interacao.mensagem, interacao.img)

                    log = Log(telefone=p_telefone_chat, tipo='out', mensagem=interacao.img)
                    log.save()

                    # envia mensagem de agradecimento
                    interacao = Interacao.objects.get(ordem=2.4)
                    post_envio(p_telefone_chat, interacao.mensagem)

                    log = Log(telefone=p_telefone_chat, tipo='out', mensagem=interacao.mensagem)
                    log.save()

                    # ordem para mensagem dados salvos
                    telefone.ordem = 0
                    telefone.save()

            else:
                mensagem_erro = mensagem_erro_generica

        else:
            mensagem_erro = 'Você precisa informar uma das opções que representa se deseja continuar. ' \
                            'Vamos tentar novamente!'

    # apelido
    elif p_ordem == 4.0 and mensagem.bot is True:
        telefone.apelido = clean(p_retorno_chat)
        telefone.ordem = 5.0
        telefone.save()

        interacao = Interacao.objects.get(ordem=5.0)
        mensagem_alterada = interacao.mensagem
        mensagem_alterada = mensagem_alterada.replace("#apelido#", telefone.apelido)

        post_envio(p_telefone_chat, mensagem_alterada)

        log = Log(telefone=p_telefone_chat, tipo='out', mensagem=mensagem_alterada)
        log.save()

    # nome jovem
    elif p_ordem == 5.0 and mensagem.bot is True:
        telefone.nome_jovem = clean(p_retorno_chat)
        telefone.ordem = 6.0
        telefone.save()

        interacao = Interacao.objects.get(ordem=6.0)
        mensagem_alterada = interacao.mensagem
        mensagem_alterada = mensagem_alterada.replace("#apelido#", telefone.apelido)
        mensagem_alterada = mensagem_alterada.replace("#nome_jovem#", telefone.nome_jovem)

        post_envio(p_telefone_chat, mensagem_alterada)

        log = Log(telefone=p_telefone_chat, tipo='out', mensagem=mensagem_alterada)
        log.save()

    # idade jovem
    elif p_ordem == 6.0 and mensagem.bot is True:
        telefone.idade_jovem = clean(p_retorno_chat)
        telefone.ordem = 7.0
        telefone.save()

        interacao = Interacao.objects.get(ordem=7.0)
        mensagem_alterada = interacao.mensagem
        mensagem_alterada = mensagem_alterada.replace("#nome_jovem#", telefone.nome_jovem)

        post_envio(p_telefone_chat, mensagem_alterada)

        log = Log(telefone=p_telefone_chat, tipo='out', mensagem=mensagem_alterada)
        log.save()

    # telefone jovem
    elif p_ordem == 7.0 and mensagem.bot is True:
        telefone.telefone_jovem = clean(p_retorno_chat)
        telefone.ordem = 8.0
        telefone.save()

        interacao = Interacao.objects.get(ordem=8.0)
        mensagem_alterada = interacao.mensagem
        mensagem_alterada = mensagem_alterada.replace("#apelido#", telefone.apelido)

        post_envio(p_telefone_chat, mensagem_alterada)

        log = Log(telefone=p_telefone_chat, tipo='out', mensagem=mensagem_alterada)
        log.save()

    #escolaridade jovem
    elif p_ordem == 8.0 and mensagem.bot is True:
        if valida_int(p_retorno_chat) is not None:
            if int(p_retorno_chat) in (1, 2, 3, 4):
                if int(p_retorno_chat) == 1:
                    v_escolaridade = 'Ensino Fundamental'
                elif int(p_retorno_chat) == 2:
                    v_escolaridade = 'Ensino Médio'
                elif int(p_retorno_chat) == 3:
                    v_escolaridade = 'Ensino Superior'
                elif int(p_retorno_chat) == 4:
                    v_escolaridade = 'Não estuda atualmente'

                telefone.escolaridade = v_escolaridade
                telefone.ordem = 9.0
                telefone.save()

                interacao = Interacao.objects.get(ordem=9.0)

                mensagem_alterada = interacao.mensagem
                mensagem_alterada = mensagem_alterada.replace("#apelido#", telefone.apelido)
                mensagem_alterada = mensagem_alterada.replace("#nome_jovem#", telefone.nome_jovem)

                post_envio(p_telefone_chat, mensagem_alterada)

                log = Log(telefone=p_telefone_chat, tipo='out', mensagem=mensagem_alterada)
                log.save()

            else:
                mensagem_erro = mensagem_erro_generica

        else:
            mensagem_erro = 'Você precisa informar uma das opções que represente a escolaridade. ' \
                            'Vamos tentar novamente!'

    # turno de estudo
    elif p_ordem == 9.0 and mensagem.bot is True:
        if valida_int(p_retorno_chat) is not None:
            if int(p_retorno_chat) in (1, 2, 3, 4):
                if int(p_retorno_chat) == 1:
                    v_turno = 'Matutino'
                elif int(p_retorno_chat) == 2:
                    v_turno = 'Vespertino'
                elif int(p_retorno_chat) == 3:
                    v_turno = 'Noturno'
                elif int(p_retorno_chat) == 4:
                    v_turno = 'Não estuda atualmente'

                telefone.turno = v_turno
                telefone.ordem = 10.0
                telefone.save()

                interacao = Interacao.objects.get(ordem=10.0)

                mensagem_alterada = interacao.mensagem
                mensagem_alterada = mensagem_alterada.replace("#apelido#", telefone.apelido)
                mensagem_alterada = mensagem_alterada.replace("#nome_jovem#", telefone.nome_jovem)

                post_envio(p_telefone_chat, mensagem_alterada)

                log = Log(telefone=p_telefone_chat, tipo='out', mensagem=mensagem_alterada)
                log.save()

            else:
                mensagem_erro = mensagem_erro_generica

        else:
            mensagem_erro = 'Você precisa informar uma das opções que represente o turno de estudo. ' \
                            'Vamos tentar novamente!'

    # nome responsavel
    elif p_ordem == 10.0 and mensagem.bot is True:
        telefone.nome_responsavel = clean(p_retorno_chat)
        telefone.ordem = 11.0
        telefone.save()

        interacao = Interacao.objects.get(ordem=11.0)

        mensagem_alterada = interacao.mensagem
        mensagem_alterada = mensagem_alterada.replace("#apelido#", telefone.apelido)

        post_envio(p_telefone_chat, mensagem_alterada)

        log = Log(telefone=p_telefone_chat, tipo='out', mensagem=mensagem_alterada)
        log.save()

    #telefone responsavel
    elif p_ordem == 11.0 and mensagem.bot is True:
        telefone.telefone_responsavel = clean(p_retorno_chat)
        telefone.ordem = 12.0
        telefone.save()

        interacao = Interacao.objects.get(ordem=12.0)

        mensagem_alterada = interacao.mensagem
        mensagem_alterada = mensagem_alterada.replace("#1#", telefone.nome_jovem)
        mensagem_alterada = mensagem_alterada.replace("#2#", telefone.nome_jovem)
        mensagem_alterada = mensagem_alterada.replace("#3#", telefone.idade_jovem)
        mensagem_alterada = mensagem_alterada.replace("#4#", telefone.telefone_jovem)
        mensagem_alterada = mensagem_alterada.replace("#5#", telefone.escolaridade)
        mensagem_alterada = mensagem_alterada.replace("#6#", telefone.turno)
        mensagem_alterada = mensagem_alterada.replace("#7#", telefone.nome_responsavel)
        mensagem_alterada = mensagem_alterada.replace("#8#", telefone.telefone_responsavel)

        post_envio(p_telefone_chat, mensagem_alterada)

        log = Log(telefone=p_telefone_chat, tipo='out', mensagem=mensagem_alterada)
        log.save()

    # Confirmacao
    elif p_ordem == 12.0 and mensagem.bot is True:
        if valida_int(p_retorno_chat) is not None:
            if int(p_retorno_chat) in (1, 2):
                if int(p_retorno_chat) == 1:
                    # envia o audio
                    interacao = Interacao.objects.get(ordem=13.0)
                    post_envio_audio(p_telefone_chat, interacao.audio)

                    log = Log(telefone=p_telefone_chat, tipo='out', mensagem=interacao.audio)
                    log.save()

                    # envia a imagem
                    interacao = Interacao.objects.get(ordem=14.0)
                    post_envio_media(p_telefone_chat, interacao.mensagem, interacao.img)

                    log = Log(telefone=p_telefone_chat, tipo='out', mensagem=interacao.img)
                    log.save()

                    #ordem que envia para mensagem que os dados foram salvos se houver outra interação
                    telefone.ordem = 20.0
                    telefone.save()

                else:
                    telefone.ordem = 0
                    telefone.save()
                    bot_respostas(p_telefone_chat, 'reiniciou', 0)

            else:
                mensagem_erro = mensagem_erro_generica

        else:
            mensagem_erro = 'Você precisa informar uma das opção valida para continuar. ' \
                            'Vamos tentar novamente!'

    # Final
    elif p_ordem == 20.0 and mensagem.bot is True:
        mensagem = 'Seus dados foram salvos, agora é só aguardar. Boa sorte!'
        post_envio(p_telefone_chat, mensagem)

        #não responde mais
        telefone.ordem = 21
        telefone.save()

        log = Log(telefone=p_telefone_chat, tipo='out', mensagem=mensagem)
        log.save()

    #para de interagir com o telefone
    elif int(p_ordem) == 21.0 and mensagem.bot is True:
        pass

    if mensagem_erro != 'N':
        post_envio(p_telefone_chat, mensagem_erro)

        log = Log(telefone=p_telefone_chat, tipo='out', mensagem=mensagem_erro)
        log.save()

