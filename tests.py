from functions.write_file import write_file

def run_tests():
    print("\nTest 1: Overwrite calculator/lorem.txt")
    print(write_file("calculator", "calculator/lorem.txt", "wait, this isn't lorem ipsum"))

    print("\nTest 2: Create calculator/pkg/morelorem.txt")
    print(write_file("calculator", "calculator/pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

    print("\nTest 3: Attempt to write outside working dir")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

if __name__ == "__main__":
    run_tests()
