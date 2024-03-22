from pandaspro import FramePro


# class ImfFrame(FramePro):
#     def __getattr__(self, item):
#         if item in c.imfattribute.keys():
#             return self.__class__(
#                 data=self.inlist(c.imfattribute[item]['var'], c.imfattribute[item]['value']))
#         elif item not in []:
#             super().__getattribute__(item)

class ImfFrame(FramePro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
