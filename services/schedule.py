from . prompt import prompt_address, prompt_date_of_birth
from . core import get_auto_increment_id
from config.constant import ELECTION_SCHEDULE_NAME
from models.election_schedule import ElectionSchedule
from config.menu import Menu
from tabulate import tabulate
from datetime import datetime, date


class ElectionScheduleService:
    CURRENT_DATE = date.today()

    def add(self):
        credentials = self.add_prompt()
        self._add(
            address=credentials['address'],
            date=credentials['date']
        )
        
    
    def list(self):
        datas = [
            ["ID", "Address", "Date"]
        ]
        try:
            with open(ELECTION_SCHEDULE_NAME, 'r') as file:
                for line in file:
                    schedule = ElectionSchedule.from_file_line(line)
                    if schedule:
                        datas.append(line.removesuffix("\n").split("|"))
                        
            print(tabulate(datas, headers='firstrow'))
            print('\n')
            
        except FileNotFoundError:
            print(f'\n❌ The {ELECTION_SCHEDULE_NAME} file does not exists. ❌\n')
            Menu.displayAdminMenu()
        except PermissionError:
            print(f'\n❌ The {ELECTION_SCHEDULE_NAME} file does not have read/write permission. ❌\n')
            Menu.displayAdminMenu()
                
        
    
    def _add(self, address: str, date: str):
        election_date = datetime.strptime(date, '%Y/%m/%d').date()
        if not election_date >=ElectionScheduleService.CURRENT_DATE:
            print(f'\n❌ Election date must be greater or equal to current/todays date. ❌\n')
            Menu.displayAdminMenu()
            return
        
        id = get_auto_increment_id(ELECTION_SCHEDULE_NAME)
        found = False         
        try:
            with open(ELECTION_SCHEDULE_NAME, 'r') as file:
                for line in file:
                    election_schedule = ElectionSchedule.from_file_line(line)
                    if election_schedule is None:
                        print(election_schedule)
                        continue
                    
                    if election_schedule.address.lower() == address.lower() and election_schedule.date == date:
                        found = True
                        print(f'\n❌ Cannot add election schedule as it already has the same schedule at {address} on {date}. ❌\n')
                        Menu.displayAdminMenu()
                        break
            
            with open(ELECTION_SCHEDULE_NAME, 'a') as file:
                if not found:   
                    schedule = f'{id}|{address}|{date}\n'
                    file.write(schedule)
                    print('----------------------------------------------------')
                    print('✔️      Election Schedule added successfully     ✔️')
                    print('----------------------------------------------------')  
                    Menu.displayAdminMenu()
                
        except FileNotFoundError:
            print(f'\n❌ Error occured while opening {ELECTION_SCHEDULE_NAME} file. ❌\n')
            Menu.displayAdminMenu()
        except PermissionError:
            print(f'\n❌ The {ELECTION_SCHEDULE_NAME} file does not have read/write permission. ❌\n')
            Menu.displayAdminMenu()
    
    
    def add_prompt(self):
        address = prompt_address(prompt_for='Enter election address: ')
        date = prompt_date_of_birth(prompt_for='Enter election date: ')
        
        return {
            'address': address,
            'date': date,
        } 