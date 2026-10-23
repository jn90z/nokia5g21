import unittest
from tools.nokia_status import summarize, ENDPOINTS

class StatusTests(unittest.TestCase):
    def test_endpoints_read_only(self):
        self.assertEqual(len(ENDPOINTS), 2)
        self.assertTrue(all(path.endswith(".cgi") for path in ENDPOINTS.values()))

    def test_summary(self):
        payload = {"gateway": "192.168.12.1", "endpoints": {
            "device": {"ok": True, "data": {"device_app_status": [{"SoftwareVersion": "test", "UpTime": "1h"}]}},
            "radio": {"ok": True, "data": {"cell_LTE_stats_cfg": [{"stat": {"Band": "B2"}}], "cell_5G_stats_cfg": [{"stat": {"Band": "n41"}}]}}
        }}
        result = summarize(payload)
        self.assertEqual(result["firmware"], "test")
        self.assertEqual(result["lte_band"], "B2")
        self.assertEqual(result["nr_band"], "n41")

    def test_empty(self):
        result = summarize({"gateway": "192.168.12.1", "endpoints": {"device": {"ok": False}, "radio": {"ok": False}}})
        self.assertIsNone(result["firmware"])

if __name__ == "__main__":
    unittest.main()
