from typing import Dict, List
from decimal import Decimal
from random import seed, random
from src.gnomo_lambdas.persistence.gnomo_predictive_data_dao import GnomoPredictiveDataDAO

seed(1)


class TenantService:

    __reported_label_coefficient = Decimal(0.8)
    __last_label_coefficient = Decimal(0.2)

    def __init__(self, gnomo_predictive_data_dao: GnomoPredictiveDataDAO = None):
        self.gnomo_predictive_data_dao = gnomo_predictive_data_dao or GnomoPredictiveDataDAO()

    def report_tenant(self, doc_id: str, name: str, metadata: Dict) -> Dict:
        if self.is_report_valid(doc_id, name, metadata):
            return self.gnomo_predictive_data_dao.create(doc_id, name, metadata, 1)
        else:
            raise RuntimeError('Invalid Report')

    def get_prediction(self, doc_id: str) -> Decimal:
        try:
            predictive_record = self.gnomo_predictive_data_dao.get(doc_id)
            reported_label = predictive_record.get('reported_label', False)
            features = predictive_record.get('processed_features', [])
            last_score = predictive_record.get('last_prediction',
                                               self.calculate_prediction(doc_id, features))

            if reported_label:
                new_score = Decimal(last_score) * self.__last_label_coefficient
                reported_score = Decimal(reported_label) * self.__reported_label_coefficient
                return new_score + reported_score
            else:
                return last_score
        except KeyError as e:
            return self.calculate_prediction(doc_id, [])

    def calculate_prediction(self, doc_id: str, features_vector: List) -> Decimal:
        # TODO Update when integrated with model, save new score
        score = random()
        return round(Decimal(score), 2)

    def get_features(self, doc_id) -> List:
        # TODO Update when integrated with data sources
        return []

    def is_report_valid(self, doc_id: str, name: str, metadata: Dict) -> bool:
        # TODO Update when integrated with data sources
        return True
