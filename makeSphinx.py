import os

dirname = os.path.dirname(os.path.abspath(__file__))
os.chdir(dirname + r"/sphinx")
os.system("make html")
