from threading import Thread
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
        thread1 = Thread(
            target = Worm2D.promenade, args=(worm1, path1)
        )

        thread2 = Thread(
            target = Worm2D.promenade, args=(worm2, path2, "worm2")
        )

        thread1.start()
        thread2.start()

        """
        prom1 = loop.create_task(worm1.promenade(path1))
        prom2 = loop.create_task(worm2.promenade(path2, "worm2"))
        await asyncio.wait([prom1, prom2])
        """

    def promenade(self, path, tagWorm = "worm"):
        for pts in path:
            self.draw_worm(pts, tagWorm)
            time.sleep(0.025)
