from getpass import getpass
from . core import is_dob_valid


def prompt_name(prompt_for, is_add=True):
    is_name_invalid = True

    
    while(is_name_invalid):
        name: str = input(f'{prompt_for}')
        if not is_add:
            if len(name) <= 1 and name == '?':
                return '?'
            
        if len(name) <= 3:
            print('\n❌ Name must be greater then 3 character. ❌\n')
        else:    
            return name 
        

            
def prompt_address(prompt_for, is_add=True,):
    is_address_invalid = True
        
    while(is_address_invalid):
        address = input(f'{prompt_for}')
        
        if not is_add:
            if len(address) <= 1 and address == '?':
                return '?'
        
        if len(address) <= 3:
            print('\n❌ Address must be greater then 3 character. ❌\n')
        else:    
            return address 
        
        
def prompt_party(prompt_for, is_add=True):
    is_party_invalid = True

    
    while(is_party_invalid):
        party: str = input(f"{prompt_for}")
        if not is_add:
            if len(party) <= 1 and party == '?':
                return '?'
            
        if len(party) <= 2:
            print('\n❌ Party name must be greater then 2 character. ❌\n')
        else:    
            return party.upper() 
        

def prompt_update_id(prompt_for ,is_add=True):
    is_id_invalid = True

    
    while(is_id_invalid):
        id: str = input(f'{prompt_for}')
        try:
            id = int(id)
            return id 
        except ValueError:
            print('\n❌ Invalid ID. Please enter numeric data. ❌\n')
            

def prompt_password(prompt_for, is_add=True):
    is_password_invalid = True
        
    while(is_password_invalid):
        password = getpass(f'{prompt_for}')
        
        if not is_add:
            if len(password) <= 1 and password == '?':
                return '?'
            
        if len(password) <= 6:
            print('\n❌ password must be greater then 6 character. ❌\n')
        else:    
            return password 
        

            
def prompt_date_of_birth(prompt_for, is_add=True):
    is_date_of_birth_invalid = True
        
    while(is_date_of_birth_invalid):
        dob = input(f'{prompt_for}')
        
        if not is_add:
            if len(dob) <= 1 and dob == '?':
                return '?'
        
        if is_dob_valid(dob):
            return dob 
        else:    
            print('\n❌ Invalid Date of Birth. ❌\n')