# title: 7
# aim: Program to implement  Monkey Banana problem using Python.


import unittest
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


class MonkeyBananaProblem:
    def __init__(self):
        self.monkey_position = "floor"
        self.banana_position = "high"
        self.stool_position = "floor"
        self.actions = []

    def perform_action(self, action):
        if action == "move_to_stool":
            return self.move_to_stool()
        elif action == "climb":
            return self.climb()
        elif action == "grab_banana":
            return self.grab_banana()
        elif action == "descend":
            return self.descend()
        elif action == "move_to_floor":
            return self.move_to_floor()
        else:
            return False

    def move_to_stool(self):
        if self.monkey_position == "floor" and self.stool_position == "floor":
            self.monkey_position = "stool"
            self.actions.append("move_to_stool")
            return True
        return False

    def climb(self):
        if self.monkey_position == "stool" and self.banana_position == "high":
            self.monkey_position = "high"
            self.actions.append("climb")
            return True
        return False

    def grab_banana(self):
        if self.monkey_position == "high" and self.banana_position == "high":
            self.banana_position = "held"
            self.actions.append("grab_banana")
            return True
        return False

    def descend(self):
        if self.monkey_position == "high":
            self.monkey_position = "stool"
            self.actions.append("descend")
            return True
        return False

    def move_to_floor(self):
        if self.monkey_position == "stool":
            self.monkey_position = "floor"
            self.actions.append("move_to_floor")
            return True
        return False

    def solve(self):
        actions = ["move_to_stool", "climb", "grab_banana", "descend", "move_to_floor"]
        for action in actions:
            if not self.perform_action(action):
                return "Failed to perform action: " + action
        return "Banana acquired!"


class TestMonkeyBananaProblem(unittest.TestCase):
    def setUp(self):
        self.problem = MonkeyBananaProblem()

    def test_initial_state(self):
        self.assertEqual(self.problem.monkey_position, "floor")
        self.assertEqual(self.problem.banana_position, "high")
        self.assertEqual(self.problem.stool_position, "floor")
        self.assertEqual(self.problem.actions, [])
        logging.info("Initial state test passed.")

    def test_actions(self):
        self.assertTrue(self.problem.perform_action("move_to_stool"))
        self.assertEqual(self.problem.monkey_position, "stool")
        self.assertTrue(self.problem.perform_action("climb"))
        self.assertEqual(self.problem.monkey_position, "high")
        self.assertTrue(self.problem.perform_action("grab_banana"))
        self.assertEqual(self.problem.banana_position, "held")
        self.assertTrue(self.problem.perform_action("descend"))
        self.assertEqual(self.problem.monkey_position, "stool")
        self.assertTrue(self.problem.perform_action("move_to_floor"))
        self.assertEqual(self.problem.monkey_position, "floor")
        logging.info("Actions test passed.")

    def test_solve(self):
        result = self.problem.solve()
        self.assertEqual(result, "Banana acquired!")
        self.assertEqual(
            self.problem.actions,
            ["move_to_stool", "climb", "grab_banana", "descend", "move_to_floor"],
        )
        logging.info("Solve test passed.")

    def test_invalid_action(self):
        result = self.problem.perform_action("invalid_action")
        self.assertFalse(result)
        logging.info("Invalid action test passed.")

    def test_failed_action(self):
        self.problem.monkey_position = "floor"
        result = self.problem.perform_action("climb")
        self.assertFalse(result)
        logging.info("Failed action test result: %s", result)

    def tearDown(self):
        logging.info("Actions taken: %s", self.problem.actions)


if __name__ == "__main__":
    unittest.main()
