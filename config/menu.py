from . import constant

class Menu:
    @staticmethod
    def displayWelcomeMessage():
        print('+-+-+-+-+-+-+-+ +-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+')
        print('|W|E|L|C|O|M|E| |T|O| |V|O|T|I|N|G| |S|Y|S|T|E|M|')
        print('+-+-+-+-+-+-+-+ +-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+ ')
    
    @staticmethod
    def displayMainMenu():
        print("1 ➟  Admin")
        print("2 ➟  Voter Register")
        print("3 ➟  Cast Vote")
        print("4 ➟  Exit")
        
    @staticmethod
    def displayAdminMenu():
        print("1  ➟   Election Schedule")
        print("2  ➟   Candidate Registration")
        print("3  ➟   Candidate Update")
        print("4  ➟   Delete Candidate")
        print("5  ➟   List of Candidate")
        print("6  ➟   Update Voter")
        print("7  ➟   Delete Voter")
        print("8  ➟   Voter Serarch")
        print("9  ➟   Voter Result")
        print("10 ➟   List of Election Schedule")
        print("11 ➟   Logout")