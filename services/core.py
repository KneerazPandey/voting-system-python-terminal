def get_auto_increment_id(file_name: str) -> int:
    current_id = 1
    
    try:
        with open(file_name, 'r') as file:
            last_line = ''
            for line in file:
                last_line = line

            items =  last_line.split('|')
            try:
                return int(items[0]) + 1
            except:
                return current_id 
    except FileNotFoundError:
        return current_id
    except PermissionError:
        return current_id
    

def is_dob_valid(dob: str):
    datas = dob.split('/')

    try:
        year = datas[0]
        month = datas[1]
        day = datas[2]
        
        if len(year) == 4 and len(month) == 2 and len(day) == 2:
            try:
                y = int(year) 
                m = int(month) 
                d = int(day)
                return True
            except ValueError:
                print('fifth')
                return False
        
        return False  
    except IndexError:
        print('second')
        return False
