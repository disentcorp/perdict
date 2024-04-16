import unittest

from tests.test_perdict import Test_Perdict


def test_suite():
    """
    add test cases into suite

    """

    suite = unittest.TestSuite(
        [unittest.TestLoader().loadTestsFromTestCase(Test_Perdict)]
    )

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    suite = test_suite()
    runner.run(suite)
