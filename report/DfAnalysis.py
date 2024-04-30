from sprnldata.myclass.ImfFrame import ImfFrame


class DfAnalysis(ImfFrame):
    def __init__(
            self,
            *args,
            monav: str = 'latest',
            ecosv: str = 'latest',
            weovintagev: str = 'latest',
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.monav = monav
        self.ecosv = ecosv
        self.weovintagev = weovintagev
