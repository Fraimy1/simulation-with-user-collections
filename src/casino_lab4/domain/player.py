class Player:
    def __init__(self, name:str, balance:float) -> None:
        self.name: str = name
        self.balance: float = balance
    
    def __repr__(self) -> str:
        return f"Player(name={self.name}, balance={self.balance})"