def create_new_file():
    print("What would you like to name your new file?")
    file_name = input()
    open(file_name, "w")

def main():
    create_new_file()

if __name__ == "__main__":
    main()