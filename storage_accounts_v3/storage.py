
''' 
	this class serve as fetcher of the files in the storage 
'''
import json
from Log.log import Log


log = Log('storage.log').open()

class Storage:

	''' 
		fetch data of account or summary list of account in storage folder

	'''
	def fetch(self,id:str='',list=False) -> dict:
		try:
			#fetch account information
			if(id != '' and list == False):
				log.info(f'fetch information @ account:{id}')
				return json.load(open(f'storage_accounts_v3/account-{id}.json','r'))
			#fetch summary list of account
			elif(id == '' and list == True):
				log.info(f'fetch information @ account-list')
				return json.load(open(f'storage_accounts_v3/account-list.json','r'))
			else:
				log.info(f'empty search parameter')
				return {'Message':'Empty Search'}
		except Exception as e:
				log.exception(f'File Error: File Doesn\'t exist')
				raise e('File Error: File Doesn\'t exist')
       
	''' 
		store information to the storage folder
	'''
	def store(self,id:str='',data:dict={},list=False) -> bool:
		try:
			#store account information
			if(id != ''and not list):
				log.info(f'store information @ account:{id}')
				json.dump(data,open(f'storage_accounts_v3/account-{id}.json','w'),indent=4)
				return True

			#store summary list of account
			if(id == '' and list):
				log.info(f'store information @ account-list')
				json.dump(data,open(f'storage_accounts_v3/account-list.json','w'),indent=4)
				return True
		except Exception as e:
			log.exception(f'File Error: Unable to Write File')
			raise e('File Error: Unable to Write File')

	def validate_id(self,id:str) -> bool:
		temp:dict = {}
		try:
			#fetch account information
			if(id != ''):
				log.info(f'fetch information @ account:{id}')
				temp = json.load(open(f'storage_accounts_v3/account-{id}.json','r'))
		except Exception as e:
			log.exception(f'File Error: Non-existing File')
			raise e('File Error: Non-existing File')
		if(temp != {}):
			if(temp['Account-ID'] == id):
				return True
		return False
