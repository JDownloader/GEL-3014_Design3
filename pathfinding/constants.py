

CUBE_BUFFER_RADIUS = 300
TABLE_WALL_BUFFER = 200
TABLE_TOP_RIGHT_WALL = (0, 2310)
TABLE_BOTTOM_LEFT_WALL = (1110, 0)
TABLE_TOP_RIGHT_BUFFERED_WALL = (TABLE_TOP_RIGHT_WALL[0] + TABLE_WALL_BUFFER, TABLE_TOP_RIGHT_WALL[1] - TABLE_WALL_BUFFER)
TABLE_BOTTOM_LEFT_BUFFERED_WALL = (TABLE_BOTTOM_LEFT_WALL[0] - TABLE_WALL_BUFFER,
                                   TABLE_BOTTOM_LEFT_WALL[1] + TABLE_WALL_BUFFER)
ATLAS_ZONE_COORDINATES = (400, 400)
PRE_DROP_POINT = (700, 1000)
WAIT_ZONE = (850, 700)
