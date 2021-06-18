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
    
    def remove_head(self):
        if self.__head is None:
            return
        if self.__head == self.__last :
            self.__last =None
        tmp = self.__head
        self.__head = None
        del tmp

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
# N-ary tree implementaion
# single_instance is root of tree
#  
#----------------------------------
class TreeNode(object):
    """Tree Node 
    """

    single_instance = None

    def __init__(self, company_name ):
        self.company_name = company_name
        self.children = SinglyLinkedList()

    def append_child(self, node):
        """ insert node at end
        """
        self.children.append(node)

    def delete_child(self, node):
        """ insert node at end
        """
        self.children.remove(node)

    def find_node_and_parent(self, company, parent_node = None):
        """ Find node 
        """
        if(self.company_name == company):
            return self , parent_node
        
        for child in self.children:
            found, parent_node = child.find_node_and_parent(company, self)
            if( found != None):
                return found, parent_node
        
        return None, None
    
    # del all subtree
    # This will all subtree when user invoked del
    def __del__(self):
        del self.children

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

        # Create new node
        if(self.__root is None):
            if(parent is None):
                self.__root = TreeNode(data)
                return True, ""
            else:
                return False, "No Data exist in tree"

        if parent is None:
            return False, "Parent node is NULL"

        node, node_parent = self.__root.find_node_and_parent(parent)
        
        if(node is None):
            return False, "Parent node exist in tree"

        node.append_child(TreeNode(data))

        return True, ""

    def find_node_and_parent(self, node):
        if(self.__root is None):
            return None, None
        
        return self.__root.find_node_and_parent(node)
            
    def delete_node(self, data):
        if(self.__root is None):
            return False, "Tree is Empty"
        
        node, parent = self.__root.find_node_and_parent(data)

        if node is None:
            return False, "Node not present in tree"

        if parent is None: # Its root node
            self.__root = None
            del node
            return True, ""
        
        parent.delete_child(node)
        del node

        return True, ""

    def isEmpty(self):
        if self.__root is None:
            return True
        return False

        

#---------------------------------------------------
# Helper class to perfor input reading and execution
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

    # OpCode
    CMD_ROOT_OPCODE = 1
    CMD_NUM_OPERATION_OPCODE = 2
    CMD_DETAILS_OPCODE = 3 
    CMD_RELEASE_OPCODE = 4
    CMD_ACQUIRED_OPCODE = 5

    def __init__(self, input_file = "inputPS5.txt", outpu_file = "outputPS5.txt"):
        self.operations = SinglyLinkedList()
        self.lines = SinglyLinkedList()
        try:
            with open( input_file ) as f :
                while True:
                    line = f.readline()
                    if not line:
                        break
                    self.lines.append(line)

        except EnvironmentError:
            print('Failed to read file', input_file)
        
        try:
            IOHelper.outfile_handle = open( outpu_file, "w" )
        except EnvironmentError:
            print('Failed to open file in write mode', input_file)

    def decode_operation(self):
        for line in self.lines:
            cmd = line.split()
            if(len(cmd) == 2):
                # Root node
                if(cmd[0].lower() == self.CMD_ROOT_NODE.lower()):
                    self.operations.append((self.CMD_ROOT_OPCODE, cmd[1]))
                if(cmd[0].lower() == self.CMD_DETAILS.lower()):
                    self.operations.append((self.CMD_DETAILS_OPCODE, cmd[1]))
                if(cmd[0].lower() == self.CMD_RELEASE.lower()):
                    self.operations.append((self.CMD_RELEASE_OPCODE, cmd[1]))
                if(cmd[0][0:len(self.CMD_ACQUIRED)].lower() == self.CMD_ACQUIRED.lower()):
                    child = cmd[0].split(":")[-1]
                    parent = cmd[1].split(":")[-1]
                    self.operations.append((self.CMD_ACQUIRED_OPCODE, child, parent))

    def execute_operation(self):
        """Execute operation on gloabl instanece tree
        """

        for operation in self.operations:
            if(operation[0] == self.CMD_ROOT_OPCODE): 
                Tree.get_instance().add_node(operation[1])
            if(operation[0] == self.CMD_DETAILS_OPCODE):
                detail(operation[1])
            if(operation[0] == self.CMD_ACQUIRED_OPCODE):
                acquire(operation[2], operation[1])
            if(operation[0] == self.CMD_RELEASE_OPCODE):
                release(operation[1])

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
    if(Tree.get_instance().isEmpty()):
        IOHelper.Print("No Company data exist")
    
    node, _ = Tree.get_instance().find_node_and_parent(company_name)

    if(node != None):
        IOHelper.Print("DETAIL: {0}".format(node.company_name))
        if(len(node.children)):
            children = [ child.company_name for child in node.children]
            IOHelper.Print("Acquired companies: {0}".format(", ".join(children)))
        else:
            IOHelper.Print("Acquired companies: none")

        IOHelper.Print("No of companies acquired: {0}".format(len(node.children)))
    else:
        IOHelper.Print("Company does not exist")


#---------------------------------------------------
# Acquire company
#---------------------------------------------------
def acquire(parent_company, acquired_company):
    """Inserts the acquired_company as a new child node to the parent_company
    """

    if(Tree.get_instance().isEmpty()):
        IOHelper.Print("No Company data exist")
    
    success , erroressage = Tree.get_instance().add_node(acquired_company, parent_company)

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
    if(Tree.get_instance().isEmpty()):
        IOHelper.Print("No Company data exist")
    
    success, errormessage = Tree.get_instance().delete_node(released_company)

    ## Make sure node exist
    if(success):
        IOHelper.Print("RELEASED SUCCESS: released {0} successfully.".format(released_company))
    else:
        IOHelper.Print("RELEASED FAILED: released {0} failed".format(released_company))


#---------------------------------------------------
# Program entry point
#---------------------------------------------------
if __name__ == '__main__':
    io = IOHelper()
    io.decode_operation()
    io.execute_operation()