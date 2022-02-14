class Rps:
    def __init__(self, name1, name2, bo=3):
        self.p1 = name1
        self.p2 = name2
        self.bo = bo
        self.round_number = 0
        self.p1_score = 0
        self.p2_score = 0

    def rnd(self, p1inp, p2inp):
        rules = {'r': 's', 's': 'p', 'p': 'r'}

        if p1inp == p2inp:
            return 'tie'

        if rules[p1inp] == p2inp:
            self.p1_score += 1
            return self.p1

        if rules[p2inp] == p1inp:
            self.p2_score += 1
            return self.p2

    def rps(self, p1inp, p2inp):
        result = self.rnd(p1inp, p2inp)

        if result == 'tie':
            return 'tie'

        else:
            self.round_number += 1

            if self.round_number == self.bo:
                if self.p1_score > self.p2_score:
                    return "Game Winner: "+str(self.p1)
                else:
                    return "Game Winner: "+str(self.p2)

            return "Round Winner: "+str(result)
