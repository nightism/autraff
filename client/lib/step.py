import importlib


class Step:
    name = None
    args = None
    upon_success = None
    upon_failure = None

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def set_successor(self, upon_success=None, upon_failure=None):
        """

        set up the succeeding steps of the current step

        @param upon_success: step obj that will be execute if the current step succeeds
        @param upon_failure: step obj that will be execute if the current step fails

        """
        self.upon_success = upon_success
        self.upon_failure = upon_failure


    def execute(self, predecessor_result):
        """

        Execute command in session

        @param predecessor_result: a dictionary storing the output from current step's predecessor
        @return: Output of command execution, return code {'code', 'output'}

        """

        module = importlib.import_module("modules." + self.name)
        module.execute(self.args, predecessor_result)
