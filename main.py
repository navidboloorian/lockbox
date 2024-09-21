from menu import Menu
from models import init_models

def main():
  init_models()
  
  menu = Menu()
  menu.show()

if __name__ == "__main__":
  main()