import sys

if __name__ == '__main__':
    x = []
    if len(sys.argv) > 1:
        x = sys.argv[1:]
    print(x)
    print("over")