
''' 
	this class serve as fetcher of the files in the storage 
'''
import json

class Storage:

	''' 
		fetch data of account or summary list of account in storage folder

	'''
	def fetch(self,id:str='',list=False) -> dict:
		try:
			#fetch account information
			if(id != '' and list == False):
				return json.load(open(f'storage_accounts_v3/account-{id}.json','r'))
			#fetch summary list of account
			elif(id == '' and list == True):
				return json.load(open(f'storage_accounts_v3/account-list.json','r'))
			else:
				return {'Message':'Empty Search'}
		except Exception as e:
				raise e('File Error: File Doesn\'t exist')
       
	''' 
		store information to the storage folder
	'''
	def store(self,id:str='',data:dict={},list=False) -> bool:
		try:
			#store account information
			if(id != ''and not list):
				json.dump(data,open(f'storage_accounts_v3/account-{id}.json','r'),indent=4)
				return True

			#store summary list of account
			if(id == '' and list):
				json.dump(data,open(f'storage_accounts_v3/account-list.json','r'),indent=4)
				return True
		except Exception as e:
			raise e('File Error: Unable to Write File')

