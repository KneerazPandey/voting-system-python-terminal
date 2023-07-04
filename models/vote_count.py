from . candidate import Candidate


class VoteCount:
    def __init__(self, candidate: Candidate, vote_date: str, count: int):
        self.candidate = candidate
        self.vote_date = vote_date
        self.count = count 

        
    @classmethod
    def from_file_line(cls, line: str):
        datas = line.split('|')
        try:
            cand: Candidate = Candidate(
                id=int(datas[0]),
                name=datas[1],
                party=datas[2],
                address=datas[3],
            )
            if datas[5].endswith("\n"):
                return cls(cand, datas[4], datas[5].removesuffix("\n"))
            else:
                return cls(cand, datas[4], datas[5])
        except Exception:
            return None 
        
    def __str__(self):
        return f'{self.candidate}|{self.count}'
        
    