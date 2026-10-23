import unittest
from tools.gateway_probe import probe

class GatewayProbeTests(unittest.TestCase):
    def test_rejects_public_address(self):
        with self.assertRaises(ValueError):
            probe("8.8.8.8", ports=())

    def test_accepts_private_address_without_ports(self):
        self.assertEqual(probe("192.168.12.1", ports=())["ports"], [])

if __name__ == "__main__":
    unittest.main()
