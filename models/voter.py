from services.core import is_dob_valid

class Voter:
    def __init__(self, id, name, date_of_birth, address, password):
        self.id = id 
        self.name = name 
        self.date_of_birth = date_of_birth
        self.address = address
        self.password = password
        
    @classmethod
    def from_file_line(cls, line: str):
        data = line.split('|')
        try:
            if data[4].endswith("\n"):
                return cls(int(data[0]), data[1], data[2], data[3], data[4].removesuffix("\n"))
            else:
                return cls(int(data[0]), data[1], data[2], data[3], data[4])
        except Exception:
            return None
        
    def __str__(self):
        return f'{self.id}|{self.name}|{self.date_of_birth}|{self.address}|{self.password}'