class ElectionSchedule:
    def __init__(self, id: int, address: str, date: str):
        self.id = id
        self.address = address 
        self.date = date 
        
    @classmethod
    def from_file_line(cls, line: str):
        datas = line.split('|')
        try:
            if datas[2].endswith('\n'):
                date = datas[2].removesuffix("\n")
                return cls(int(datas[0]), datas[1].strip(), date.strip())
            else:
                return cls(int(datas[0]), datas[1].strip(), datas[2].strip().removesuffix("\n"))
        except Exception:
            return None 
        
    def __str__(self):
        return f'{self.id}|{self.address}|{self.date}'