from sprnldata.myclass.mona.ClassDescription import MonaDes
from sprnldata.myclass.ecosdata import EcosData
from sprnldata.myclass.weovintage import WeoVinage


class DfAnalysis:
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

        self.monadata_d = MonaDes(version=self.monav)
        self.ecosdata = EcosData(version=self.ecosv)
        self.weovintagedata = WeoVinage(version=self.weovintagev)

