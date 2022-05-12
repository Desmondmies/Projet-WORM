import time

class Worm2D:
    def __init__(self, canvas, pos_tete):
        self.canv = canvas
        self.draw_worm(pos_tete)

    def draw_worm(self, new_pos_head, tagWorm = "worm"):
        self.canv.delete(tagWorm)
        self.draw_head(new_pos_head, tagWorm)
        self.canv.update()

    def draw_head(self, new_pos_head, tagWorm, size = 10):
        self.canv.create_oval(new_pos_head[0] - size, new_pos_head[1] - size, new_pos_head[0] + size, new_pos_head[1] + size,
                                fill = "pink",
                                tags = tagWorm)

    @staticmethod
    def course(worm1, worm2, path1, path2):
        max_step = len(path1) if len(path1) >= len(path2) else len(path2)

        for step in range(0, max_step):
            if step < len(path1):
                worm1.draw_worm(path1[step])
            if step < len(path2):
                worm2.draw_worm(path2[step], "worm2")
            time.sleep(0.025)

    def promenade(self, path, tagWorm = "worm"):
        for pts in path:
            self.draw_worm(pts, tagWorm)
            time.sleep(0.025)
