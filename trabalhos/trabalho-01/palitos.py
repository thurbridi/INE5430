from random import randint


class Game(object):
    def __init__(self, players):
        if len(players) < 2:
            raise ValueError('Number of player must be at least 2')

        self.play_order = players

        self.player_data = {}
        for player in self.play_order:
            #                          [total, on_hand, hunch]
            self.player_data[player] = [3, None, None]

    def game_loop(self):
        while not self.won():
            hunches = []

            for player, data in self.player_data.items():
                # data[1] = randint(0, data[0])
                print("Jogador: {}".format(player))
                data[1] = int(input("Quantos palitos irá guardar na mão?\n"))

            for player in self.play_order:
                print("Jogador: {}".format(player))
                hunch = int(input("Qual seu palpite?\n"))
                if hunch not in hunches:
                    self.player_data[player][2] = hunch
                    hunches.append(hunch)

            winner = self.round_won()
            if winner:
                print("{} ganhou a rodada\n".format(winner))
                self.player_data[winner][0] -= 1

            print(self.player_data)
            self.reset()

    def hunch(self):
        pass

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
    players = ['A', 'B']

    game = Game(players)
    game.game_loop()
