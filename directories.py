import sys
import logging


class Tree:
    def __init__(self):
        self.tree = {}
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger()

    def log_and_return(self, message, level='info'):
        if level == 'info':
            self.logger.info(message)
        elif level == 'error':
            self.logger.error(message)
        return message

    def parse(self, command_line):
        """
        Parse and execute a command from a command line string.
        Commands must start with CREATE, MOVE, LIST, OR DELETE.
        LIST requires no other params.
        MOVE requires 2 directories.
        ALL other commands require 1 directory.
        """
        lines = command_line.split()
        if lines[0] not in ['CREATE', 'MOVE', 'LIST', 'DELETE']:
            return self.log_and_return('Invalid command, it must be one of CREATE, MOVE, LIST, DELETE.', 'error')
        elif lines[0] == 'CREATE':
            if len(lines) < 2:
                return self.log_and_return('Invalid CREATE, no directory in input.', 'error')
            return self.create(lines[1])
        elif lines[0] == 'MOVE':
            if len(lines) < 3:
                return self.log_and_return('Invalid MOVE, requires 2 directories in input.', 'error')
            return self.move(lines[1], lines[2])
        elif lines[0] == 'LIST':
            # list function is recursive, so this must be outside
            self.logger.info("LIST")
            return self.log_and_return(self.list())
        else:
            if len(lines) < 2:
                return self.log_and_return('Invalid DELETE, no directory in input.', 'error')
            return self.delete(lines[1])

    def create(self, directory):
        """
        Create a directory given its path.
        If an intermediate folder does not exist, it will be created.
        """
        folders = directory.split('/')
        self.make_if_not_existing(folders)
        return self.log_and_return(f"CREATE {directory}")

    def make_if_not_existing(self, folders):
        node = self.tree
        for folder in folders:
            if folder not in node:
                node[folder] = {}
            node = node[folder]
        return node

    def move(self, dir_one, dir_two):
        """
        Move a directory from dir_one to dir_two.
        The source directory must fully exist, the destination follows the same rules as CREATE.
        """
        source = dir_one.split('/')
        destination = dir_two.split('/')
        source_node = self.tree

        folder_to_move = source[-1]

        for folder in source:
            if folder not in source_node:
                return self.log_and_return(f"Cannot move {dir_one} - {folder} does not exist", 'error')
            if folder != folder_to_move:
                source_node = source_node[folder]

        dest_node = self.make_if_not_existing(destination)

        dest_node[folder_to_move] = source_node.pop(folder_to_move)
        return self.log_and_return(f"MOVE {dir_one} {dir_two}")

    def list(self, node=None, prefix=''):
        if node is None:
            node = self.tree
        result = []
        for key in sorted(node.keys()):
            result.append(prefix + key)
            result.extend(self.list(node[key], prefix + '  '))
        if prefix == '':
            return '\n'.join(result)
        return result

    def delete(self, directory):
        # Due to requirements to have an exact match, this delete log is at the start.
        self.logger.info(f"DELETE {directory}")
        folders = directory.split('/')
        node = self.tree

        folder_to_delete = folders[-1]
        for folder in folders[:-1]:
            if folder not in node:
                return self.log_and_return(f"Cannot delete {directory} - {folders[0]} does not exist", 'error')
            node = node[folder]
        if folder_to_delete in node:
            del node[folder_to_delete]
            return f"DELETE {directory}"
        else:
            return self.log_and_return(f"Cannot delete {directory} - {folders[0]} does not exist", 'error')


if __name__ == "__main__":
    tree = Tree()

    if len(sys.argv) != 2:
        print("Usage: python directories.py <input_file>")
        sys.exit(1)

    file = sys.argv[1]

    contents = open(file, 'r').readlines()
    for line in contents:
        tree.parse(line)
