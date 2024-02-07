from .Helper import SupersaasTest

class PromotionsTest(SupersaasTest):

    def test_promotion(self):
        promotion_code = "ab1235"
        self.assertIsNotNone(self.client.promotions.promotion(promotion_code))

    def test_list(self):
        self.assertIsNotNone(self.client.promotions.list(10, 10))

    def test_duplicate_promotion_code(self):
        new_promotion_code = "u123"
        template_code = "33aa44"
        self.assertIsNone(
            self.client.promotions.duplicate_promotion_code(
                new_promotion_code, template_code))
