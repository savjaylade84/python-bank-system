
''' 
	this class serve as fetcher of the files in the storage 
'''
import json
import os 
from Log.log import Log


log = Log('storage.log').open()

class Storage:


	'''
        :Description: fetch account or account list data from a file in the storage folder

        :Parameter:
					:id: string - :default: ''
					:list: boolean - :default: false
        :Return: Dictionary
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
        :Description: store account or account list data in a file in storage folder

        :Parameter:
					:id: string - :default: ''
					:data: dictionary - :default: {}
					:list: boolean - :default: false
        :Return: Boolean
	''' 
	def store(self,id:str='',data:dict={},list=False) -> bool:
		try:
			#store account information
			if(id != ''and not list):
				log.info(f'store information @ account:{id}')

				try: 
					with open(f'storage_accounts_v3/account-{id}.json','w') as file:
						json.dump(data,file,indent=4)
				except IOError:
					log.exception(f'File Error: could\'t write the json file of the account-{id}')
				except Exception as e:
					log.exception(f'Failed Error: {e}')
				return True

			#store summary list of account
			if(id == '' and list):
				log.info(f'store information @ account-list')

				try:
					with open(f'storage_accounts_v3/account-list.json','w') as file:
						json.dump(data,file,indent=4)
				except IOError:
					log.exception('File Error: could\'t write the json file of the account list')
				except Exception as e:
					log.exception(f'Failed Error: {e}')
				return True

		except Exception as e:
			log.exception(f'File Error: Unable to Write File')

	'''
        :Description: delete a account from account list data and file in storage folder

        :Parameter:
					:id: string - :default: ''
        :Return: Boolean
	''' 
	def delete(self,id:str) -> bool:
		
		if self.validate_id(id):

			try:
				os.remove(f'storage_accounts_v3/account-{id}.json')
				log.info('Remove the file in the storage folder')
			except Exception as e:
				log.exception(f'File Error: Account-{id} could\'nt find in the account list ->{e}')
			
			try:
				with open(f'storage_accounts_v3/account-list.json','r') as file: 
					acc_list:dict = json.load(file)
				log.info(f'Opening Account list to remove the record of the account-{id}')
			except IOError:
				log.exception('File Error: could\'t read the json file of the account list')
			except Exception as e:
				log.exception(f'Failed Error: {e}')

			if acc_list == {} or acc_list == None:
				return False

			for acc_id in acc_list['Account-List']:
				if acc_id['Account-ID'] == id:
					acc_list['Account-List'].remove(acc_id)
					log.info(f'Successfully removing the record of the account-{id} in the account list')

			json.dump(acc_list,open(f'storage_accounts_v3/account-list.json','w'),indent=4)	
			
			# free memory from the storage
			del acc_list
			
			log.info(f'File Execution: Success Deleting Account-{id}')
			return True
		
		log.info(f'File Execution: Failed to Deleting Account-{id}')
		return False
		

	'''
        :Description: verify the account in account list data

        :Parameter:
					:id: string - :default: ''
        :Return: Boolean
	''' 
	def validate_id(self,id:str) -> bool:
		acc_list:dict = {}
		try:
			#fetch account information
			if id != '':
				log.info(f'fetch information @ account:{id}')

				try:
					with open(f'storage_accounts_v3/account-list.json','r') as file:
						acc_list = json.load(file)
				except IOError:
					log.exception('File Error: could\'t read the json file of the account list')
				except Exception as e:
					log.exception(f'Failed Error: {e}')

		except Exception as e:
			log.exception(f'File Error: Non-existing File')

		if acc_list != {}:

			for acc_id in acc_list['Account-List']:
				if acc_id['Account-ID'] == id:
					del acc_list
					return True
				
		del acc_list
		return False
