from dialogs.breeding_facility_dialog import BreedingFacilityDialog

class FeedFacilityDialog(BreedingFacilityDialog):
    def __init__(self, data=None):
        super().__init__(data)
        self.setWindowTitle("Thông tin cơ sở sản xuất thức ăn chăn nuôi")
