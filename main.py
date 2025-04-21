# Prevents __pycache__ generation - cache is not needed for this small project
import sys; sys.dont_write_bytecode = True
# Rest of imports
from library import SystemContext, clear, main_menu



def main():
    clear()
    ctx = SystemContext()
    main_menu(ctx)


if __name__ == "__main__":
    main()