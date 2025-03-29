import pyxel

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Jack or Rich")
        pyxel.load("jor.pyxres")

        self.STAGE_WIDTH = 256 * 3
        self.STAGE_HEIGHT = 128 * 2
        self.LEFT_LINE = 40
        self.RIGHT_LINE = pyxel.width - 48
        self.UPPER_LINE = 40
        self.BOTTOM_LINE = pyxel.height - 20
        self.scroll_x = 0
        self.scroll_y = 0
        self.x = 8
        self.y = 100
        self.dx = 0
        self.dy = 0
        self.pldir = 1
        self.jump = 0
        self.score = 0
        self.is_bgm_playing = False
        self.SE_CH = 1
        self.is_goal = False
        self.time_left = 60
        self.is_game_over = False
        self.chkpoint = [(2, 0), (6, 0), (2, 7), (6, 7)]
        self.is_start_screen = True  # スタート画面フラグ
        
        pyxel.run(self.update, self.draw)

    def restart_game(self):
        self.x, self.y = 8, 100
        self.dx, self.dy = 0, 0
        self.jump = 0
        self.score = 0
        self.scroll_x, self.scroll_y = 0, 0
        self.is_goal = False
        self.is_game_over = False
        self.time_left = 60

    def update(self):
        if self.is_start_screen:
            if pyxel.btnp(pyxel.KEY_A):
                self.is_start_screen = False
            return

        if self.is_goal or self.is_game_over:
            if pyxel.btnp(pyxel.KEY_A):
                self.restart_game()
            return

        if not self.is_bgm_playing:
            pyxel.playm(0, loop=True)
            self.is_bgm_playing = True

        if pyxel.frame_count % 30 == 0:
            self.time_left -= 1
            if self.time_left <= 0:
                self.is_game_over = True
                pyxel.play(1, 12, loop=False)

        if pyxel.btn(pyxel.KEY_LEFT):
            if -3 < self.dx:
                self.dx -= 1
            self.pldir = -1
        elif pyxel.btn(pyxel.KEY_RIGHT):
            if self.dx < 3:
                self.dx += 1
            self.pldir = 1
        else:
            self.dx = int(self.dx * 0.7)

        self.x = max(0, min(self.STAGE_WIDTH - 8, self.x + self.dx))
        self.y = max(0, min(self.STAGE_HEIGHT, self.y - self.dy))
        
        if self.y > 128:
            self.is_game_over = True
            pyxel.play(1, 12, loop=False)

    def draw(self):
        pyxel.cls(0)
        if self.is_start_screen:
            pyxel.blt(0, 0, 1, 0, 0, 128, 128)
            pyxel.text(40, 100, "PRESS A TO START", pyxel.frame_count % 16)
        else:
            pyxel.camera()
            pyxel.bltm(0, 0, 0, self.scroll_x, self.scroll_y, pyxel.width, pyxel.height, 0)
            pyxel.camera(self.scroll_x, self.scroll_y)
            pyxel.blt(self.x, self.y, 0, 0, 8, self.pldir * 8, 8, 0)
            pyxel.text(self.scroll_x + pyxel.width - 50, self.scroll_y + 5, f"SCORE: {self.score}", 7)
            pyxel.text(self.scroll_x + pyxel.width - 40, self.scroll_y + 15, f"TIME: {self.time_left}", 7)
            
            if self.is_goal:
                pyxel.text(self.scroll_x + 45, self.scroll_y + 56, "YOU WIN!" if self.score > 0 else "YOU LOSE!", 7)
            elif self.is_game_over:
                pyxel.text(self.scroll_x + 45, self.scroll_y + 56, "GAME OVER!", 7)
                pyxel.text(self.scroll_x + 30, self.scroll_y + 70, "PRESS A TO RESTART", 7)

App()
