import pygame
import time 
from Problem import Graph
from Search import Search
class Visualized:
    def Visualize(file_path):  
        graph=Graph()
        graph.load_map(file_path) 

        # Chuyển mảng chuỗi sao mảng số nguyên để vẽ theo quy ước 
        def convertStringtoInt(mangCuaPhong):
        # Mã nhị phân được bật theo {up}{down}{left}{right}
            mapping = { 
                "0000": 0,  # Không có tường
                "0101": 4,  # góc trái trên
                "1001": 5,  # góc trái dưới
                "0110": 6,  # góc phải trên
                "1010": 7,  # góc phải dưới
                "0011": 8,  # đường ngang
                "0001": 8.1, 
                "0010": 8.2,  
                "1100": 9,  # đường dọc
                "1000": 9.1, 
                "0100": 9.2,    
                "1011": 8.3, 
                "1101": 9.3, 
                "0111": 8.3, 
                "1110": 9.3, 
                "1111": 14
            }

            def get_walls(x, y):
            # toạ độ của tường
                """ Kiểm tra 4 hướng (trên, dưới, trái, phải) xem có phải tường hay không """

            # xét up
                up = 1 if y > 0 and x < len(mangCuaPhong[0]) and mangCuaPhong[y - 1][x] == '%' else 0

            # xét down 
                down = 1 if y < (len(mangCuaPhong) - 1) and x < len(mangCuaPhong[0]) and mangCuaPhong[y + 1][x] == '%' else 0

            # xét left  
                left = 1 if x > 0 and mangCuaPhong[y][x - 1] == '%' else 0

            # xét right
                right = 1 if x < (len(mangCuaPhong[0]) - 1) and mangCuaPhong[y][x + 1] == '%' else 0
                return f"{up}{down}{left}{right}"
        # Lấy vị trí các phần tử như food, pie, pacman 
            def get_Objects(mang: list):
                for i in range(len(mang)):
                    for j in range(len(mang[i])):
                        if (i,j) == graph.get_pacman():
                            mang[i][j] = 1
                        if (i,j) in graph.get_foods():
                            mang[i][j] = 2
                        if (i,j) in graph.get_pies():
                            mang[i][j] = 3
                return mang


            # Khởi tạo mảng số nguyên
            number_mangCuaPhong = [[0] * len(mangCuaPhong[0]) for _ in range(len(mangCuaPhong))]

            for y in range(len(mangCuaPhong)):
                for x in range(len(mangCuaPhong[y])):
                    if mangCuaPhong[y][x] == '%':  # Nếu là tường
                        key = get_walls(x, y)
                        number_mangCuaPhong[y][x] = mapping.get(key, 0)  # Lấy giá trị từ mapping
            number_mangCuaPhong=get_Objects(number_mangCuaPhong)
            return number_mangCuaPhong
        mangCuaPhong = convertStringtoInt(graph.get_grid())
        
        
        pygame.init()
        # Các phần tử tham gia vẽ mê cung
        size_up=40
        W=len(mangCuaPhong[0])*size_up
        H=len(mangCuaPhong)*size_up
        # Kích thước mỗi ô lưới
        cell_H=H//len(mangCuaPhong)
        cell_W=W//len(mangCuaPhong[0])
        # Tạo cửa sổ 
        screen=pygame.display.set_mode([W, H])
        pygame.display.set_caption("Pacman Visualization")
        
        # Các phần tử tham gia vẽ Pacman
        S=Search()
        direction='R' # Định hướng cho Pacman 
        pacman=graph.get_pacman()
        move_count=0
        move,nextPos,cost=S.search(file_path) #Các danh sách lần lượt chứa bước di chuyền, vị trí đi qua, chi phí đi
        print(f"Path : {move}")
        print(f"Total cost: {cost}")
        # Lấy khung cho Pacman
        pac_image=[]
        for i in range(1,5):
            pac_image.append(pygame.transform.scale(pygame.image.load(f'./images/pacman/pacman{i}.png'),(30,30)))

        # Hàm vẽ mê cung
        def draw_board(mangCuaPhong): 
            for i in range(len(mangCuaPhong)): 
                for j in range(len(mangCuaPhong[i])):   
                # Định tọa độ của các phần tử lên trên lưới
                    x=j*cell_W
                    y=i*cell_H
                # vẽ đường đi và đối tượng
                    if mangCuaPhong[i][j]==0:
                      pygame.draw.circle(screen,'white',(x + cell_W//2 , y + cell_H//2), 1) #Path
                    if mangCuaPhong[i][j]==1:
                        continue  
                    if mangCuaPhong[i][j]==2 and not flicker:
                      pygame.draw.circle(screen,'white',(x + cell_W//2 , y + cell_H//2), 4) #Foods
                    if mangCuaPhong[i][j]==3:
                      pygame.draw.circle(screen,'brown',(x + cell_W//2 , y + cell_H//2), 8) #Pies

                #Các góc 
                    #Góc trái trên
                    if mangCuaPhong[i][j]==4 :
                     if(i==0 and j==0):
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x+cell_W, y + cell_H//2),3)
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x+cell_W//2, y + cell_H),3)
                     else:
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x + cell_W*1.5, y + cell_H//2),3)
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x + cell_W//2, y + cell_H*1.5),3)

                    #Góc trái dưới
                    if mangCuaPhong[i][j]==5 :
                     if(i==len(mangCuaPhong)-1 and j==0):
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x+cell_W, y + cell_H//2),3)
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x+cell_W//2, y),3)
                     else:
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x+cell_W*1.5, y + cell_H//2),3)
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x+cell_W//2, y-cell_H//2),3)

                    #Góc phải trên       
                    if mangCuaPhong[i][j]==6 :
                        if(i==0 and j==len(mangCuaPhong[0])-1):
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x, y + cell_H//2),3)
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x+cell_W//2, y + cell_H),3)
                        else:
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x-cell_W//2, y + cell_H//2),3)
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x+cell_W//2, y + cell_H*1.5),3)

                    #Góc phải dưới
                    if mangCuaPhong[i][j]==7 :
                        if(i==len(mangCuaPhong)-1 and j==len(mangCuaPhong[0])-1):
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x, y + cell_H//2),3)
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x+cell_W//2, y),3)
                        else:
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x-cell_W//2, y+cell_H//2 ),3)
                            pygame.draw.line(screen, 'blue', (x + cell_W//2 , y + cell_H//2), (x+cell_W//2, y-cell_H//2),3)

                # Đường thẳng
                    #Ngang
                    if mangCuaPhong[i][j]==8:
                        pygame.draw.line(screen, 'blue', (x + cell_W//2, y + cell_H//2), (x+cell_W, y + cell_H//2),3)
                        pygame.draw.line(screen, 'blue', (x + cell_W//2, y + cell_H//2), (x, y + cell_H//2),3)
                    if mangCuaPhong[i][j]==8.1:
                        pygame.draw.line(screen, 'blue', (x + cell_W//2, y + cell_H//2), (x+cell_W, y + cell_H//2),3) #Vẽ bên phải
                    if mangCuaPhong[i][j]==8.2:
                        pygame.draw.line(screen, 'blue', (x + cell_W//2, y + cell_H//2), (x, y + cell_H//2),3) #Vẽ bên Trái 
                    if mangCuaPhong[i][j]==8.3:
                        pygame.draw.line(screen, 'blue', (x + cell_W//2, y + cell_H//2), (x+cell_W*1.5, y + cell_H//2),3)
                        pygame.draw.line(screen, 'blue', (x + cell_W//2, y + cell_H//2), (x-cell_W//2, y + cell_H//2),3)
                    #Dọc
                    if mangCuaPhong[i][j]==9:
                        pygame.draw.line(screen, 'blue', (x + cell_W//2, y + cell_H//2), (x+cell_W//2, y + cell_H),3)
                        pygame.draw.line(screen, 'blue', (x + cell_W//2, y + cell_H//2), (x+cell_W//2, y),3)
                    if mangCuaPhong[i][j]==9.1:
                        pygame.draw.line(screen, 'blue', (x + cell_W//2, y + cell_H//2), (x+cell_W//2, y),3) #Vẽ lên 
                    if mangCuaPhong[i][j]==9.2:
                        pygame.draw.line(screen, 'blue', (x + cell_W//2, y + cell_H//2), (x+cell_W//2, y + cell_H),3) #Vẽ xuống
                    if mangCuaPhong[i][j]==9.3:
                        pygame.draw.line(screen, 'blue', (x + cell_W//2, y + cell_H//2), (x+cell_W//2, y-cell_H//2),3)
                        pygame.draw.line(screen, 'blue', (x + cell_W//2, y + cell_H//2), (x+cell_W//2, y + cell_H*1.5),3)

        # Hàm vẽ Pacman 
        def draw_Pacman(Pos: tuple, direction):
            direction_angle = {'R': 0, 'U': 90, 'L': 180, 'D': 270}
            pac_y, pac_x = Pos[0],Pos[1]
            rotate_pacman = pygame.transform.rotate(pac_image[counter // 5], direction_angle[direction])
            screen.blit(rotate_pacman ,(pac_x,pac_y)) 

    
        run=True
        current_pos = pacman
        started = False
        path_steps = list(zip(move, nextPos))
        
        timer = pygame.time.Clock()
        fps=60
        counter=0
        flicker=False
        
        while run:
            time.sleep(0.17)
            timer.tick(fps)
            if counter < 10:  # Giữ tốc độ nhai nhanh hơn
                counter += 2 
                if counter > 10 :
                    counter = 0
                    flicker = not flicker  # Tiếp tục nhấp nháy dù food đã hết
            else:
                counter = 0
                flicker = not flicker

            screen.fill('black')
            # Vẽ 
            draw_board(mangCuaPhong)
            y,x = current_pos[0],current_pos[1]
            draw_Pacman((y*cell_H,x*cell_W),direction)

            # Cập nhật bản đồ 
            if  started and move_count < len(path_steps):
                direction, (new_y,new_x) = path_steps[move_count]
                if(mangCuaPhong[new_y][new_x]==2 or mangCuaPhong[new_y][new_x]==3):
                    mangCuaPhong[new_y][new_x] = 0
                current_pos = (new_y,new_x)
                move_count+=1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    started = True 

            pygame.display.flip()
        pygame.quit()
