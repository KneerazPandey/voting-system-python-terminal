class Candidate:
    def __init__(self, id, name, party, address):
        self.id = id 
        self.name = name 
        self.party = party
        self.address = address
    
    @classmethod
    def from_file_line(cls, line: str):
        datas = line.split('|')
        try:
            if datas[3].endswith("\n"):
                return cls(int(datas[0]), datas[1], datas[2], datas[3].removesuffix("\n"))
            else:
                return cls(int(datas[0]), datas[1], datas[2], datas[3])
        except Exception:
            return None 
        
    def __str__(self):
        return f'{self.id}|{self.name}|{self.party}|{self.address}'
        