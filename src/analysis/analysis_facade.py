# analysis_facade.py
from .geographical_segmentation import GeographicalSegmentation
from .price_heat_map import PriceHeatMap
# from .tour_analysis import TourAnalysis
# from .pricing_analysis import PricingAnalysis
#... import other analysis classes

class AnalysisFacade:
    def __init__(self):
        # self.data_paths = {
        #     'geo_segmentation': 'path_to_geo_segmentation_data',
        #     'heat_map': ''
        #     # 'tour_analysis': 'path_to_tour_analysis_data',
        #     # 'pricing_analysis': 'path_to_pricing_analysis_data',
        #     # #... other data paths
        # }

        self.geographical_segmentation = GeographicalSegmentation()
        self.price_heat_map = PriceHeatMap()
        # self.tour_analysis = TourAnalysis(data_paths['tour_analysis'])
        # self.pricing_analysis = PricingAnalysis(data_paths['pricing_analysis'])



    def show_geographical_segmentation(self):
        self.geographical_segmentation.show()

    def show_heat_map(self):
        self.price_heat_map.show()

    # def show_tour_analysis(self):
    #     self.tour_analysis.show()

    # def show_pricing_analysis(self):
    #     self.pricing_analysis.show()

    #... other methods to display different analyses
