# AGENTS.md

## What this repo is
Personal collection of TDD "katas" (Codewars/Uncle Bob style), written in Python.
README mentions Go, but **no Go code exists** yet. Kata statements, comments, and
tests are in **French** — keep that language when adding or editing katas.

## Layout / status
- `a-faire/` — not done yet
- `a-revoir/` — needs review/fixes
- `fait/` — completed
Move a file between these dirs as its status changes. Do not re-solve katas in `fait/`.

## Kata file conventions
Each kata is a standalone `.py` file named after the kata in CamelCase
(`PrimeFactors.py`, `RpnCalculator.py`). A typical file holds, in order:
1. problem statement in a module docstring and/or comments (French),
2. the solution function/class,
3. a `unittest.TestCase`,
4. `if __name__ == '__main__': unittest.main()`.

To add a kata, follow the README "Transformation" workflow: translate the original
kata to French, adapt it for Python, and emit one file with the statement in
comments, the solving function, and `unittest` tests.

Exceptions worth knowing: `fait/Jukebox.py` + `Jukebox_test.py` split solution and
tests (the test imports `from jukebox import ...` in lowercase, so it fails against
the `Jukebox.py` filename on case-sensitive filesystems). `fait/RomanNumerals.py`
uses `pytest.mark.parametrize` instead of `unittest`. Some katas also have a
companion `.md` statement and/or `.ipynb` notebook (e.g. `ReverseFizzBuzz.*`).

## Running tests
- Single kata: `python3 a-faire/PrimeFactors.py` (relies on `unittest.main()`).
- `pytest` is **not installed**; `fait/RomanNumerals.py` fails at import. Convert
  such tests to `unittest` when touching them.
- Directories have hyphenated names and no `__init__.py`, so they are not importable
  packages. Run files by path; module-style invocations like `python3 -m unittest
  a-faire.PrimeFactors` do not work.

## Tooling / style
- Target Python 3.13; uses modern syntax (type hints, `match`).
- No linter, formatter, typechecker, CI, or `requirements`/manifest files exist.
- Only stdlib `unittest` is relied upon. Comments and helper names are often French
  (e.g. `ajouter_chanson`) — match the surrounding file.

## Git
- Remote: `git@github.com:franckfpro/katas.git`.
- Commit messages are terse ("more katas", "clean kata"). Do not commit unless asked.
