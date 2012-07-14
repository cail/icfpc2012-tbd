reachability_tests = [


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
#####''',
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
#######
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
######
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
