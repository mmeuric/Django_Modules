def read_numbers():
    with open('numbers.txt', 'r') as f:
        content = f.read()
    numbers = content.split(',')
    for n in numbers:
        print(n.strip())


if __name__ == '__main__':
    read_numbers()
