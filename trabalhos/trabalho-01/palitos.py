from random import randint


class Game(object):
    def __init__(self, players):
        if len(players) < 2:
            raise ValueError('Number of player must be at least 2')

        self.play_order = players

        self.player_data = {}
        for player in self.play_order:
            #                          [total, on_hand, hunch]
            self.player_data[player] = [3, None, None, False]
        self.player_data['IA 1'][3] = True
        self.player_data['IA 2'][3] = True

    def game_loop(self):
        while not self.won():
            hunches = []

            for player, data in self.player_data.items():
                print("Jogador: {}".format(player))
                if (data[3]):
                    data[1] = randint(0, data[0])

                else:
                    data[1] = randint(0, data[0])

                print("Palitos na mão: {}\n".format(data[1]))

            for player in self.play_order:
                print("Jogador: {}".format(player))
                if (self.player_data[player][3]):
                    hunch = self.hunch(player, hunches)
                    self.player_data[player][2] = hunch

                else:
                    # random hunch
                    hunch = randint(0, self.max())
                    while hunch in hunches:
                        hunch = randint(0, self.max())
                    self.player_data[player][2] = hunch

                    # human hunch
                    # hunch = int(input("Qual seu palpite?\n"))
                    # while (hunch in hunches):
                    #     hunch = int(input("Palpite invalido. \nQual seu palpite?\n"))
                    # self.player_data[player][2] = hunch

                print("Palpite: {}\n".format(hunch))

                hunches.append(hunch)

            winner = self.round_won()

            print("Soma dos palitos: {}".format(self.sum()))

            if winner:
                print("{} ganhou a rodada\n".format(winner))
                self.player_data[winner][0] -= 1
                self.play_order.remove(winner)
                self.play_order.insert(0, winner)
            else:
                print("Ninguém ganhou :(\n")

            print(("-" * 10) + " nova rodada " + ("-" * 10))

            self.reset()

        for player, data in self.player_data.items():
            if data[0] == 0:
                print("{} ganhou o jogo".format(player))
                return player

    def hunch(self, player, hunches):
        # seu palpite inicial eh pelo menos a sua quantidade de palitos
        hunch = self.player_data[player][1]
        rand = 0
        sticks = []
        stik = 0
        # calcula os palitos dos jogadores anteriores atraves dos palpites destes
        for other_player in self.play_order[0:self.play_order.index(player)]:
            # media dos proximos jogadores
            average = self.average(self.play_order[self.play_order.index(other_player):len(self.play_order) - 1])

            # calcula os palitos estimados do jogador
            stik = self.player_data[other_player][2] - average[0]

            # remove os palitos anteriores que ja estao considerados
            for stick in sticks:
                stik -= stick
            sticks.append(stik)

            # erros de arredondamento, adiciona a randomicidade esperada
            rand += average[1]
            hunch += stik

        # chama average com os jogadores remanescente
        average = self.average(self.play_order[self.play_order.index(player):len(self.play_order) - 1])

        # caso o numero seja quebrado (0.5) adiciona-se 1 a randomicidade
        rand += average[1]

        # valor estimado, com metade da randomicidade
        hunch += average[0] + rand // 2

        # caso o chute ja tenha sido usado, chutar o mais proximo possivel
        # começando pelo lado mais proximo da media
        if (self.average(self.play_order)[0] > hunch):
            i = 0
            while (hunch in hunches) or (hunch > self.max()) or (hunch < 0):
                i += 1
                if i % 2 == 0:
                    hunch -= i
                else:
                    hunch += i

        else:
            i = 0
            while (hunch in hunches) or (hunch > self.max()) or (hunch < 0):
                i += 1
                if i % 2 == 0:
                    hunch += i
                else:
                    hunch -= i
        # retorna seu chute
        return hunch

    def average(self, remaining_players):
        result = 0
        for player in remaining_players:
            result += self.player_data[player][0]

        # entrega a media do resultado, e se houve sobra entrega 1 no segundo argumento
        return [result // 2, result % 2]

    def max(self):
        total = 0
        for player in self.play_order:
            total += self.player_data[player][0]
        return total

    def reset(self):
        for player, data in self.player_data.items():
            data[1] = None
            data[2] = None

    def round_won(self):
        sum = self.sum()

        for player, data in self.player_data.items():
            if data[2] == sum:
                return player
        return None

    def won(self):
        for player, data in self.player_data.items():
            if data[0] == 0:
                return True
        return False

    def sum(self):
        sum = 0

        for player, data in self.player_data.items():
            sum += data[1]

        return sum


if __name__ == '__main__':
    players = ['Rand A', 'Rand B', 'Rand C', 'IA 1', 'IA 2']
    wins = {}

    n = 1

    for player in players:
        wins[player] = 0

    for i in range(0, n):
        game = Game(players)
        winner = game.game_loop()
        if winner:
            wins[winner] += 1

    print("\nRelatório:")
    for player, win_count in wins.items():
        print("{} ganhou {} vezes".format(player, win_count))
