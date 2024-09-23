from menu import Menu
from models import init_models
from utils import create_arg_parser, does_key_match, private_key_bytes, set_private_key
from api import user_exists
import os
from pathlib import Path
from sys import exit

def main():
  init_models()

  parser = create_arg_parser()
  args = parser.parse_args()

  if user_exists() and not args.private_key_path:
    print("Private key is required.")
    exit()
  elif user_exists() and not os.path.exists(args.private_key_path):
    print("Invalid private key path.")
    exit()
  elif user_exists() and not does_key_match(private_key_bytes(Path(args.private_key_path).read_text())):
    print("Key validation failed!")
    exit()

  set_private_key(private_key_bytes(Path(args.private_key_path).read_text()))
  
  menu = Menu()
  menu.show()

if __name__ == "__main__":
  main()