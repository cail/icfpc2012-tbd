reachability_tests = [

(r'''
#######################################
#****................#..1...\\\\\\\B..#
#R.......##############################
#.. ..................................#
#.. ........       \            ......#
#.. .*. ....**.*...#....... ..........#
#.. ... ....\\\\...#.A..... ..........#
#.. ... ....\ .....#.......    *  \\..#
#.. ... ....\......#....... ..........#
#.. ... ....\......#....... ..........#
#.. ... ...........#................**#
#..\\\\\...........#................\\#
########### ############## ############
#...*.................................#
#....*..................        ......#
#... .*....*.............. ..... .....#
#....*2*........########.. ..... .....L
#...*...*.......#\\\#..... ...*.......#
#.....\\\.......#\\\#....**..***......#
#....    .......#\\\#*................#
#...............#\\\#*...**...*.......#
#...............#.....................#
######       ############## ### #######
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#
#######################################

Trampoline A targets 1
Trampoline B targets 2''',

r'''
000000000000000000000000000000000000000
011111111111111111111011111111111111110
011111111000000000000000000000000000000
011111111111111111111111111111111111110
011111111111111111111111111111111111110
011111111111111111101111111111111111110
011111111111111111101111111111111111110
011111111111111111101111111111111111110
011111111111111111101111111111111111110
011111111111111111101111111111111111110
011111111111111111101111111111111111110
011111111111111111101111111111111111110
000000000001000000000000001000000000000
011111111111111111111111111111111111110
011111111111111111111111111111111111110
011111111111111111111111111111111111110
011111111111111100000000111111111111110
011111111111111101110111111111111111110
011111111111111101110111111111111111110
011111111111111101110111111111111111110
011111111111111101110111111111111111110
011111111111111101111111111111111111110
000000111111100000000000000100010000000
011111111111111111111111111111111111110
000000000000000000000000000000000000000'''),



(r'''
     ######
     #....#
     #.**.#
     #.**.#
     #.**.#
######.\\.######
#**....*.......#
#\\....L\\\....#
#A......*****..#
######R.....###########
     ###.....*.....\\\#
       #\\\\#..1...\\\#
       #\\\\#......\\\#
       ################

Trampoline A targets 1''',
r'''
00000000000000000000000
00000011110000000000000
00000011110000000000000
00000011110000000000000
00000011110000000000000
00000011110000000000000
01111111111111100000000
01111110111111100000000
01111111111111100000000
00000011111100000000000
00000000111111111111110
00000000111101111111110
00000000111101111111110
00000000000000000000000'''),

(r'''
############
#..*.R..*..#
#..A....B..######
#....2.. ..#\\\C#
#......* *.#\\\1#
########L########

Trampoline A targets 1
Trampoline B targets 1
Trampoline C targets 2''',
r'''
00000000000000000
01111111111000000
01111111111000000
01111111111011110
01111111111011110
00000000000000000
'''),

(r'''
######
#. *R#
#  \.#
#\ * #
L  .\#
######''',
'''
000000
011110
011110
011110
011110
000000'''),

(r'''
#####
# # #
##R##
# # #
####L''',
'''
00000
00000
00100
00000
00000'''),

(r'''
#######
#..***#
#..\\\#
#...**#
#.*.*\#
LR....#
#######''',
'''
0000000
0111110
0111110
0111110
0111110
0111110
0000000'''),

(r'''
L################
#           *...#
#        * \*..\#
#       #########
#   **          #
#  *..*    **   #
# *\  .*  *.\*  #
#*...R..**.  .* #
#################''',
'''
00000000000000000
01111111111111110
01111111111111110
01111111000000000
01111111111111110
01111111111001110
01111111110000110
00111111000000010
00000000000000000'''
),
(r'''
L######
#R #\\#
#  * .#
# *#..#
#######''',
'''
0000000
0110110
0111110
0100110
0000000'''
),
(r'''
####################
# R      #         #
#        .*     *  #
#        #\    *.* #
#   **   #**  *...*#
#LO#.#######.#######
#        #    #    #
#        #    .**  #
#        #    #**  #
#        #    ##   #
####################''',
'''
00000000000000000000
01111111101111111110
01111111111111111110
01111111101111111110
01110011100011111100
00000000000010000000
00000000001111011110
00000000001111111110
00000000001111001110
00000000001111001110
00000000000000000000'''
),
(r'''
L#####
#R.**#
# #**#
# ## #
######''',
r'''
000000
011110
010010
010010
000000'''
),
]





##################################################################

stone_reachability_tests = [


(r'''
######
#. *R#
#  \.#
#\ * #
L  .\#
######''',
'''
000000
001110
011110
011110
011110
000000'''),

(r'''
#######
#..***#
#..\\\#
#...**#
#.*.*\#
LR....#
#######''',
'''
0000000
0111110
0111110
0111110
0111110
0111110
0000000'''),

(r'''
L################
#           *...#
#        * \*..\#
#       #########
#   **          #
#  *..*    **   #
# *\  .*  *.\*  #
#*...R..**.  .* #
#################''',
'''
00000000000000000
00000000001111110
00000001111111110
00000011000000000
00111111100000000
01111111111111100
01111111111111110
01111111111111110
00000000000000000'''
),
(r'''
L######
#R #\\#
#  * .#
# *#..#
#######''',
'''
0000000
0000000
0111110
0110110
0000000'''
),
(r'''
####################
# R      #         #
#        .*     *  #
#        #\    *.* #
#   **   #**  *...*#
#LO#.#######.#######
#        #    #    #
#        #    .**  #
#        #    #**  #
#        #    ##   #
####################''',
'''
00000000000000000000
00000000000000000000
00000000111100111110
00000001101111111110
01111111101111111110
00001000000010000000
00011100000111000000
00111110001111111100
01111111001111011110
01111111101111001110
00000000000000000000'''
),
(r'''
################L
#R* #           #
#   #           #
#####           #
#               #
#               #
#               #
# *    #       *#
#################''',
'''
00000000000000000
00110000000000000
01110000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
01111110000000010
00000000000000000'''
),
]