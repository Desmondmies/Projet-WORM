import time
class Worm2D:
    def __init__(self, canvas, pos_tete):
        self.canv = canvas
        #size_worm = 5
        #pos_worm = [0] * size_worm
        self.draw_worm(pos_tete)

    def draw_worm(self, new_pos_head):
        self.canv.delete("worm")
        self.draw_head(new_pos_head)
        self.canv.update()

    def draw_head(self, new_pos_head, tag = 0, size = 10):
        self.canv.create_oval(new_pos_head[0] - size, new_pos_head[1] - size, new_pos_head[0] + size, new_pos_head[1] + size,
                                fill = "pink",
                                tags = ("worm", tag))
    def promenade(self, path):
        for pts in path:
            self.draw_worm(pts)
            time.sleep(0.025)
