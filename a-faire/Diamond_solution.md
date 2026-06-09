---
title: "Diamond"
draft: false
date: "2021-06-18T18:04:00"
aliases:
  - "/DiamondSolution"

---

# Python

    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R","S", "T", "U", "V", "W", "X", "Y", "Z"];
    input = "E"

    index = alphabet.index(input)


    arr = alphabet[1:index] + alphabet[index:0:-1]

    total = index*2 + 1
    edge = index - 1

    print(" "*index + "A" + " "*index)
    for i in arr:
        print(" " *abs(edge) + i + " " * (total - 2 * abs(edge) - 2) + i + " " * abs(edge))
        edge = edge - 1
    print(" " * index + "A" + " " * index)


# Rust

  This is the more accurate solution for the moment for the [Diamond kata](/kata/Diamond).
  Feel free to create a merge request on the [codingdojo repository](https://gitlab.com/codingdojo-org/codingdojo.org) to improve it.

``` Rust
fn main() {
    println!("{}", make_diamond('z'));
}

fn make_diamond(character: char) -> String {
    let goal_offset = char_offset(character);
    let base = if character.is_uppercase() {'A' as u8} else {'a' as u8};
    let mut diamond = String::new();
    diamond += create_base(character).as_str();
    for i in 1..goal_offset {
        diamond += create_line((base + i) as char, character).as_str();
    }
    for i in (1..goal_offset - 1).rev() {
        diamond += create_line((base + i) as char, character).as_str();
    }
    diamond += create_base(character).as_str();
    diamond
}


fn create_line(character: char, goal: char) -> String {
    let mut line = String::new();
    let current_char_offset = char_offset(character);

    let left_spaces = char_offset(goal) - current_char_offset;
    line = make_spaces(left_spaces, line);

    line.push(character);

    let inter_spaces = 1 + (current_char_offset - 2) * 2;
    line = make_spaces(inter_spaces, line);

    line.push(character);
    line.push('\n');
    line
}

fn make_spaces(number: u8, mut string: String) -> String {
    for _ in 0..number {
        string.push(' ');
    }
    string
}

fn create_base(character: char) -> String {
    let mut string = String::new();
    string = make_spaces(char_offset(character) - 1, string);
    if character.is_uppercase() {
        string.push_str("A\n");
    } else {
        string.push_str("a\n");
    }
    string
}

fn char_offset(character: char) -> u8 {
        let base = if character.is_uppercase() { 'A' } else { 'a' };
        character as u8 - base as u8 + 1
}

#[cfg(test)]
mod tests {
    use crate::char_offset;
    #[test]
    fn char_offset_uppercase_legal() {
        assert_eq!(char_offset('A'), 1);
        assert_eq!(char_offset('E'), 5);
        assert_eq!(char_offset('Z'), 26);
    }

    #[test]
    fn char_offset_lowercase_legal() {
        assert_eq!(char_offset('a'), 1);
        assert_eq!(char_offset('e'), 5);
        assert_eq!(char_offset('z'), 26);
    }

    use crate::create_base;

    #[test]
    fn create_base_A() {
        assert_eq!(create_base('A'), String::from("A\n"));
    }

    #[test]
    fn create_base_B() {
        assert_eq!(create_base('B'), String::from(" A\n"));
    }

    #[test]
    fn create_base_C() {
        assert_eq!(create_base('C'), String::from("  A\n"));
    }

    use crate::create_line;

    #[test]
    fn create_line_previous_spaces_B() {
        assert_eq!(create_line('B', 'B'), String::from("B B\n"));
        assert_eq!(create_line('B', 'C'), String::from(" B B\n"));
        assert_eq!(create_line('B', 'E'), String::from("   B B\n"));
    }

    #[test]
    fn create_line_middle_spaces() {
        assert_eq!(create_line('C', 'C'), String::from("C   C\n"));
        assert_eq!(create_line('D', 'D'), String::from("D     D\n"));
        assert_eq!(create_line('E', 'E'), String::from("E       E\n"));
    }

    use crate::make_spaces;

    #[test]
    fn make_spaces_no() {
        let string = String::new();
        assert_eq!(make_spaces(0, string), String::from("")); 
    } 

    #[test]
    fn make_spaces_five() {
        let string = String::new();
        assert_eq!(make_spaces(5, string), String::from("     ")); 
    }

    use crate::make_diamond;

    #[test]
    fn make_diamond_A() {
        assert_eq!(make_diamond('A'), String::from("A\nA\n"));
    }

    #[test]
    fn make_diamond_a() {
        assert_eq!(make_diamond('a'), String::from("a\na\n"));
    }

    #[test]
    fn make_diamond_B() {
        assert_eq!(make_diamond('B'), String::from(" A\nB B\n A\n"));
    }

    #[test]
    fn make_diamond_C() {
        assert_eq!(make_diamond('C'),
                   String::from("  A\n B B\nC   C\n B B\n  A\n"));
    }
}
```
