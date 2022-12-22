# chinese-names

This is a simple library to parse Chinese names into surname + given name.
It can also guess the gender from the given name. Chinese names are less
strictly separated by gender than in many other cultures, but in this way it
is possible to get an educated guess. The library was orginally created for a
project that involved identifying the genders of authors when the only
information available was their names.

The gender estimates are based on character-level statistics from names of
people born 1930-2008 in mainland China.

## Installing

    pip install --user .

## Usage

    >>> from chinese_names import ChineseNames
    >>> cn = ChineseNames()
    >>> cn.parse("诸葛亮")
    ChineseName(surname='诸葛', given_name='亮', p_male=0.9480300169983071, p_female=0.051969983001692865, p_name=1.3000188515699997e-07)
    >>> cn.parse("Freddy Foreigner")
    >>>

Note that `p_name` is the total name probability from a unigram character
model. Thus it is generally a rather low value. You should be able to get a
very rough approximation of the expected number of bearers, given naive
independence assumptions, by multiplying with population size. For the PRC:

    >>> 1.412e9 * cn.parse("王伟").p_name
    1399604.0484204555
    >>> 1.412e9 * cn.parse("诸葛亮").p_name
    183.56266184168396

## Data

Data is obtained from [the ChineseNames R library]([https://github.com/psychbruce/ChineseNames]) under a CC-BY-NC-SA license.

