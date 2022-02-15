from datetime import date, datetime

from core.models import Teste, Teste2

if __name__ == "__main__":
    # a = Teste2(campo1=1, campo2="abc123", campo3=1500.77, campo4=datetime.now())
    a = Teste2(
        trancode="00000000000000000000001abc123             0000000000015007720220214084636"
    )
    b = a.from_trancode()
    print(a.to_trancode())
