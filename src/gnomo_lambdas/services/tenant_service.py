from typing import Dict
from src.gnomo_lambdas.persistence.gnomo_predictive_data_dao import GnomoPredictiveDataDAO


class TenantService:

    def __init__(self, gnomo_predictive_data_dao: GnomoPredictiveDataDAO = None):
        self.gnomo_predictive_data_dao = gnomo_predictive_data_dao or GnomoPredictiveDataDAO()

    def report_tenant(self, doc_id: str, name: str) -> Dict:
        return self.gnomo_predictive_data_dao.create(doc_id, name)
