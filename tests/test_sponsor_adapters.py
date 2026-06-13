import unittest

from app.sponsors import daytona, videodb


class SponsorAdapterTests(unittest.TestCase):
    def test_videodb_fixture_keeps_existing_manifest(self):
        existing = [{"scene_id": "s00", "t_start": 0, "t_end": 4}]

        manifest, receipt = videodb.ingest_creative(
            source=None,
            existing_manifest=existing,
            scenario={"brand": "MerlionTel", "campaign": "Test"},
            mode="fixture",
        )

        self.assertEqual(manifest, existing)
        self.assertIsNone(receipt)

    def test_daytona_fixture_does_not_create_sandboxes(self):
        agents = [{"agent_id": "auntie_1", "kind": "persona", "label": "Auntie"}]

        copied, receipts = daytona.attach_receipts(
            agents,
            mode="fixture",
            enabled=True,
        )

        self.assertEqual(copied, agents)
        self.assertEqual(receipts, [])
        self.assertIsNot(copied[0], agents[0])


if __name__ == "__main__":
    unittest.main()
