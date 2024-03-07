from pandaspro import FramePro
import sprnldata.core.config as c


class ImfFrame(FramePro):
    def __getattr__(self, item):
        if item in c.imfattribute.keys():
            return self.__class__(
                data=self.inlist(c.imfattribute[item]['var'], c.imfattribute[item]['value']))
        elif item not in []:
            super().__getattribute__(item)
