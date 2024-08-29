import pygame
from simulation.UI.hex_grid_board import HexGrid
from simulation.UI.log_window import LogWindow
from simulation.model.factory import Game_Sample, Game_Sample_small
from simulation.model.mech import MovementDirection, RotatetDirection

if __name__ == '__main__':
    WIDTH, HEIGHT = 600, 800
    TOTAL_WIDTH,TOTAL_HEIGHT = 1200,800
    #uiboard = UIBoard(game=Game_Sample,map_width=WIDTH,map_height=HEIGHT,screen_width= TOTAL_WIDTH,screen_height=TOTAL_HEIGHT)
    game = Game_Sample_small
    board = game.board
    uiboard = HexGrid(origin_x=0,origin_y=0,map_width=board.width, map_height=board.height,map_screen_width=WIDTH,map_screen_height=HEIGHT)
    pygame.init()
    screen = pygame.display.set_mode(( TOTAL_WIDTH, TOTAL_HEIGHT))
    clock = pygame.time.Clock()
    logs = LogWindow(origin_x=700,origin_y=30,screen_width=400,screen_height=700)
    running = True
    while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type==pygame.KEYDOWN and event.key != pygame.K_ESCAPE:
                     if event.key == pygame.K_UP:
                          game.move_mech_forward_backward(MovementDirection.md_forward)
                          logs.add_log("Mech move forward")
                     if event.key == pygame.K_DOWN:
                          game.move_mech_forward_backward(MovementDirection.md_backward)
                          logs.add_log("Mech move bacwkard")
                     if event.key == pygame.K_LEFT:
                          game.rotate_mech(rotateDirection=RotatetDirection.rd_left)
                          logs.add_log("Mech rotate left")
                     if event.key == pygame.K_RIGHT:
                          game.rotate_mech(rotateDirection=RotatetDirection.rd_right)
                          logs.add_log("Mech rotate right")
            uiboard.draw_board(screen=screen,board=board)
            uiboard.draw_unit(screen=screen, mech=game.p1_mech)
            uiboard.draw_unit(screen=screen, mech=game.p2_mech)
            logs.draw_logs(screen=screen)
            # Actualizar la pantalla
            pygame.display.flip()
            clock.tick(60)
    pygame.quit()