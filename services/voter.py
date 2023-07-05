from config.constant import (
    VOTER_FILE_NAME, TEMPORARY_FILE_NAME, 
    VOTER_COUNT_FILE_NAME, ELECTION_SCHEDULE_NAME,
)
from . core import get_auto_increment_id
from . prompt import (
    prompt_name, prompt_address, prompt_password,
    prompt_date_of_birth, prompt_update_id
)
from . candidate import CandidateService
from . schedule import ElectionScheduleService
from models.voter import Voter
from models.vote_count import VoteCount
from models.election_schedule import ElectionSchedule
import os 
from datetime import date, datetime



from config.menu import Menu


class VoterService:
    CURRENT_DATE = date.today()
    
    def __init__(self) -> None:
        pass 
    
    def add(self):
        credentials = self.add_prompt()
        self._add(
            name=credentials['name'], 
            date_of_birth=credentials['date_of_birth'],
            address=credentials['address'],
            password=credentials['password'],
        )  
    
    
    def update(self):
        credentials = self.update_prompt()
        
        if not credentials.get('found', False):
            print(f'\n❌ The voter with voter id {credentials["id"]} does not exists. ❌\n')
            Menu.displayAdminMenu()
            return 
        
        self._update(
            id=credentials['id'],
            name=credentials['name'], 
            date_of_birth=credentials['date_of_birth'],
            address=credentials['address'],
            password=credentials['password'],
        ) 
        
    
    def delete(self):
        id = self.delete_prompt()
        self._delete(id)
        
    
    def search(self):
        id = self.search_prompt()
        self._search(id) 
        
    
    def cast_vote(self):
        datas = self.cast_vote_prompt()
        id = datas['id']
        password = datas['password']
        
        if self.is_credentials_valid(id=id, password=password):
            self._cast_vote()
        else:
            print('\n❌ Invalid username or password. ❌\n')
            Menu.displayMainMenu()
        
    
    def _add(self, name, date_of_birth, address, password):
        id = get_auto_increment_id(VOTER_FILE_NAME)
        
        try:
            with open(VOTER_FILE_NAME, 'a') as file:
                voter_detail = f'{id}|{name}|{date_of_birth}|{address}|{password}\n'
                file.write(voter_detail) 
                print('----------------------------------------------')
                print('✔️       Voter Registered Successfully      ✔️')
                print('----------------------------------------------')
                Menu.displayMainMenu()
                
        except FileNotFoundError:
            print('\n❌ The voter file does not exist. ❌\n')
            Menu.displayAdminMenu()
        except PermissionError:
            print('\n❌ The voter file does not have read/write permission. ❌\n')
            Menu.displayAdminMenu()
            
            
    def _update(self, id, name, date_of_birth, address, password):
        found = False 
        try:
            with open(VOTER_FILE_NAME, 'r') as file:
                with open(TEMPORARY_FILE_NAME, 'a') as temp_file:
                    for line in file:
                        voter = Voter.from_file_line(line)
                        if not voter:
                            continue
                        
                        if voter.id != id:
                            existing_voter_detail = f'{voter.id}|{voter.name}|{voter.date_of_birth}|{voter.address}|{voter.password}\n'
                            temp_file.write(existing_voter_detail)
                        else:
                            found = True 
                            _name = voter.name if name == '?' else name 
                            _date_of_birth = voter.date_of_birth if date_of_birth == '?' else date_of_birth
                            _address = voter.address if address == '?' else address
                            _password = voter.password if password == '?' else password
                            new_voter_detail = f'{voter.id}|{_name}|{_date_of_birth}|{_address}|{_password}\n'
                            temp_file.write(new_voter_detail)
            
            
            if found:
                os.remove(VOTER_FILE_NAME)
                os.rename(TEMPORARY_FILE_NAME, VOTER_FILE_NAME)
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
            print('\n❌ The voter file does not have read/write permission. ❌\n') 
            Menu.displayAdminMenu()
            
    
    def _delete(self, id):
        exists = False 
        
        try:
            with open(VOTER_FILE_NAME, 'r') as file:
                with open(TEMPORARY_FILE_NAME, 'a') as temp_file:
                    for line in file: 
                        voter: Voter = Voter.from_file_line(line)
                        if not voter:
                            continue
                        
                        if voter.id == id:
                            exists = True
                        else:
                            candidate_details = f'{voter.id}|{voter.name}|{voter.date_of_birth}|{voter.address}|{voter.password}\n'
                            temp_file.write(candidate_details)
            
                    
            if exists:
                os.remove(VOTER_FILE_NAME)
                os.rename(TEMPORARY_FILE_NAME, VOTER_FILE_NAME)
                print('-------------------------------------------------')
                print('✔️         Voter deleted successfully          ✔️')
                print('-------------------------------------------------')
            else:
                print(f'\n❌ The voter with id {id} does not exists to be deleted. ❌\n') 
            
            Menu.displayAdminMenu()  
        
        except FileNotFoundError:
            print(f'\n❌ The voter file does not exists. ❌\n') 
            Menu.displayAdminMenu()
        except PermissionError:
            print(f'\n❌ The voter file does not have read/write permission. ❌\n') 
            Menu.displayAdminMenu()
            
    
    def _cast_vote(self):
        if not self.is_election_today():
            print('\n❌ There is no voting todays. Please view the voting details ❌\n')
            election_schedule_service = ElectionScheduleService()
            election_schedule_service.list()
            Menu.displayMainMenu()
            return
        
        if self.has_already_cast_vote():
            print('\n❌ You have already cast todays vote. ❌\n')
            Menu.displayMainMenu()
            return
        
        candidate_service = CandidateService()
        candidate_service.list()
        
        candidate_id = self.candidate_prompt()
        candidate = candidate_service.get_candidate_by_id(id=candidate_id)
        
        if not candidate:
            print('\n❌ The candidate you want to vote does not exists. ❌\n')
            Menu.displayMainMenu()
            return
        
        found = False 
        temp_file = open(TEMPORARY_FILE_NAME,'a+')
        voting_date = f'{VoterService.CURRENT_DATE.year}/{VoterService.CURRENT_DATE.month}/{VoterService.CURRENT_DATE.day}'
        try:
            
            with open(VOTER_COUNT_FILE_NAME, 'r') as file:
                for line in file:
                    vote_count: VoteCount = VoteCount.from_file_line(line)
                    if vote_count.candidate.id == candidate_id:
                        found = True
                        result = f'{vote_count.candidate.id}|{vote_count.candidate.name}|{vote_count.candidate.party}|{vote_count.candidate.address}|{voting_date}|{vote_count.count + 1}\n'
                        temp_file.write(result)  
                    else:
                        result = f'{vote_count.candidate.id}|{vote_count.candidate.name}|{vote_count.candidate.party}|{vote_count.candidate.address}|{voting_date}|{vote_count.count}\n'  
                        temp_file.write(result)
        except FileNotFoundError:
            result = f'{candidate_id}|{candidate.name}|{candidate.party}|{candidate.address}|{voting_date}|1\n'  
            temp_file.write(result)
            temp_file.close()
            found = True 
            
        if not found:
            result = f'{candidate_id}|{candidate.name}|{candidate.party}|{candidate.address}|{voting_date}|1\n'  
            temp_file.write(result)
        
        temp_file.close()
        if os.path.exists(VOTER_COUNT_FILE_NAME):
            os.remove(VOTER_COUNT_FILE_NAME)
        
        if os.path.exists(TEMPORARY_FILE_NAME):
            os.rename(TEMPORARY_FILE_NAME, VOTER_COUNT_FILE_NAME)
        
        print('----------------------------------------------------')
        print('✔️      You have successfully cast your vote      ✔️')
        print('----------------------------------------------------')
        
        Menu.displayMainMenu()
                
    
    
    def _search(self, id):
        found = False 
        
        try:
            with open(VOTER_FILE_NAME, 'r') as file:
                for line in file:
                    voter: Voter = Voter.from_file_line(line)
                    if not voter:
                        continue
                    
                    if voter.id == id:
                        found = True
                        print()
                        print('✔️        Voter Details       ✔️')
                        print('----------------------------------')
                        print(f'Voter ID: {voter.id}')
                        print(f'Voter Name: {voter.name}')
                        print(f'Voter Address: {voter.address}')
                        print(f'Voter Date of Birth: {voter.date_of_birth}')
                        print(f'Voter Password: {voter.password}\n\n')
                        break
            
            if not found:
                print(f'\n❌ The voter with id {id} does not exists. ❌\n') 
                
            Menu.displayAdminMenu()
            
        except FileNotFoundError:
            print(f'\n❌ The voter file does not exists. ❌\n') 
            Menu.displayAdminMenu()
        except PermissionError:
            print(f'\n❌ The voter file does not have read/write permission. ❌\n') 
            Menu.displayAdminMenu()
            
    
    
    def add_prompt(self):
        name = prompt_name(prompt_for='Enter voter name: ')
        date_of_birth = prompt_date_of_birth(prompt_for='Enter voter date of birth(yyyy/mm/dd): ')
        address = prompt_address(prompt_for='Enter voter address: ')
        password = prompt_address(prompt_for='Enter voter password: ')
        
        return {
            'name': name,
            'date_of_birth': date_of_birth,
            'address': address,
            'password': password, 
        }
        
    def update_prompt(self):
        id = prompt_update_id(prompt_for='Enter voter id to be updated: ')
        
        if self.get_voter_by_id(id=id) is None:
            return {'id': id, 'found': False }
        
        name = prompt_name(is_add=False, prompt_for='Enter new voter name: ')
        date_of_birth = prompt_date_of_birth(is_add=False, prompt_for='Enter new voter date of birth(yyyy/mmdd): ')
        address = prompt_address(is_add=False, prompt_for='Enter new voter address: ')
        password = prompt_password(is_add=False, prompt_for='Enter new password: ')
        
        return {
            'id': id,
            'name': name,
            'date_of_birth': date_of_birth,
            'address': address,
            'password': password, 
            'found': True,
        }
        
    def delete_prompt(self):
        id = prompt_update_id(prompt_for='Enter voter id to be deleted: ')
        
        return id 
    
    
    def search_prompt(self):
        id = prompt_update_id(prompt_for='Enter voter id for search: ')
        
        return id 
    

    def cast_vote_prompt(self):
        id = prompt_update_id(prompt_for='Enter your id: ')
        password = prompt_password(prompt_for='Enter your password: ')
        
        return {
            'id': id,
            'password': password,
        }
        
    
    def candidate_prompt(self):
        id = prompt_update_id(prompt_for='Enter candidate id for voting: ')
        
        return id 
    

    def get_voter_by_id(self, id):
        try:
            with open(VOTER_FILE_NAME, 'r') as file:
                for line in file:
                    voter: Voter = Voter.from_file_line(line)
                    if not voter:
                        continue
                    
                    if voter.id == id:
                        return voter
                    
        except FileNotFoundError:
            print(f'\n❌ Unable to open {VOTER_FILE_NAME} file. ❌\n') 
            return None 
        except PermissionError:
            print(f'\n❌ Permission denied in {VOTER_FILE_NAME} file. ❌\n') 
            return None
        except Exception:
            print(f'\n❌ Error occured while reading {VOTER_FILE_NAME} file. ❌\n')
            return None 
         
        
    
    def is_credentials_valid(self, id, password):
        try:
            with open(VOTER_FILE_NAME, 'r') as file:
                for line in file:
                    voter: Voter = Voter.from_file_line(line)
                    if voter.id == id and voter.password == password:
                        return True 
        
            return False 
        except FileNotFoundError:
            print(f'\n❌ The voter file does not exists. ❌\n') 
            return False
        except PermissionError:
            print(f'\n❌ The voter file does not have read/write permission. ❌\n') 
            return False
        
    
    def has_already_cast_vote(self):
        try:
            with open(VOTER_COUNT_FILE_NAME, 'r') as file:
                for line in file:
                    vote_count = VoteCount.from_file_line(line)
                    voting_date = date.strftime(vote_count.vote_date, '%Y/%m/%d')
                    if voting_date == VoterService.CURRENT_DATE: 
                        return True 
        
            return False 
        except FileNotFoundError:
            print(f'\n❌ The voter file does not exists. ❌\n') 
            return False
        except PermissionError:
            print(f'\n❌ The voter file does not have read/write permission. ❌\n') 
            return False
        
        
    def is_election_today(self):
        try:
            with open(ELECTION_SCHEDULE_NAME, 'r') as file:
                for line in file:
                    election_schedule: ElectionSchedule = ElectionSchedule.from_file_line(line)
                    if not election_schedule:
                        continue
                    
                    if election_schedule.date == VoterService.CURRENT_DATE:
                        return True 
            
            return False

        except FileNotFoundError:
            print('\n❌ The election schedule file does not found ❌\n')
            Menu.displayMainMenu()
            return False
            

            