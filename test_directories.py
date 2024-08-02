import unittest
from directories import Tree

class TestDirectoryTree(unittest.TestCase):
    def setUp(self):
        self.tree = Tree()

    def test_create_valid(self):
        result = self.tree.create("fruits/apples")
        self.assertEqual(result, "CREATE fruits/apples")

    def test_create_invalid_no_directory(self):
        result = self.tree.parse("CREATE")
        self.assertEqual(result, 'Invalid CREATE, no directory in input.')

    def test_move_valid(self):
        self.tree.create("fruits/apples")
        self.tree.create("food")
        result = self.tree.move("fruits/apples", "food")
        self.assertEqual(result, "MOVE fruits/apples food")

    def test_move_invalid_source_does_not_exist(self):
        self.tree.create("food")
        result = self.tree.move("fruits/bananas", "food")
        self.assertEqual(result, "Cannot move fruits/bananas - fruits does not exist")

    def test_delete_valid(self):
        self.tree.create("fruits/apples")
        result = self.tree.delete("fruits/apples")
        self.assertEqual(result, "DELETE fruits/apples")

    def test_delete_invalid_does_not_exist(self):
        result = self.tree.delete("fruits/ananas")
        self.assertEqual(result, "Cannot delete fruits/ananas - fruits does not exist")

    def test_list(self):
        self.tree.create("fruits/apples")
        self.tree.create("vegetables")
        result = self.tree.list()
        self.assertEqual(result, "fruits\n  apples\nvegetables")

    def test_parse_create_commands(self):
        commands = [
            "CREATE fruits",
            "CREATE vegetables",
            "CREATE grains",
            "CREATE fruits/apples",
            "CREATE fruits/apples/fuji",
            "LIST"
        ]

        results = [self.tree.parse(command) for command in commands]

        expected_results = [
            "CREATE fruits",
            "CREATE vegetables",
            "CREATE grains",
            "CREATE fruits/apples",
            "CREATE fruits/apples/fuji",
            "fruits\n  apples\n    fuji\ngrains\nvegetables"
        ]

        self.assertEqual(results, expected_results)

    def test_parse_move_and_delete_commands(self):
        commands = [
            "CREATE fruits",
            "CREATE vegetables",
            "CREATE grains",
            "CREATE fruits/apples",
            "CREATE fruits/apples/fuji",
            "LIST",
            "CREATE grains/squash",
            "MOVE grains/squash vegetables",
            "CREATE foods",
            "MOVE grains foods",
            "MOVE fruits foods",
            "MOVE vegetables foods",
            "LIST",
            "DELETE fruits/apples",
            "DELETE foods/fruits/apples",
            "LIST"
        ]

        results = [self.tree.parse(command) for command in commands]

        expected_results = [
            "CREATE fruits",
            "CREATE vegetables",
            "CREATE grains",
            "CREATE fruits/apples",
            "CREATE fruits/apples/fuji",
            "fruits\n  apples\n    fuji\ngrains\nvegetables",
            "CREATE grains/squash",
            "MOVE grains/squash vegetables",
            "CREATE foods",
            "MOVE grains foods",
            "MOVE fruits foods",
            "MOVE vegetables foods",
            "foods\n  fruits\n    apples\n      fuji\n  grains\n  vegetables\n    squash",
            "Cannot delete fruits/apples - fruits does not exist",
            "DELETE foods/fruits/apples",
            "foods\n  fruits\n  grains\n  vegetables\n    squash"
        ]

        self.assertEqual(results, expected_results)

    def test_parse_invalid_command(self):
        result = self.tree.parse("INVALID_COMMAND test")
        self.assertEqual(result, 'Invalid command, it must be one of CREATE, MOVE, LIST, DELETE.')

    def test_parse_invalid_create_no_directory(self):
        result = self.tree.parse("CREATE")
        self.assertEqual(result, 'Invalid CREATE, no directory in input.')

    def test_parse_invalid_move_missing_directory(self):
        result = self.tree.parse("MOVE dir1")
        self.assertEqual(result, 'Invalid MOVE, requires 2 directories in input.')

    def test_parse_invalid_delete_no_directory(self):
        result = self.tree.parse("DELETE")
        self.assertEqual(result, 'Invalid DELETE, no directory in input.')

if __name__ == '__main__':
    unittest.main()
