import unittest

class TestReverseFizzBuzz(unittest.TestCase):
    def test_fizz(self):
        self.assertEqual(reverse_fizzbuzz("Fizz"), 3)

    def test_buzz(self):
        self.assertEqual(reverse_fizzbuzz("Buzz"), 5)

    def test_fizzbuzz(self):
        self.assertEqual(reverse_fizzbuzz("FizzBuzz"), 15)

    def test_number(self):
        self.assertEqual(reverse_fizzbuzz("7"), 7)
        self.assertEqual(reverse_fizzbuzz("101"), 101)

if __name__ == "__main__":
    unittest.main()
