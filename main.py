@namespace
class SpriteKind:
    circle = SpriteKind.create()
    hoop = SpriteKind.create()

def on_up_pressed():
    make_one_hoop()
controller.up.on_event(ControllerButtonEvent.PRESSED, on_up_pressed)

def degrees_to_XY(degrees: number, Radius: number, Origin_X: number, Origin_Y: number):
    global radians, Point_X, Point_y
    radians = degrees * Pi / 180
    Point_X = Math.floor(Origin_X + Radius * Math.cos(radians))
    Point_y = Math.floor(Origin_Y + Radius * Math.sin(0 - radians))
def count_hoops_in_motion():
    global hoops_in_motion_return, distance_prior, this_hoop, This_hoop_size, N_this_hoop_points
    hoops_in_motion_return = 0
    update_ndx = 0
    while update_ndx <= len(hoop_list) - 1:
        distance_prior = distance_list[update_ndx]
        this_hoop = hoop_list[update_ndx]
        This_hoop_size = this_hoop.width
        N_this_hoop_points = 3 * this_hoop.width
        calc_distance_moved(update_ndx)
        if distance_return == 0:
            draw_circle(this_hoop, N_this_hoop_points, red)
            remove_slowest_hoop()
        else:
            hoops_in_motion_return += 1
            if distance_prior == 0:
                get_hoop_color(this_hoop)
                draw_circle(this_hoop, N_this_hoop_points, color_return)
        X_list[update_ndx] = X
        Y_list[update_ndx] = Y
        distance_list[update_ndx] = distance_return
        update_ndx += 1
def show_instructions_question():
    global msg
    if game.ask("Hula Hoop Instructions?"):
        msg = "If hoops stop moving, game ends, score = 0. "
        msg = "" + msg + "Player wins when level 4 countdown ends. "
        msg = "" + msg + "Score is the number of hoops in motion. "
        msg = "" + msg + "Up button adds a hoop.  "
        msg = "" + msg + "Down button removes slowest hoop. "
        msg = "" + msg + "Hearts indicate level from 1 to 4. "
        msg = "" + msg + "Level increases when a countdown ends. "
        msg = "" + msg + "Countdown starts at 10 seconds for level 1 "
        msg = "" + msg + "and adds 10 seconds per level. "
        msg = "" + msg + "Current countdown starts over when hoop is added.  "
        msg = "" + msg + "Countdown continues while hoops move. "
        msg = "" + msg + "As levels increase, hoops are more likely to follow and "
        msg = "" + msg + "launch more slowly; thus, have a greater tendency to stop moving. "
        msg = "" + msg + "More at wecodemakecode.com"
        game.show_long_text(msg, DialogLayout.FULL)

def on_on_overlap(sprite, otherSprite):
    global n_points
    if randint(0, stickiness) == 0:
        sprite.follow(otherSprite)
        n_points = 1 * sprite.width
        get_hoop_color(otherSprite)
        draw_circle(sprite, n_points, color_return)
        n_points = 3 * otherSprite.width
        draw_circle(otherSprite, n_points, color_return)
sprites.on_overlap(SpriteKind.hoop, SpriteKind.hoop, on_on_overlap)

def make_one_hoop():
    global side, hoop_img, new_hoop, sW_m1, sH_m1, clr_cnt, Hoop_color, New_countdown
    side = randint(16, 100)
    if side % 2 == 0:
        side += 1
    hoop_img = image.create(side, side)
    new_hoop = sprites.create(hoop_img, SpriteKind.hoop)
    sW_m1 = scene.screen_width() - 1
    sH_m1 = scene.screen_height() - 1
    new_hoop.x = randint(0, sW_m1)
    new_hoop.y = randint(0, sH_m1)
    hoop_list.append(new_hoop)
    X_list.append(new_hoop.x)
    Y_list.append(new_hoop.x)
    distance_list.append(-1)
    clr_cnt = (clr_cnt + 1) % 12
    Hoop_color = clr_cnt + 3
    Hoop_color_list.append(Hoop_color)
    draw_circle(new_hoop, 3.6 * side, Hoop_color)
    get_random_velocity()
    new_hoop.vx = v_return
    get_random_velocity()
    new_hoop.vy = v_return
    new_hoop.set_flag(SpriteFlag.BOUNCE_ON_WALL, True)
    New_countdown = True
def draw_circle(square: Sprite, pts: number, clr: number):
    global degrees_per_point, CenterX, CenterY, degrees
    degrees_per_point = Math.round(360 / pts)
    CenterX = square.width / 2
    CenterY = square.width / 2
    for Circle_ndx in range(360):
        degrees = Circle_ndx + 1
        if degrees % degrees_per_point == 0:
            degrees_to_XY(degrees, CenterX - 1, CenterX, CenterY)
            square.image.set_pixel(Point_X, Point_y, clr)
def calc_distance_moved(hoop_index_arg: number):
    global X, Y, X_prior, Y_prior, dx, dy, distance_prior, dx2, dy2, distance_return
    X = hoop_list[hoop_index_arg].x
    Y = hoop_list[hoop_index_arg].y
    X_prior = X_list[hoop_index_arg]
    Y_prior = Y_list[hoop_index_arg]
    dx = abs(X - X_prior)
    dy = abs(Y - Y_prior)
    distance_prior = distance_list[hoop_index_arg]
    dx2 = dx * dx
    dy2 = dy * dy
    distance_return = Math.sqrt(dx2 + dy2)
    distance_return = Math.floor(distance_return)
def remove_slowest_hoop():
    global B_changing_hoops, Min_dd, ndx, This_dd, min_ndx, this_hoop, Tmp_N
    B_changing_hoops = False
    Min_dd = 100
    ndx = 0
    if len(hoop_list) > 1:
        while ndx < len(hoop_list) - 2:
            This_dd = distance_list[ndx]
            if This_dd < Min_dd:
                Min_dd = This_dd
                min_ndx = ndx
            ndx += 1
        this_hoop = hoop_list.remove_at(min_ndx)
        Tmp_N = X_list.remove_at(min_ndx)
        Tmp_N = Y_list.remove_at(min_ndx)
        Tmp_N = distance_list.remove_at(min_ndx)
        Tmp_N = Hoop_color_list.remove_at(min_ndx)
        this_hoop.destroy()
def get_random_velocity():
    global v_return
    v_return = randint(10, max_velocity)
    if randint(0, 1) == 0:
        v_return = 0 - v_return

def on_countdown_end():
    global Level, max_velocity, stickiness, New_countdown
    if Level == levels:
        game.over(True)
    else:
        Level += 1
        info.set_life(Level)
        max_velocity = 100 / Level
        stickiness = stickiness - 10
        New_countdown = True
info.on_countdown_end(on_countdown_end)

def init_constants():
    global levels, change_per_level, s_pi, Pi, red
    levels = 4
    change_per_level = 10
    s_pi = "3.1415926535897932384626433832795"
    Pi = parse_float(s_pi)
    red = 2

def on_down_pressed():
    remove_slowest_hoop()
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

def get_hoop_color(sprite_arg: Sprite):
    global color_return, color_ndx
    color_return = 0
    color_ndx = 0
    while color_return == 0 and color_ndx < len(Hoop_color_list):
        if sprite_arg == hoop_list[color_ndx]:
            color_return = Hoop_color_list[color_ndx]
        color_ndx += 1
time = 0
color_ndx = 0
s_pi = ""
change_per_level = 0
levels = 0
Tmp_N = 0
min_ndx = 0
This_dd = 0
ndx = 0
Min_dd = 0
B_changing_hoops = False
dy2 = 0
dx2 = 0
dy = 0
dx = 0
Y_prior = 0
X_prior = 0
degrees = 0
CenterY = 0
CenterX = 0
degrees_per_point = 0
v_return = 0
Hoop_color = 0
sH_m1 = 0
sW_m1 = 0
new_hoop: Sprite = None
hoop_img: Image = None
side = 0
n_points = 0
msg = ""
Y = 0
X = 0
color_return = 0
red = 0
distance_return = 0
N_this_hoop_points = 0
This_hoop_size = 0
this_hoop: Sprite = None
distance_prior = 0
hoops_in_motion_return = 0
Point_y = 0
Point_X = 0
Pi = 0
radians = 0
max_velocity = 0
stickiness = 0
Level = 0
clr_cnt = 0
New_countdown = False
Hoop_color_list: List[number] = []
distance_list: List[number] = []
Y_list: List[number] = []
X_list: List[number] = []
hoop_list: List[Sprite] = []
cmt = "Code by " + "WeCodeMakeCode.com"
cmt = "Please " + "use, modify and learn"
hoop_list = sprites.all_of_kind(SpriteKind.hoop)
X_list = []
Y_list = []
distance_list = []
Hoop_color_list = []
New_countdown = False
clr_cnt = 11
Level = 1
# lower values are most sticky
stickiness = 31
max_velocity = 100 / Level
info.set_life(Level)
init_constants()
show_instructions_question()
make_one_hoop()
prior_time = game.runtime()

def on_on_update():
    global New_countdown, time, prior_time
    if New_countdown:
        New_countdown = False
        info.start_countdown(change_per_level * Level)
    time = game.runtime() - prior_time
    if time > 200:
        prior_time = game.runtime()
        count_hoops_in_motion()
        info.set_score(hoops_in_motion_return)
        if info.score() == 0:
            game.over(False)
game.on_update(on_on_update)
