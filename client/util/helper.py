from modules import *


def execute_mod(module_name, args, driver):
    print('helper1')
    if module_name is None or module_name == "":
        return

    print('helper2')
    mod = eval(module_name)
    mod.execute(args, driver=driver)
