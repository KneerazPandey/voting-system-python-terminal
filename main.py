from config.menu import Menu
from services.voter import VoterService
from services.admin import AdminService


def run():
    Menu.displayWelcomeMessage()
    Menu.displayMainMenu()
    
    isRunning = True 
    voter_service = VoterService()
    admin_service = AdminService()
    while isRunning:
        choice = input('Enter choice: ')
        try:
            choice = int(choice)
            if choice == 1:
                admin_service.login()
            elif choice == 2:
                voter_service.add() 
            elif choice == 3:
                voter_service.cast_vote() 
            elif choice == 4:
                print('---------------------------------------------')
                print('✔️       Program Closed Successfully      ✔️')
                print('---------------------------------------------')
                isRunning = False
                break
        except ValueError:
            print('\n❌ Please choose. Please choose correct numeric data ❌\n')
            Menu.displayMainMenu()
    


if __name__ == '__main__':
    run()
