class Intern:

    class Coffee:
        def __str__(self):
            return "This is the worst coffee you ever tasted."

    def __init__(self, name="My name? I'm nobody, an intern, I have no name."):
        self.Name = name

    def __str__(self):
        return self.Name

    def work(self):
        raise Exception("I'm just an intern, I can't do that...")

    def make_coffee(self):
        return Intern.Coffee()


if __name__ == '__main__':
    # Instanciation sans nom
    intern1 = Intern()
    print(intern1)

    # Instanciation avec nom "Mark"
    mark = Intern("Mark")
    print(mark)

    # Mark fait un café
    coffee = mark.make_coffee()
    print(coffee)

    # L'autre stagiaire tente de travailler — exception gérée
    try:
        intern1.work()
    except Exception as e:
        print(e)
