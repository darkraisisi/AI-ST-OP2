from random import uniform
class Person:
    """
        Main class that houses most of a persons logic, like political views 
    """
    def __init__(self, views=None):
        if views:
            # values between -1 & 1, 0 is exactly in the middle of the spectrum.
            self.views = views 
        else:
            self.views = self.generateViews()

    
    def generateViews(self) -> [float, float]:
        return uniform(-1, 1), uniform(-1, 1)


class Voter(Person):

    def __init__(self):
        super().__init__()
    

    def castVote(self):
        pass



class Candidate(Person):

    def __init__(self):
        super().__init__()


