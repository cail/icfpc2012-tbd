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
001110
001110
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
#################
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
00000001000000000
00111111000000000
01111111111111100
01111111111111110
01111111111111110
00000000000000000'''
),
(r'''
#######
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
00000000101111111110
01111111101111111110
00001000000010000000
00001000000010000000
00001000000011111100
00001000000011011100
01111111101111001110
00000000000000000000'''

)
]
