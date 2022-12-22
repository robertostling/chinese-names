import csv
import os.path
from collections import namedtuple


ChineseName = namedtuple(
        'ChineseName', 'surname given_name p_male p_female p_name')

class ChineseNames:
    # This is a hack that will not work in all circumstances, unfortunately
    # there is only a good solution since Python 3.10 that does not include
    # adding extra dependencies:
    # https://setuptools.pypa.io/en/latest/userguide/datafiles.html
    def __init__(
            self,
            data_path=os.path.join(os.path.dirname(__file__), 'data')):
        self.surname = {}
        self.namechar = {}
        with open(os.path.join(data_path, 'familyname.csv'), newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.surname[row['surname']] = row

        with open(os.path.join(data_path, 'givenname.csv'), newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.namechar[row['character']] = row

    def parse(self, s):
        """Parse a name in simplified Chinese characters

        Args:
            s -- name using simplified Chinese characters

        Returns:
            a ChineseName object, or None if it does not seem to be a Chinese
            name at all.
        """

        if 2 <= len(s) <= 4:
            hypotheses = []
            # Currently we assume both a surame and a given name, but this
            # could be modified to allow only surnames/given names.
            for surname_length in (1, 2):
                surname = s[:surname_length]
                given_name = s[surname_length:]
                p_surname = 0.0
                if surname in self.surname:
                    p_surname = 1e-6*float(
                            self.surname[surname]['ppm.1930_2008'])
                p_male = 1.0
                p_female = 1.0
                p_given = 1.0
                for c in given_name:
                    row = self.namechar.get(c)
                    if row is None:
                        p_given *= 1e-6
                    else:
                        p_given *= 1e-6*float(row['name.ppm'])
                        n_male = int(row['n.male'])
                        n_female = int(row['n.female'])
                        p_male *= n_male / (n_male+n_female)
                        p_female *= n_female / (n_male+n_female)
                if p_surname != 0:
                    hypotheses.append(ChineseName(
                        surname=surname,
                        given_name=given_name,
                        p_male=p_male/(p_male+p_female),
                        p_female=p_female/(p_male+p_female),
                        p_name=p_surname*p_given))
            if not hypotheses:
                # In effect, only accept surnames from the list
                return None
            return max(hypotheses, key=lambda h: h.p_name)
        else:
            # Non-typical name lengths are not handled
            return None


def main():
    import sys
    db = ChineseNames()
    for form in sys.argv[1:]:
        name = db.parse(form)
        if name is None:
            print(f'{form} is unlikely to be a name')
        else:
            print(f'{name.surname} {name.given_name} '
                    f'P(name) = {name.p_name:.3g} '
                    f'P(male) = {100*name.p_male:.2f}%')


if __name__ == '__main__': main()

