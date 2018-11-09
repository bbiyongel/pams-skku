from subroutine import Subroutine
from data_class import Data


class SignCam(Subroutine):
    def __init__(self, data: Data):
        super().__init__(data)
        self.detected_mission = 'DEFAULT'
        self.sign_data = "a"
        self.signs_and_percents = [[0 for col in range(2)] for row in range(50)]
        self.sign = [[0 for col in range(9)] for row in range(3)]
        self.sign_init()

    def sign_init(self):
        self.sign[0][0] = 'default'
        self.sign[0][1] = 'narrow'
        self.sign[0][2] = 'u_turn'
        self.sign[0][3] = 'crosswalk'
        self.sign[0][4] = 'target_tracking'
        self.sign[0][5] = 'parking'
        self.sign[0][6] = 'parking_a'
        self.sign[0][7] = 'parking_b'
        self.sign[0][8] = 'green_light'

    # 최근 몇개의 데이터를 가져와 저장한다!
    def data_decoding(self):
        for i in range(0, 50):
            if self.sign_data.decode() == self.sign_data.decode():
                i = i - 1
            else:
                self.signs_and_percents[i] = self.sign_data.decode().split(' : ')

    #  조건1 최근 몇개의 데이터에서 특정 인식률 이상 인것에 (sign[1][#]+=1)
    def first_selection(self):
        for i in range(0, 50):
            for j in range(0, 8):
                if self.signs_and_percents[i][0] == self.sign[0][j]:
                    if int(self.signs_and_percents[i][1]) > 75:  # 최소 인식률 정하는 곳
                        self.sign[1][j] = self.sign[1][j] + 1

    #  조건2 first_selection 거친 것중에 몇회이상 나오면 (sign[2][#]=1)
    def second_selection(self):
        for i in range(0, 8):
            if self.sign[1][i] >= 25:
                self.sign[2][i] = 1

    #  조건3  sign[2][a]=1의 a를 sign[3][#]=1(가장 최근에 수행한미션)의 #을 비교하여 a <= # 이면 default인 a > # 이면 current_mission=self[0][i]
    def third_selection(self):
        for j in range(0, 8):
            if self.sign[2][j] == 1:
                if self.data.is_next_mission(self.sign[0][j]):
                    self.data.detected_mission_number = self.sign[0][j]

    def sign_reinit(self):
        self.sign[1][0] = 0
        self.sign[1][1] = 0
        self.sign[1][2] = 0
        self.sign[1][3] = 0
        self.sign[1][4] = 0
        self.sign[1][5] = 0
        self.sign[1][6] = 0
        self.sign[1][7] = 0
        self.sign[2][0] = 0
        self.sign[2][1] = 0
        self.sign[2][2] = 0
        self.sign[2][3] = 0
        self.sign[2][4] = 0
        self.sign[2][5] = 0
        self.sign[2][6] = 0
        self.sign[2][7] = 0

    def main(self):
        while True:
            self.data_decoding()
            self.first_selection()
            self.second_selection()
            self.third_selection()
            print(self.detected_mission)
            self.sign_reinit()


if __name__ == "__main__":
    import socket
    import msvcrt

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 20002))

    test = SignCam()
    while True:
        sign_data, addr = sock.recvfrom(1024)
        print(sign_data.decode())
        test.sign_data = sign_data

    sock.close()
