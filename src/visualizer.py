import tkinter as tk
import constants
import time

class snake_visualizer(tk.Canvas):
    BOARD_WIDTH_PX = 300
    BOARD_HEIGHT_PX = 300

    def __init__(self, snake, apple):
        super().__init__(width=constants.VIS_WIDTH, height=constants.VIS_HEIGHT,
                         background="black", highlightthickness=0)
        self.pack()
        self.winfo_toplevel().title("snakeAI")

        # Set the last draw time to zero so we don't wait to draw on the first frame
        self.last_draw_time = 0.0
        self.draw_board(snake, apple)
        self.update()

    def draw_board(self, snake, apple):
        # Time delay so that we can actually see what's going on
        while time.time() < (self.last_draw_time + constants.VIS_TARGET_STEP_TIME):
            time.sleep(0.0001)

        self.delete("all")
        
        for point in snake:
            if point is snake[0]:
                fill_color = "#0BDA51"  # Malachite color
            else:
                fill_color = "#98FB98"  # Mint green
            self.create_rectangle(constants.PX_PER_SQUARE * point[1], constants.PX_PER_SQUARE * point[0],
                                  constants.PX_PER_SQUARE * (point[1] + 1), constants.PX_PER_SQUARE * (point[0] + 1), fill=fill_color)

        fill_color = "#FF3131"  # Neon Red
        self.create_rectangle(constants.PX_PER_SQUARE * apple[1], constants.PX_PER_SQUARE * apple[0],
                              constants.PX_PER_SQUARE * (apple[1] + 1), constants.PX_PER_SQUARE * (apple[0] + 1), fill=fill_color)

        self.update()
        self.last_draw_time = time.time()
    
    def deadloop(self):
        self.mainloop()


if __name__ == '__main__':
    print("Run 'runme.py' with -v/--visualizer option.")
    exit(1)
