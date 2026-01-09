from dialogs.breeding_facility_dialog import BreedingFacilityDialog

class FeedTradingFacilityDialog(BreedingFacilityDialog):
    def __init__(self, data=None):
        super().__init__(data)
        self.setWindowTitle("Thông tin cơ sở mua bán thức ăn chăn nuôi")
