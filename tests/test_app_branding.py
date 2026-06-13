import unittest

from app.main import app


class AppBrandingTests(unittest.TestCase):
    def test_fastapi_title_uses_product_name(self):
        # Given
        expected_title = "60's Pulse"

        # When
        title = app.title

        # Then
        self.assertEqual(title, expected_title)


if __name__ == "__main__":
    unittest.main()
