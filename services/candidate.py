from . prompt import (
    prompt_name, prompt_address, prompt_party,
    prompt_update_id
)
from . core import get_auto_increment_id
from config.menu import Menu
from config.constant import CANDIDATE_FILE_NAME, TEMPORARY_FILE_NAME
from models.candidate import Candidate
import os
from tabulate import tabulate


class CandidateService:
    def add(self):
        credentials = self.add_prompt()
        self._add(
            name=credentials['name'], 
            party=credentials['party'],
            address=credentials['address'],
        ) 
    
    def update(self):
        credentials = self.update_prompt()
        if not credentials.get('found', False):
            print(f'\n❌ The candidate with candidate id {credentials["id"]} does not exists. ❌\n')
            Menu.displayAdminMenu()
            return 
        
        self._update(
            id=credentials['id'],
            name=credentials['name'], 
            party=credentials['party'],
            address=credentials['address'],
        )
        
    
    def delete(self):
        id = self.delete_prompt()
        self._delete(id)
        
    
    def list(self):
        datas = [
            ["ID", "Name", "Party", "Address"]
        ]
        with open(CANDIDATE_FILE_NAME, 'r') as file:
            for line in file:
                candidate: Candidate = Candidate.from_file_line(line)
                if candidate:
                    datas.append(line.removesuffix("\n").split("|"))
                
        print(tabulate(datas, headers='firstrow'))
        
    
    def _add(self, name, party, address):
        id = get_auto_increment_id(CANDIDATE_FILE_NAME)
        
        try:
            with open(CANDIDATE_FILE_NAME, 'a') as file:
                candidate_detail = f'{id}|{name}|{party}|{address}\n'
                file.write(candidate_detail) 
                
            print('-----------------------------------------------')
            print('✔️     Candidate Registered Successfully     ✔️')
            print('-----------------------------------------------')
            Menu.displayAdminMenu()
        except FileNotFoundError:
            print('\n❌ The candidate file does not exist. ❌\n')

            
    def _update(self, id, name, party, address):
        found = False 
        try:
            with open(CANDIDATE_FILE_NAME, 'r') as file:
                with open(TEMPORARY_FILE_NAME, 'a') as temp_file:
                    for line in file:
                        candidate: Candidate = Candidate.from_file_line(line)
                        if not candidate:
                            continue
                        
                        if candidate.id != id:
                            existing_candidate_detail = f'{candidate.id}|{candidate.name}|{candidate.party}|{candidate.address}\n'
                            temp_file.write(existing_candidate_detail)
                        else:
                            found = True 
                            _name = candidate.name if name == '?' else name 
                            _address = candidate.address if address == '?' else address
                            _party = candidate.party if party == '?' else party
                            new_candidate_detail = f'{candidate.id}|{_name}|{_party}|{_address}\n'
                            temp_file.write(new_candidate_detail)
            
            
            if found:
                os.remove(CANDIDATE_FILE_NAME)
                os.rename(TEMPORARY_FILE_NAME, CANDIDATE_FILE_NAME)
                print('-------------------------------------------------')
                print('✔️      Voter Details Updated Successfully     ✔️')
                print('-------------------------------------------------')
            else:
                print(f'\n❌ The voter with voter id {id} does not exists. ❌\n') 
            
            Menu.displayAdminMenu()
        except FileNotFoundError:
            print('\n❌ The voter file does not exist. ❌\n') 
            Menu.displayAdminMenu()
        except PermissionError:
            print('\n❌ The file currently does not have read/write permission. ❌\n') 
            Menu.displayAdminMenu()
    
    def _delete(self, id):
        exists = False 
        try:
            with open(CANDIDATE_FILE_NAME, 'r') as file:
                with open(TEMPORARY_FILE_NAME, 'a') as temp_file:
                    for line in file: 
                        candidate: Candidate = Candidate.from_file_line(line)
                        if not candidate:
                            continue
                        
                        if candidate.id == id:
                            exists = True
                        else:
                            candidate_details = f'{candidate.id}|{candidate.name}|{candidate.party}|{candidate.address}\n'
                            temp_file.write(candidate_details)
                            
            if exists:
                os.remove(CANDIDATE_FILE_NAME)
                os.rename(TEMPORARY_FILE_NAME, CANDIDATE_FILE_NAME)
                print('-------------------------------------------------')
                print('✔️      Candidate deleted successfully        ✔️')
                print('-------------------------------------------------')
            else:
                print(f'\n❌ The candidate with id {id} does not exists to be deleted. ❌\n') 
            
            Menu.displayAdminMenu()  
            
        except FileNotFoundError:
            print(f'\n❌ The file does not exist to be read. ❌\n') 
            Menu.displayAdminMenu()
        except PermissionError:
            print(f'\n❌ The file does not have read/write permission. ❌\n')  
            Menu.displayAdminMenu()
    
    def add_prompt(self):
        name = prompt_name(prompt_for='Enter candidate naem: ')
        address = prompt_address(prompt_for='Enter candidate address: ')
        party = prompt_party(prompt_for='Enter candidate party: ')
        
        return {
            'name': name,
            'address': address,
            'party': party, 
        }
        
    def update_prompt(self):
        id = prompt_update_id(prompt_for='Enter candidate id: ')
        
        if not self.get_candidate_by_id(id=id):
            return {'id': id, 'found': False }
        
        name = prompt_name(is_add=False, prompt_for='Enter new candidate name: ')
        address = prompt_address(is_add=False, prompt_for='Enter new candidate address: ')
        party = prompt_party(is_add=False, prompt_for='Enter new candidate party: ')
        
        return {
            'id': id,
            'name': name,
            'party': party, 
            'address': address,
        }
        
    def delete_prompt(self):
        id = prompt_update_id(prompt_for="Enter candidate id to be deleted: ")
        
        return id
    

    def get_candidate_by_id(self, id):
        try:
            with open(CANDIDATE_FILE_NAME, 'r') as file:
                for line in file:
                    candidate: Candidate = Candidate.from_file_line(line)
                    if candidate.id == id:
                        return candidate
                    
        except FileNotFoundError:
            print(f'\n❌ Unable to open {CANDIDATE_FILE_NAME} file. ❌\n') 
            return None 
        except PermissionError:
            print(f'\n❌ Permission denied in {CANDIDATE_FILE_NAME} file. ❌\n') 
            return None
        except Exception:
            print(f'\n❌ Error occured while reading {CANDIDATE_FILE_NAME} file. ❌\n')
            return None 
         
        return None
            