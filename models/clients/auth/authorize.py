from models.clients.maker_teams_client import MTClient
from flask import request, redirect, url_for


class Authorize():

	@classmethod
	def integration(cls, client):
		client = client()
		return client.authorization_url

	@classmethod
	def request_token(cls, client, code=None):
		return client.request_token(code)







'''
		when should data be injected into an instantiation of a class vs contained within the methods
		credentials - inside from env vars
		endpoints - inside in the code
		parameters - injected from the domain at which they're decided
		parameters inserted when they're not request/object specific - 

cli_id and scope can be built same as prameters in mtclient requests
'''
