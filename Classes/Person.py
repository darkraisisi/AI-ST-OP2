from random import choice # pakt een willekeurigee element van een lijst

# Class Person definieer een bepaalde persoon die door de lift
#  van een bepaalde verdiepeing naar een andere verdieping moet gaan.
class Person:

    def __init__(self,startFlr,amntFlrs):
        self.startFloor = startFlr # de verdieping waar die zich bevind.
        self.destinationFloor = choice([i for i in range(1,amntFlrs) if i not in [startFlr]]) # willekeurige verdieping gepakt die niet geliujk is aan de startFloor

    # Print de verdieping waar de persoon zich bevind en de verdieping waar hij wilt gaan.
    def print(self):
        print(f'StartFloor: {self.startFloor}, Destination: {self.destinationFloor}') 