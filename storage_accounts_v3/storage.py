
''' 
	this class serve as fetcher of the files in the storage 
'''
import json
import os 
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

	def delete(self,id:str) -> bool:
		
		if self.validate_id(id):
			try:
				os.remove(f'storage_accounts_v3/account-{id}.json')
			except Exception as e:
				log.exception(f'File Error: Account-{id} could\'nt find in the account list ->{e}')
			
			acc_list:dict = json.load(open(f'storage_accounts_v3/account-list.json','r'))
			
			if acc_list == {} or acc_list == None:
				return False

			for acc_id in acc_list['Account-List']:
				if acc_id['Account-ID'] == id:
					acc_list['Account-List'].remove(acc_id)

			json.dump(acc_list,open(f'storage_accounts_v3/account-list.json','w'),indent=4)	
			
			# free memory from the storage
			del acc_list
			
			log.info(f'File Execution: Success Deleting Account-{id}')
			return True
		
		log.info(f'File Execution: Failed to Deleting Account-{id}')
		return False
		

	# check and validate id in the list
	def validate_id(self,id:str) -> bool:
		acc_list:dict = {}
		try:
			#fetch account information
			if id != '':
				log.info(f'fetch information @ account:{id}')
				acc_list = json.load(open(f'storage_accounts_v3/account-list.json','r'))
		except Exception as e:
			log.exception(f'File Error: Non-existing File')

		if acc_list != {}:

			for acc_id in acc_list['Account-List']:
				if acc_id['Account-ID'] == id:
					del acc_list
					return True
				
		del acc_list
		return False
