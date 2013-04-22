# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

"""
Modulo responsável por realizar as requisições com a api do GitHub.
"""

import settings
from os import path
from json import loads
from requests import get


class Notificacao:

	id_notificacao = None
	nome_usuario = None
	acao = None
	repositorio = None

	def __init__(self, id_notificacao, nome_usuario, acao, repositorio):
		self.id_notificacao = id_notificacao
		self.nome_usuario = nome_usuario
		self.acao = acao
		self.repositorio = repositorio

	def obter_notificacao(self):
		return '{0} {1} {2}'.format(self.nome_usuario, self.acao, self.repositorio)


def obter_notificacoes(nome_usuario):
	notificacoes = []
	try:
		resposta = get('https://api.github.com/users/{0}/received_events'.format(nome_usuario))
		res_json = resposta.json()
		for r in res_json:
			if not (path.exists('{0}/cache/{1}.json'.format(settings.path_media, r['id']))):
				id_notificacao = r['id']
				nome_usuario = r['actor']['login']
				try:
					acao = r['payload']['action']
				except:
					acao = 'forked'
				repositorio = r['repo']['name']
				notificacao = Notificacao(id_notificacao, nome_usuario, acao, repositorio)
				notificacoes.append(notificacao)
				grava_notificacao(notificacao)
	except:
		pass
	return notificacoes


def grava_notificacao(notificacao):
	dados = '{\"id\": \"' + notificacao.id_notificacao + '\",' + '\"nome_usuario\": ' + '\"' + notificacao.nome_usuario + '\",' + '\"acao\": ' + '\"' + notificacao.acao + '\",' + '\"repositorio\": ' + '\"' + notificacao.repositorio+ '\"}'
	arq = open('{0}/cache/{1}.json'.format(settings.path_media, notificacao.id_notificacao), 'w')
	arq.write(dados)
	arq.close()