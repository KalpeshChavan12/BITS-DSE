#-----------------------------------------------
# built in function used
#   split, print, open, readline, close, lower
# built in datatype used
#  int, str, tuple
#-----------------------------------------------

#----------------------------
# Singly linked list node
#----------------------------
class LinkedListNode:

    def __init__(self, data, next = None):
        self.data = data
        self.next = next
        
    # Iterator to traverse over loop
    def __iter__(self):
        head = self
        while head is not None:
            yield head
            head = head.next

#----------------------------
# Singly linked list 
#----------------------------
class SinglyLinkedList:
    """Singly linked list implementaion contains append, remove and len method
    """

    def __init__(self):
        """ Constructor
        """

        self.__head = None
        self.__last = None
        self.__len = 0
    
    # Append node to list
    def append(self, data):
        """ Append data at end of list
            e.g. 
                ssl.append(3)
                ssl.append("XYZ")
        """
        
        if(self.__head is None):
            self.__head = LinkedListNode(data)
            self.__last = self.__head
        else:
            self.__last.next = LinkedListNode(data)
            self.__last = self.__last.next
        
        self.__len += 1        

    # Remove node from List
    def remove(self, data):
        """ Remove element from list
            if element not exist perform noop.

            e.g sll <- [1,2,3,4]
                sll.remove(3)
                sll <- [1,2,4]
        """

        if(self.__head is None):
            return
        previous = None
        found = None
        for item in self.__head:
            if(item.data == data):
                found = item
                break
            previous = item
        
        if(found is not None):
            # removing head node
            if(previous is None): 
                self.__head = self.__head.next
            # Last node
            elif(self.__last == found):
                self.__last = previous
                self.__last.next = None
            # middle node
            else:
                previous.next = found.next
            
            del found
            self.__len -= 1
    
    # Garbage collector will invoke destructor and make sure it deleted
    def __del__(self):
        while self.__head is not None:
            tmp = self.__head
            self.__head = self.__head.next
            del tmp
        self.__last = None
        self.__len = 0

    # Iterator
    # It will enable iterate over loop
    # e.g. 
    # 
    #  for item in SLL:
    #   print(item)
    #
    def __iter__(self):
        tmp = self.__head
        while tmp is not None:
            yield tmp.data
            tmp = tmp.next

    # call when len(sll) invoked
    def __len__(self):
        return self.__len

#----------------------------------
# N-ary tree node implementaion
#----------------------------------
class TreeNode(object):
    """Tree Node 
    """

    single_instance = None

    def __init__(self, company_name ):
        self.company_name = company_name
        self.children = SinglyLinkedList()

    # add child node for given TreeNode
    def append_child(self, node):
        """ insert node at end
        """
        self.children.append(node)

    # delete child node for given TreeNode
    def delete_child(self, node):
        """ insert node at end
        """
        self.children.remove(node)

    # Preorder traversal provide node and its parent.
    def find_node_and_parent(self, company, parent_node = None):
        """ Find node using preorder search
        """
        if(self.company_name == company):
            return self , parent_node
        
        for child in self.children:
            found, parent_node = child.find_node_and_parent(company, self)
            if( found != None):
                return found, parent_node
        
        return None, None
    
    # del all subtree
    # This will delete all subtree when user invoked del TreeNodeInstance
    def __del__(self):
        del self.children

    # Post order traversal
    # this will enable travesal using loop 
    def __iter__(self):
        for child in self.children:
            for c in child:
                yield c
        yield self

#----------------------------------
# N-ary tree implementaion
#----------------------------------
class Tree:

    __instance = None

    def __init__(self):
        self.__root = None
    
    # non thread safe singleton
    def get_instance():
        if(Tree.__instance is None):
            Tree.__instance = Tree()
        return Tree.__instance

    def add_node(self, data, parent = None):
        """Expect arbitay data and parent node
        """

        # Validate
        if(data is None):
            return False, "Invalid data: Value None"

        # Create new root node
        if(self.__root is None):
            if(parent is None):
                self.__root = TreeNode(data)
                return True, ""
            else:
                return False, "No Data exist in tree"

        # Parent must be null if we want to insert root node
        if parent is None:
            return False, "Parent node is NULL"

        # Validate company already exist in tree
        node, _ = self.__root.find_node_and_parent(data)

        if node is not None:
            return False, "Company already exist"

        # Lookup parent company node in tree
        node, _ = self.__root.find_node_and_parent(parent)
        
        # If node not exist return false
        if(node is None):
            return False, "Parent node exist in tree"

        # add child node
        node.append_child(TreeNode(data))

        return True, ""

    # Find company and its parent in tree using preorder search
    def find_node_and_parent(self, node):
        if(self.__root is None):
            return None, None
        
        return self.__root.find_node_and_parent(node)
            
    # delete company and return reference of deleted node
    # user need to call del (node) explicity to cleanup memory
    def delete_node(self, data):
        if(self.__root is None):
            return False, None, "Tree is Empty"
        
        # Find node in tree
        node, parent = self.__root.find_node_and_parent(data)

        # No node not exist, return error
        if node is None:
            return False, None, "Node not present in tree"

        # Node found but its root node.
        if parent is None:
            self.__root = None
            return True, node, ""
        
        # delete child node
        parent.delete_child(node)

        return True, node, ""

    # returns true if tree is empty
    def is_empty(self):
        if self.__root is None:
            return True
        return False

#---------------------------------------------------
# Helper class to perform input reading and execution
#---------------------------------------------------
class IOHelper:
    """Helper class to read decode and execute input
    """

    outfile_handle = None

    # Constants used for parsing
    CMD_ROOT_NODE = "Company:"
    CMD_NUM_OPERATION = "No of operations:"
    CMD_DETAILS = "DETAIL"
    CMD_RELEASE = "RELEASE"
    CMD_ACQUIRED = "ACQUIRED"

    # constructor
    def __init__(self, input_file = "inputPS5.txt", output_file = "outputPS5.txt"):
        self.input_file = input_file
        self.max_operation_count = 2
        self.operation_counter = 0
        
        # Open file in write mode
        try:
            IOHelper.outfile_handle = open( output_file, "w" )
        except EnvironmentError:
            print('Failed to open file in write mode', input_file)

    # This will read input file and execute operation on tree
    def decode_and_execute_operation(self):

        try:
            with open( self.input_file ) as f :
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if self.execute(line) == False:
                        break

        except EnvironmentError:
            print('Failed to read file', self.input_file)
        
    # Execute single operation from file
    # Param: line -> Detail ce
    def execute(self, line):
        cmd = line.split()
        if(len(cmd) == 2):
            # Create root node
            if(cmd[0].lower() == self.CMD_ROOT_NODE.lower()):
                Tree.get_instance().add_node(cmd[1])
            # Print detail of company
            if(cmd[0].lower() == self.CMD_DETAILS.lower()):
                detail(cmd[1])
            # Release company
            if(cmd[0].lower() == self.CMD_RELEASE.lower()):
                release(cmd[1])
            # Aquire company
            if(cmd[0][0:len(self.CMD_ACQUIRED)].lower() == self.CMD_ACQUIRED.lower()):
                child = cmd[0].split(":")[-1]
                parent = cmd[1].split(":")[-1]
                acquire(parent, child)
        # No of operation command
        elif(len(cmd) == 4):
            if(" ".join(cmd[0:3]).lower() == self.CMD_NUM_OPERATION.lower()):
                try : 
                    self.max_operation_count = int(cmd[3])
                except ValueError :
                    print("Invalid instruction count")
        else:
            print("Invalid instruction")

        self.operation_counter += 1
        if  self.max_operation_count + 2 > self.operation_counter:
                return True
        return False

    # Print output to file
    def Print(str):
        if(IOHelper.outfile_handle == None):
            print(str)
        else:
            print(str,file=IOHelper.outfile_handle)


#---------------------------------------------------
# Get details of company
#---------------------------------------------------
def detail(company_name):
    """this function prints the parent and immediate children of company
    """
    if(Tree.get_instance().is_empty()):
        IOHelper.Print("[Error] No Company data exist")
        return
    
    # Find node in tree
    node, _ = Tree.get_instance().find_node_and_parent(company_name)

    if(node != None):
        IOHelper.Print("DETAIL: {0}".format(node.company_name))
        if(len(node.children)):
            children = [ child.company_name for child in node.children ]
            IOHelper.Print("Acquired companies: {0}".format(", ".join(children)))
        else:
            IOHelper.Print("Acquired companies: none")

        IOHelper.Print("No of companies acquired: {0}".format(len(node.children)))
    else:
        IOHelper.Print("{0} Company does not exist".format(company_name))


#---------------------------------------------------
# Acquire company
#---------------------------------------------------
def acquire(parent_company, acquired_company):
    """Inserts the acquired_company as a new child node to the parent_company
    """

    if(Tree.get_instance().is_empty()):
        IOHelper.Print("[Error] No Company data exist")
        return
    
    # Add node to tree, tree will take care of handling duplicate
    success , _ = Tree.get_instance().add_node(acquired_company, parent_company)

    if(success):
        IOHelper.Print("ACQUIRED SUCCESS: {0} Successfully acquired {1} ".format(parent_company, acquired_company))
    else:
        IOHelper.Print("ACQUIRED FAILED: {0} BY:{1}".format(acquired_company, parent_company))

#---------------------------------------------------
# release company
#---------------------------------------------------
def release(released_company):
    """remove
    """
    if(Tree.get_instance().is_empty()):
        IOHelper.Print("[Error] No Company data exist")
        return
    
    # Delete company delete
    success, node, _ = Tree.get_instance().delete_node(released_company)

    ## Make sure node deleted
    if(success):
        for company in node:
            IOHelper.Print("RELEASED SUCCESS: released {0} successfully.".format(company.company_name))
        # delete subtree (perform cleanup, node already detached from tree)
        del node
    else:
        IOHelper.Print("RELEASED FAILED: released {0} failed.".format(released_company))


#---------------------------------------------------
# Program entry point
#---------------------------------------------------
if __name__ == '__main__':
    io = IOHelper()
    io.decode_and_execute_operation()