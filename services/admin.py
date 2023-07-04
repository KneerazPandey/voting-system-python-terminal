from config.menu import Menu
from config.constant import ADMIN_USER_NAME, ADMIN_PASSWORD
from . voter import VoterService
from . candidate import CandidateService
from . schedule import ElectionScheduleService
from getpass import getpass


class AdminService:
    def login(self):        
        counter = 1
        is_valid = False 
        
        while counter <= 3:
            name = self.prompt_name()
            password = self.prompt_password()
            if name == ADMIN_USER_NAME and password == ADMIN_PASSWORD:
                is_valid = True
                break
            elif counter != 3:
                print('\n❌ Invalid username or password ❌\n')
                
            counter += 1
        
        if is_valid and counter <= 3:
            self.run()
        else:
           print('\n❌ Password Invalid for 3 times ❌\n') 
           Menu.displayAdminMenu()
        

    def run(self):
        Menu.displayAdminMenu()
        voter_service = VoterService()
        candidate_service = CandidateService()
        election_schedule_service = ElectionScheduleService()
        
        
        isRunning = True 
        while isRunning:
            choice = input('Enter choice: ')
            try:
                choice = int(choice)
                if choice == 1:
                    election_schedule_service.add()
                elif choice == 2:
                    candidate_service.add()
                elif choice == 3:
                    candidate_service.update()
                elif choice == 4:
                    candidate_service.delete() 
                elif choice == 5:
                    candidate_service.list()
                elif choice == 6:
                    voter_service.update()
                elif choice == 7:
                    voter_service.delete()
                elif choice == 8:
                    voter_service.search()
                    pass 
                elif choice == 9:
                            # print("9 ➟  Voter Result")
                    pass 
                elif choice == 10:
                    election_schedule_service.list()
                elif choice == 11:
                    print('----------------------------------------------------')
                    print('✔️       Successfully exit from admin panel      ✔️')
                    print('----------------------------------------------------')
                    Menu.displayMainMenu()
                    isRunning = False
                    break
            except ValueError:
                print('\n❌ Please choose. Please choose correct numeric data ❌\n')
                Menu.displayAdminMenu()
                
    def prompt_name(self):
        name = input('Enter admin username: ')
        return name
            
    def prompt_password(self):
        password = getpass('Enter admin password: ')
        return password