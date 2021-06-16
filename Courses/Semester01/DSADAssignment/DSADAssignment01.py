
# N-ary tree implementaion
# single_instance is root of tree
#  
class TreeNode(object):
    """Tree Node 
    """

    children = []
    company_name = None

    single_instance = None

    def __init__(self, company_name ):
        self.company_name = company_name
        self.children = []

    def insert_node(self, node):
        """ insert node at end
        """
        self.children.append(node)

    def delete_node(self, node):
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



class IOHelper:
    """Helper class to read decode and execute input
    """

    operations = []
    lines = []

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
        self.operations = []
        self.lines = []
        try:
            with open( input_file ) as f :
                self.lines = f.readlines()
        except EnvironmentError:
            print('Failed to read file', input_file)
        
        try:
            IOHelper.outfile_handle = open( outpu_file, "w" )
        except EnvironmentError:
            print('Failed to open file in write mode', input_file)

    def decode_operation(self):
        for line in self.lines:
            cmd = line.split()
            #print(cmd, len(cmd))
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
            #print(operation)
            if(operation[0] == self.CMD_ROOT_OPCODE): 
                TreeNode.single_instance = TreeNode(operation[1])
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



def detail(company_name):
    """this function prints the parent and immediate children of company
    """
    if(TreeNode.single_instance == None):
        IOHelper.Print("No Company data exist")
    
    node, parent = TreeNode.single_instance.find_node_and_parent(company_name)

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

def acquire(parent_company, acquired_company):
    """Inserts the acquired_company as a new child node to the parent_company
    """

    if(TreeNode.single_instance == None):
        IOHelper.Print("No Company data exist")
    
    node, parent = TreeNode.single_instance.find_node_and_parent(acquired_company)

    if(parent != None):
        IOHelper.Print("ACQUIRED FAILED: {0} BY:{1}".format(acquired_company, parent_company))
        return

    node, parent = TreeNode.single_instance.find_node_and_parent(parent_company)
    
    if(node != None):
        node.insert_node(TreeNode(acquired_company))
        IOHelper.Print("ACQUIRED SUCCESS:{1} Successfully acquired {0} ".format(acquired_company,node.company_name))
    else:
        IOHelper.Print("ACQUIRED FAILED:{0} BY:{1}".format(acquired_company, parent_company))

def release(released_company):
    """remove
    """
    if(TreeNode.single_instance == None):
        IOHelper.Print("No Company data exist")
    
    node, parent = TreeNode.single_instance.find_node_and_parent(released_company)

    ## Make sure node exist
    if(node != None and len(node.children)  == 0):
        if(parent == None): # Root node
            TreeNode.single_instance = None
        else:
            parent.delete_node(node)
            IOHelper.Print("RELEASED SUCCESS: released {0} successfully.".format(node.company_name))
    else:
        IOHelper.Print("RELEASED FAILED: released {0} failed".format(released_company))

if __name__ == '__main__':
    io = IOHelper()
    io.decode_operation()
    io.execute_operation()