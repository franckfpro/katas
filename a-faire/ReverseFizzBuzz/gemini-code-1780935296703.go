package kata

import "testing"

func TestReverseFizzBuzz(t *testing.T) {
	tests := []struct {
		input    string
		expected int
	}{
		{"Fizz", 3},
		{"Buzz", 5},
		{"FizzBuzz", 15},
		{"7", 7},
		{"101", 101},
	}

	for _, tc := range tests {
		t.Run(tc.input, func(t *testing.T) {
			result := ReverseFizzBuzz(tc.input)
			if result != tc.expected {
				t.Errorf("Pour %s, attendu %d, mais obtenu %d", tc.input, tc.expected, result)
			}
		})
	}
}
