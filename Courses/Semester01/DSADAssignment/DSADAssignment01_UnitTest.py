import unittest
import random
import DSADAssignment01V4

def add_childs_to_leaf(root, num):
    if root is None:
        return
    
    if(len(root.children)  == 0 ):
        for i in range(num):
            root.append_child(DSADAssignment01V4.TreeNode("child{0}".format(TestStringMethods.count)))
            TestStringMethods.count += 1
    else:
        for i in root.children:
            add_childs_to_leaf(i, num)

class TestStringMethods(unittest.TestCase):

    count = 0
    def setUp(self):
        TestStringMethods.count = 0
        self.root = DSADAssignment01V4.TreeNode("Root")
        add_childs_to_leaf(self.root, 10)
        add_childs_to_leaf(self.root, 10)
        add_childs_to_leaf(self.root, 10)
        add_childs_to_leaf(self.root, 10)
        add_childs_to_leaf(self.root, 10)
        add_childs_to_leaf(self.root, 10)
        print("Total Number of nodes added", TestStringMethods.count)

    def test_find_rand_node_exist(self):
        
        # random element search
        for i in range(1, 20):
            key = "child{0}".format(random.randrange(TestStringMethods.count - 1))
            print("Finding node=",key)
            n, parent = self.root.find_node_and_parent(key)
            self.assertTrue(n is not None)
            self.assertTrue(parent is not None)

        # Find root Node 
        n, parent = self.root.find_node_and_parent("Root")
        self.assertTrue(n is not None)
        self.assertTrue(parent is None)

        # Node not exist
        n, parent = self.root.find_node_and_parent("NodeNotExist")
        self.assertTrue(n is None)
        self.assertTrue(parent is None)

        # delete
        for i in range(1, 20):
            key = "child{0}".format(random.randrange(TestStringMethods.count - 1))
            print("Deleting node=",key)
            n, parent = self.root.find_node_and_parent(key)
            self.assertTrue(n is not None)
            self.assertTrue(parent is not None)

            parent.delete_child(n)

            # verify deleted
            n, parent = self.root.find_node_and_parent(key)
            self.assertTrue(n is None)
            self.assertTrue(parent is None)

if __name__ == '__main__':
    unittest.main()