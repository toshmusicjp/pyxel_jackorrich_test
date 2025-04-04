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
        self.is_bgm_playing = False  # BGM再生フラグ
        self.SE_CH = 1  # 効果音のチャンネル
        self.is_goal = False  # ゴール判定フラグ
        self.time_left = 60  # 制限時間
        self.is_game_over = False  # ゲームオーバーフラグ
        self.chkpoint = [(2, 0), (6, 0), (2, 7), (6, 7)]
        self.is_start_screen = True  # スタート画面フラグ
        
        pyxel.run(self.update, self.draw)

    def chkwall(self, cx, cy):
        c = 0
        if cx < 0 or self.STAGE_WIDTH - 8 < cx:
            c += 1
        if self.STAGE_HEIGHT < cy:
            c += 1
        for cpx, cpy in self.chkpoint:
            xi = (cx + cpx) // 8
            yi = (cy + cpy) // 8
            if (1, 0) == pyxel.tilemap(0).pget(xi, yi):
                c += 1
        return c

    def restart_game(self):
        pyxel.load("jor.pyxres")
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
            if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.is_start_screen = False
            return

        if self.is_goal or self.is_game_over:
            if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.restart_game()
            return  # ゲーム終了時は操作無効

        # BGMを一度だけ再生
        if not self.is_bgm_playing:
            pyxel.playm(0, loop=True)
            self.is_bgm_playing = True

        # タイマー更新
        if pyxel.frame_count % 30 == 0:
            self.time_left -= 1
            if self.time_left <= 0:
                self.is_game_over = True
                pyxel.play(1, 12, loop=False)

        # 操作判定
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT, 1, 1):
            if -3 < self.dx:
                self.dx -= 1
            self.pldir = -1
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT, 1, 1):
            if self.dx < 3:
                self.dx += 1
            self.pldir = 1
        else:
            self.dx = int(self.dx * 0.7)

        # 横方向の移動
        lr = pyxel.sgn(self.dx)
        loop = abs(self.dx)
        while loop > 0:
            if self.chkwall(self.x + lr, self.y) != 0:
                self.dx = 0
                break
            self.x += lr
            loop -= 1

        # 左方向へのスクロール
        if self.x < self.scroll_x + self.LEFT_LINE:
            self.scroll_x = max(0, self.x - self.LEFT_LINE)

        # 右方向へのスクロール
        if self.scroll_x + self.RIGHT_LINE < self.x:
            self.scroll_x = min(self.STAGE_WIDTH - pyxel.width, self.x - self.RIGHT_LINE)

        # ジャンプと落下
        if self.jump == 0:
            if self.chkwall(self.x, self.y + 1) == 0:
                self.jump = 2
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.dy = 8
                self.jump = 1
        else:
            self.dy -= 1
            if self.dy < 0:
                self.jump = 2

        ud = pyxel.sgn(self.dy)
        loop = abs(self.dy)
        while loop > 0:
            if self.chkwall(self.x, self.y - ud) != 0:
                self.dy = 0
                self.jump = 2 if self.jump == 1 else 0
                break
            self.y -= ud
            loop -= 1

        # 0以下に落下したらゲームオーバー
        if self.y > 128:
            self.is_game_over = True
            pyxel.play(1, 12, loop=False)

        # コイン判定
        xi, yi = (self.x + 4) // 8, (self.y + 4) // 8
        if pyxel.tilemap(0).pget(xi, yi) == (1, 1):
            self.score += 100
            pyxel.tilemap(0).pset(xi, yi, (0, 0))
            pyxel.play(1, 8, loop=False)

        # ジャック判定
        if pyxel.tilemap(0).pget(xi, yi) == (1, 2):
            self.score -= 200
            pyxel.tilemap(0).pset(xi, yi, (0, 0))
            pyxel.play(1, 9, loop=False)

        # ガール判定
        if pyxel.tilemap(0).pget(xi, yi) == (0, 5):
            self.score += 500
            self.time_left -= 5
            pyxel.tilemap(0).pset(xi, yi, (0, 0))
            pyxel.play(1, 10, loop=False)

        # ゴール判定
        if pyxel.tilemap(0).pget(xi, yi) == (1, 3):
            self.is_goal = True
            pyxel.play(1, 11, loop=False) if self.score > 0 else pyxel.play(1, 12, loop=False)

    def draw(self):
        pyxel.cls(0)
        if self.is_start_screen:
            pyxel.blt(0, 0, 1, 0, 0, 128, 128)
            pyxel.text(30, 56, "PRESS A TO START", pyxel.frame_count % 16)
        else:
            pyxel.camera()
            pyxel.bltm(0, 0, 0, self.scroll_x, self.scroll_y, pyxel.width, pyxel.height, 0)
            pyxel.camera(self.scroll_x, self.scroll_y)
            pyxel.blt(self.x, self.y, 0, 0, 8, self.pldir * 8, 8, 0)
            pyxel.text(self.scroll_x + pyxel.width - 50, self.scroll_y + 5, f"SCORE: {self.score}", 1)
            pyxel.text(self.scroll_x + pyxel.width - 40, self.scroll_y + 15, f"TIME: {self.time_left}", 1)
            
        # ゲーム終了時のメッセージ表示
        if self.is_goal:
            pyxel.text(self.scroll_x + 45, self.scroll_y + 56, "YOU WIN!" if self.score > 0 else "YOU LOSE!", 8)
        elif self.is_game_over:
            pyxel.text(self.scroll_x + 45, self.scroll_y + 56, "GAME OVER!", 8)

        if self.is_goal or self.is_game_over:
            pyxel.text(self.scroll_x + 20, self.scroll_y + 70, "PRESS A KEY TO RESTART", 8)

App()
