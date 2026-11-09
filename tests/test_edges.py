"""Validate sorting with an independent stack interpreter."""

from pathlib import Path
import random
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PushSwapTests(unittest.TestCase):
    def setUp(self) -> None:
        workspace = tempfile.TemporaryDirectory(prefix="push-swap-test-")
        self.addCleanup(workspace.cleanup)
        self.work = Path(workspace.name)

    def call(self, program: str, args: list[str], data: str = ""
             ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(ROOT / program), *args], input=data, text=True,
            capture_output=True, cwd=self.work, timeout=5)

    def interpret(self, values: list[int], output: str) -> None:
        stacks = [values.copy(), []]
        for op in output.splitlines():
            self.assertIn(op, ("sa", "sb", "ss", "pa", "pb", "ra", "rb",
                               "rr", "rra", "rrb", "rrr"))
            if op in ("pa", "pb"):
                target = 0 if op == "pa" else 1
                if stacks[1 - target]:
                    stacks[target].insert(0, stacks[1 - target].pop(0))
                continue
            indices = [0, 1] if op in ("ss", "rr", "rrr") else [
                1 if op.endswith("b") else 0]
            for index in indices:
                stack = stacks[index]
                if op.startswith("s") and len(stack) >= 2:
                    stack[0], stack[1] = stack[1], stack[0]
                elif op.startswith("rr") and op not in ("rr",) and stack:
                    stack.insert(0, stack.pop())
                elif op.startswith("r") and stack:
                    stack.append(stack.pop(0))
        self.assertEqual(stacks, [sorted(values), []])

    def test_empty_single_and_sorted(self) -> None:
        for args in ([], ["42"], ["-1", "0", "1"]):
            with self.subTest(args=args):
                result = self.call("push_swap", args)
                self.assertEqual((result.returncode, result.stdout,
                                  result.stderr), (0, "", ""))

    def test_all_strategies_and_integer_limits(self) -> None:
        rng = random.Random(42)
        cases = [[2, 1], [3, 2, 1], [5, 4, 3, 2, 1],
                 [-2147483648, 2147483647, 0, -1, 1],
                 list(range(20, 0, -1)), rng.sample(range(-500, 500), 40)]
        for strategy in ("--simple", "--medium", "--complex", "--adaptive"):
            for values in cases:
                with self.subTest(strategy=strategy, size=len(values)):
                    args = [strategy, *map(str, values)]
                    result = self.call("push_swap", args)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stderr, "")
                    self.interpret(values, result.stdout)
                    checked = self.call("checker", list(map(str, values)),
                                        result.stdout)
                    self.assertEqual(checked.stdout, "OK\n")

    def test_grouped_arguments(self) -> None:
        result = self.call("push_swap", ["3 1 2"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.interpret([3, 1, 2], result.stdout)

    def test_invalid_inputs(self) -> None:
        cases = [["1", "1"], ["0", "-0"], [""], ["   "], ["abc"],
                 ["1.5"], ["+"], ["-"], ["2147483648"], ["-2147483649"],
                 ["--unknown", "2", "1"]]
        for program in ("push_swap", "checker"):
            for args in cases:
                with self.subTest(program=program, args=args):
                    result = self.call(program, args)
                    self.assertGreater(result.returncode, 0)
                    self.assertEqual(result.stdout, "")
                    self.assertEqual(result.stderr, "Error\n")

    def test_benchmark_stays_on_stderr(self) -> None:
        values = [8, 4, 7, 3, 6, 2, 5, 1]
        result = self.call("push_swap", ["--bench", *map(str, values)])
        self.assertEqual(result.returncode, 0)
        self.interpret(values, result.stdout)
        total = re.search(r"total_ops: (\d+)", result.stderr)
        self.assertIsNotNone(total)
        if total:
            self.assertEqual(int(total[1]), len(result.stdout.splitlines()))

    def test_checker_rejects_invalid_instructions(self) -> None:
        for instruction in ("unknown\n", "\n", "sa"):
            with self.subTest(instruction=instruction):
                result = self.call("checker", ["2", "1"], instruction)
                self.assertEqual(result.stderr, "Error\n")
                self.assertGreater(result.returncode, 0)
        self.assertEqual(self.call("checker", ["2", "1"]).stdout, "KO\n")
        self.assertEqual(self.call("checker", ["1", "2"]).stdout, "OK\n")


if __name__ == "__main__":
    unittest.main()
