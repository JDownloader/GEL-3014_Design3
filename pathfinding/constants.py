

CUBE_BUFFER_RADIUS = 300
TABLE_WALL_BUFFER = 200
TABLE_TOP_RIGHT_WALL = (0, 2310)
TABLE_BOTTOM_LEFT_WALL = (1110, 0)
TABLE_TOP_RIGHT_BUFFERED_WALL = (TABLE_TOP_RIGHT_WALL[0] + TABLE_WALL_BUFFER, TABLE_TOP_RIGHT_WALL[1] - TABLE_WALL_BUFFER)
TABLE_BOTTOM_LEFT_BUFFERED_WALL = (TABLE_BOTTOM_LEFT_WALL[0] - TABLE_WALL_BUFFER,
                                   TABLE_BOTTOM_LEFT_WALL[1] + TABLE_WALL_BUFFER)
ATLAS_ZONE_COORDINATES = (400, 400)
DOCK_POINT = (600, 700)
DOCK_ANGLE = 180
SAFE_POINT = (850, 700)
SAFE_AND_DOCK_POINT_INTERMEDIATE = (0, 0)
WIDTH_DISTANCE_TO_MOVE_TO_CHANGE_FLAG_COLUMN = 110
LENGTH_DISTANCE_TO_CHANGE_FLAG_ROW = 110
FIRST_CUBE_DROP_POSITION = {'direction': 'right',
                            'width_distance': WIDTH_DISTANCE_TO_MOVE_TO_CHANGE_FLAG_COLUMN,
                            'length_distance': 3 * LENGTH_DISTANCE_TO_CHANGE_FLAG_ROW}
SECOND_CUBE_DROP_POSITION = {'direction': 'forward',
                             'width_distance': 0 * WIDTH_DISTANCE_TO_MOVE_TO_CHANGE_FLAG_COLUMN,
                             'length_distance': 3 * LENGTH_DISTANCE_TO_CHANGE_FLAG_ROW}
THIRD_CUBE_DROP_POSITION = {'direction': 'left',
                            'width_distance': WIDTH_DISTANCE_TO_MOVE_TO_CHANGE_FLAG_COLUMN,
                            'length_distance': 3 * LENGTH_DISTANCE_TO_CHANGE_FLAG_ROW}
FOURTH_CUBE_DROP_POSITION = {'direction': 'right',
                             'width_distance': WIDTH_DISTANCE_TO_MOVE_TO_CHANGE_FLAG_COLUMN,
                             'length_distance': 2* LENGTH_DISTANCE_TO_CHANGE_FLAG_ROW}
FIFTH_CUBE_DROP_POSITION = {'direction': 'forward',
                            'width_distance': 0 * WIDTH_DISTANCE_TO_MOVE_TO_CHANGE_FLAG_COLUMN,
                            'length_distance': 2 * LENGTH_DISTANCE_TO_CHANGE_FLAG_ROW}
SIXTH_CUBE_DROP_POSITION = {'direction': 'left',
                            'width_distance': WIDTH_DISTANCE_TO_MOVE_TO_CHANGE_FLAG_COLUMN,
                            'length_distance': 2 * LENGTH_DISTANCE_TO_CHANGE_FLAG_ROW}
SEVENTH_CUBE_DROP_POSITION = {'direction': 'right',
                              'width_distance': WIDTH_DISTANCE_TO_MOVE_TO_CHANGE_FLAG_COLUMN,
                              'length_distance': LENGTH_DISTANCE_TO_CHANGE_FLAG_ROW}
EIGHT_CUBE_DROP_POSITION = {'direction': 'forward',
                            'width_distance': 0 * WIDTH_DISTANCE_TO_MOVE_TO_CHANGE_FLAG_COLUMN,
                            'length_distance': LENGTH_DISTANCE_TO_CHANGE_FLAG_ROW}
NINTH_CUBE_DROP_POSITION = {'direction': 'left',
                            'width_distance': WIDTH_DISTANCE_TO_MOVE_TO_CHANGE_FLAG_COLUMN,
                            'length_distance': LENGTH_DISTANCE_TO_CHANGE_FLAG_ROW}
CUBE_DROP_MOVEMENTS_LIST = [FIRST_CUBE_DROP_POSITION, SECOND_CUBE_DROP_POSITION, THIRD_CUBE_DROP_POSITION, FOURTH_CUBE_DROP_POSITION, FIFTH_CUBE_DROP_POSITION, SIXTH_CUBE_DROP_POSITION,
                            SEVENTH_CUBE_DROP_POSITION, EIGHT_CUBE_DROP_POSITION, NINTH_CUBE_DROP_POSITION]
