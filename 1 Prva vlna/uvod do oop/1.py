from typing import List


class Person():
    def __init__(self,
                 person_id: int,
                 name: str,
                 age: int,
                 accounts: List['Account']):  # '' protože typ bude definován
        self.person_id: int = person_id
        self.name: str = name
        self.age: int = age
        self.accounts: List['Account'] = accounts
    
    def check_integrity(self) -> bool:
        for i in self.accounts:
            if i.owner != self:
                return False
        if self.age < 18:
            return False
        elif self.name == "":
            return False
        else:
            return True


class Account():
    def __init__(self,
                account_id: int, 
                password: str,
                balance: int,
                limit: int,
                owner: Person):
        self.account_id: int = account_id
        self.password: str = password
        self.balance: int = balance
        self.limit: int = limit
        self.owner: Person = owner

    def add_balance(self, password: str, amount: int) -> bool:
        if password == self.password and amount + self.balance < self.limit:
            self.balance += amount
            return True
        else:
            return False
    
    def withdraw_balance(self, password: str, amount: int) -> bool:
        if password == self.password and amount < 100000:
            if self.balance - amount < 0:
                return False
            else:
                self.balance -= amount
                return True
        else:
            return False
    
    def set_limit(self, password: str, new_limit: int) -> bool:
        if password == self.password:
            self.limit = new_limit
            return True
        else:
            return False
    
    def total_remaining(self) -> int:
        return self.balance

ja = Person(1, "Lubo", 20, [])
ucet = Account(2, "heslo", 20, 30, ja)
ja.accounts = [ucet]
print(ja.check_integrity())
print(ucet.add_balance("heslo", 5))
#ucet = Account(2, "heslo", 15, 20, )
#ucet2 = Account(3, "heslo2", 30, 50, "Lubomir")
#ucet3 = Account(4, "heslo3", 20, 30, "Lubko")
#ja = Person(1, "Lubko", 20, [ucet, ucet3])
#ja2 = Person(5, "Lubomir", 30, [ucet2, ucet])
#print(ucet.add_balance("heslo", 3))
#print(ucet.total_remaining())
#print(ja.check_integrity())
#print(ja2.check_integrity())