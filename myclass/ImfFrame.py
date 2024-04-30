from pandaspro.core.frame import FramePro
import re


class ImfFrame(FramePro):
    def __getattr__(self, item):
        if re.fullmatch(r'y\d{4}', item):
            keepkey = int(re.fullmatch(r'y(\d{4})', item).group(1))
            if keepkey < 2002:
                raise ValueError('Vintage data available only after year 2002')
            else:
                return self.inlist('vintage_year', keepkey)
        elif re.fullmatch(r'y\d{4}_\d{4}', item):
            startyear = int(re.fullmatch(r'y(\d{4})_(\d{4})', item).group(1))
            endyear = int(re.fullmatch(r'y(\d{4})_(\d{4})', item).group(2))
            if startyear < 2002:
                raise ValueError('Vintage data available only after year 2002')
            else:
                return self.inlist('vintage_year', [i for i in range(startyear, endyear + 1)])
        elif re.fullmatch(r'y(\d+)', item):
            numbers = re.fullmatch(r'y(\d+)', item).group(1)
            if len(numbers) % 4 == 0:
                years = [int(numbers[i: i + 4]) for i in range(0, len(numbers), 4)]
                if any(year < 2002 for year in years):
                    raise ValueError('Vintage data available only after year 2002')
                else:
                    return self.inlist('vintage_year', years)
            else:
                raise ValueError(
                    'Enter separate vintage years in 4-digit format, eg. 200120042008 for year 2001, 2004 and 2008 April vintages')
        # Inlist with Dummies
        elif item in ['keep2018', 'keep2025']:
            return self.inlist(item.replace('keep', 'roc'), 1)
        elif item in self.columns and item not in self.idvar:
            return self[self.idvar + [item]]
        elif item in ['idvar', 'dmona', 'dmona_raw']:
            pass
        else:
            return super().__getattr__(item)