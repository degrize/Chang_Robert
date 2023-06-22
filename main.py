import socket

ELECTION = 0
NEW_LEAD = 1


class Node:
    def __init__(self, site_number, neighbor_number, info):
        self.site_number = site_number
        self.neighbor_number = neighbor_number
        self.info = info
        self.is_participant = False
        self.is_leader = False
        self.leader = None

    def start_election(self):
        print("Numéro du site :", self.site_number)
        print("Numéro du voisin :", self.neighbor_number)
        print("Info transmise :", self.info)
        print("Démarre une élection.")
        self.is_participant = True
        self.forward((ELECTION, self.site_number, self.info))

    def forward(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", self.neighbor_number))
            s.sendall(str(message).encode())

    def accept(self, message):
        group, site_number, info = message
        if group == ELECTION:
            if site_number > self.site_number:
                print("{}Transmet {} tel que recu".format(self.site_number, site_number))
                self.is_participant = True
                self.forward((ELECTION, site_number, info))
            if site_number < self.site_number:
                print("{} transmet son propre numéro.".format(self.site_number))
                self.is_participant = True
                self.forward((ELECTION, self.site_number, self.info))
            if site_number == self.site_number:
                print("Je suis l'élu !")
                self.is_participant = False
                self.is_leader = True
                self.leader = self.site_number
                self.forward((NEW_LEAD, self.site_number))
        if group == NEW_LEAD:
            print("Le site élu est :", site_number)


def run_node(node):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", node.site_number))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = eval(data.decode())
                node.accept(message)


def spawn():
    site_number = int(input("Entrez le numéro du site : "))
    neighbor_number = int(input("Entrez le numéro du voisin : "))
    info = int(input("Entrez l'information à transmettre : "))
    node = Node(site_number, neighbor_number, info)
    return node


if __name__ == '__main__':
    node = spawn()
    run_node(node)
    start = input("Appuyez sur Entrée pour démarrer l'algorithme de Chang Robert...")

    node.start_election()
