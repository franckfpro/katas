import unittest


def reverse_fizzbuzz(input: str) -> int:
    match input:
        case "Fizz":
            return 3
        case "Buzz":
            return 5
        case "FizzBuzz":
            return 15
        case _:
            return int(input)


def test_reverse_fizzbuzz():
    assert reverse_fizzbuzz("Fizz") == 3
    assert reverse_fizzbuzz("Buzz") == 5
    assert reverse_fizzbuzz("FizzBuzz") == 15


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
