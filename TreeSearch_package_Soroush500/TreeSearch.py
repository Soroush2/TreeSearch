import os
import pickle

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

def build_tree(root_path):
    root = TreeNode(root_path)
    for dirpath, dirnames, filenames in os.walk(root_path):
        rel_path = os.path.relpath(dirpath, root_path)
        curr_node = root
        if rel_path != '.':
            for dir_name in rel_path.split(os.path.sep):
                child_node = next((child for child in curr_node.children if child.name == dir_name), None)
                if not child_node:
                    child_node = TreeNode(dir_name)
                    curr_node.children.append(child_node)
                curr_node = child_node
        for filename in filenames:
            curr_node.children.append(TreeNode(filename))
    return root

def save_tree(tree, filename):
    with open(filename, 'wb') as file:
        pickle.dump(tree, file)

def load_tree(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

def find_files_with_name(node, target_name, current_path=""):
    results = []
    if node.name == target_name:
        results.append(os.path.join(current_path, node.name))
    for child in node.children:
        results.extend(find_files_with_name(child, target_name, os.path.join(current_path, node.name)))
    return results

def display_tree(node, indent=""):
    print(indent + node.name)
    for child in node.children:
        display_tree(child, indent + "  ")

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    custom_extension = ".mytree"
    save_filename = directory.rstrip(os.path.sep) + custom_extension

    while True:
        option = input("\n1. Build and save tree\n2. Load tree and find files by name\n3. Display tree\n4. Quit\nSelect an option: ")
        
        if option == "1":
            tree = build_tree(directory)
            save_tree(tree, save_filename)
            print(f"Tree saved as {save_filename}")
        
        elif option == "2":
            try:
                loaded_tree = load_tree(save_filename)
                print("Loaded Tree:")
                print(loaded_tree.name)
                target_name = input("Enter the target file name to search for: ")
                matching_files = find_files_with_name(loaded_tree, target_name)
                if matching_files:
                    print(f"Files with the name '{target_name}':")
                    for i, file in enumerate(matching_files, start=1):
                        print(f"{i}. {file}")
                    choice = input("Do you want to open any of these files? (Enter the number or 'n' for no): ")
                    if choice != 'n':
                        try:
                            chosen_file = matching_files[int(choice) - 1]
                            os.system(chosen_file)
                        except (ValueError, IndexError):
                            print("Invalid choice.")
                else:
                    print(f"No files found with the name '{target_name}'.")
            except FileNotFoundError:
                print("Tree file not found. Please build and save the tree first.")
        
        elif option == "3":
            try:
                loaded_tree = load_tree(save_filename)
                print("Tree Structure:")
                display_tree(loaded_tree)
            except FileNotFoundError:
                print("Tree file not found. Please build and save the tree first.")
        
        elif option == "4":
            break
        
        else:
            print("Invalid option. Please select a valid option.")
