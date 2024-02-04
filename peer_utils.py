def find_longest_chain(root):
    def dfs(node, current_path):
        if not node:
            return current_path

        current_path.append(node)

        longest_path = current_path
        for child in node.children:
            child_path = dfs(child, current_path.copy())
            if len(child_path) > len(longest_path):
                longest_path = child_path

        return longest_path

    return dfs(root, [])