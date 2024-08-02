import unittest
from directories import Tree


class TestDirectoryTree(unittest.TestCase):
    def setUp(self):
        self.tree = Tree()


    def test_create_directories(self):
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

    def test_move_and_delete_directories(self):
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


    def test_create_invalid_command(self):
        result = self.tree.parse("INVALID_COMMAND test")
        self.assertEqual(result, 'Invalid command, it must be one of CREATE, MOVE, LIST, DELETE.')

    def test_create_no_directory(self):
        result = self.tree.parse("CREATE")
        self.assertEqual(result, 'Invalid CREATE, no directory in input.')

    def test_move_missing_directory(self):
        result = self.tree.parse("MOVE dir1")
        self.assertEqual(result, 'Invalid MOVE, requires 2 directories in input.')

    def test_delete_no_directory(self):
        result = self.tree.parse("DELETE")
        self.assertEqual(result, 'Invalid DELETE, no directory in input.')

    def test_create_function(self):
        # Valid path
        result = self.tree.create("fruits/apples")
        self.assertEqual(result, "CREATE fruits/apples")

        # Invalid path - handled in parse, not in create directly
        result = self.tree.parse("CREATE")
        self.assertEqual(result, 'Invalid CREATE, no directory in input.')

    def test_move_function(self):
        # Setup initial structure
        self.tree.create("fruits/apples")
        self.tree.create("food")

        # Valid move
        result = self.tree.move("fruits/apples", "food")
        self.assertEqual(result, "MOVE fruits/apples food")

        # Invalid move - source does not exist
        result = self.tree.move("fruits/bananas", "food")
        self.assertEqual(result, "Cannot move fruits/bananas - bananas does not exist")

        # Invalid move - destination does not exist
        result = self.tree.move("vegetables/apples", "grains")
        self.assertEqual(result, "MOVE vegetables/apples grains")

    def test_delete_function(self):
        # Setup initial structure
        self.tree.create("fruits/apples")

        # Valid delete
        result = self.tree.delete("fruits/apples")
        self.assertEqual(result, "DELETE fruits/apples")

        # Invalid delete - directory does not exist
        result = self.tree.delete("fruits/ananas")
        self.assertEqual(result, "Cannot delete fruits/ananas - fruits does not exist")

    def test_list_function(self):
        # Setup initial structure
        self.tree.create("fruits/apples")
        self.tree.create("vegetables")

        # Valid list
        result = self.tree.list()
        self.assertEqual(result, "fruits\n  apples\nvegetables")


if __name__ == '__main__':
    unittest.main()
