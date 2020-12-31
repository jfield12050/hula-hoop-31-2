namespace SpriteKind {
    export const circle = SpriteKind.create()
    export const hoop = SpriteKind.create()
}
controller.up.onEvent(ControllerButtonEvent.Pressed, function () {
    make_one_hoop()
})
function degrees_to_XY (degrees: number, Radius: number, Origin_X: number, Origin_Y: number) {
    radians = degrees * Pi / 180
    Point_X = Math.floor(Origin_X + Radius * Math.cos(radians))
    Point_y = Math.floor(Origin_Y + Radius * Math.sin(0 - radians))
}
function count_hoops_in_motion () {
    hoops_in_motion_return = 0
    for (let update_ndx = 0; update_ndx <= hoop_list.length - 1; update_ndx++) {
        distance_prior = distance_list[update_ndx]
        this_hoop = hoop_list[update_ndx]
        This_hoop_size = this_hoop.width
        N_this_hoop_points = 3 * this_hoop.width
        calc_distance_moved(update_ndx)
        if (distance_return == 0) {
            draw_circle(this_hoop, N_this_hoop_points, red)
        } else {
            hoops_in_motion_return += 1
            if (distance_prior == 0) {
                get_hoop_color(this_hoop)
                draw_circle(this_hoop, N_this_hoop_points, color_return)
            }
        }
        X_list[update_ndx] = X
        Y_list[update_ndx] = Y
        distance_list[update_ndx] = distance_return
    }
}
function show_instructions_question () {
    if (game.ask("Hula Hoop Instructions?")) {
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
        game.showLongText(msg, DialogLayout.Full)
    }
}
sprites.onOverlap(SpriteKind.hoop, SpriteKind.hoop, function (sprite, otherSprite) {
    if (randint(0, stickiness) == 0) {
        sprite.follow(otherSprite)
        n_points = 1 * sprite.width
        get_hoop_color(otherSprite)
        draw_circle(sprite, n_points, color_return)
        n_points = 3 * otherSprite.width
        draw_circle(otherSprite, n_points, color_return)
    }
})
function make_one_hoop () {
    side = randint(16, 100)
    if (side % 2 == 0) {
        side += 1
    }
    hoop_img = image.create(side, side)
    new_hoop = sprites.create(hoop_img, SpriteKind.hoop)
    sW_m1 = scene.screenWidth() - 1
    sH_m1 = scene.screenHeight() - 1
    new_hoop.x = randint(0, sW_m1)
    new_hoop.y = randint(0, sH_m1)
    hoop_list.push(new_hoop)
    X_list.push(new_hoop.x)
    Y_list.push(new_hoop.x)
    distance_list.push(-1)
    clr_cnt = (clr_cnt + 1) % 12
    Hoop_color = clr_cnt + 3
    Hoop_color_list.push(Hoop_color)
    draw_circle(new_hoop, 3.6 * side, Hoop_color)
    get_random_velocity()
    new_hoop.vx = v_return
    get_random_velocity()
    new_hoop.vy = v_return
    new_hoop.setFlag(SpriteFlag.BounceOnWall, true)
    New_countdown = true
}
function draw_circle (square: Sprite, pts: number, clr: number) {
    degrees_per_point = Math.round(360 / pts)
    CenterX = square.width / 2
    CenterY = square.width / 2
    for (let Circle_ndx = 0; Circle_ndx <= 359; Circle_ndx++) {
        degrees = Circle_ndx + 1
        if (degrees % degrees_per_point == 0) {
            degrees_to_XY(degrees, CenterX - 1, CenterX, CenterY)
            square.image.setPixel(Point_X, Point_y, clr)
        }
    }
}
function calc_distance_moved (hoop_index_arg: number) {
    X = hoop_list[hoop_index_arg].x
    Y = hoop_list[hoop_index_arg].y
    X_prior = X_list[hoop_index_arg]
    Y_prior = Y_list[hoop_index_arg]
    dx = Math.abs(X - X_prior)
    dy = Math.abs(Y - Y_prior)
    distance_prior = distance_list[hoop_index_arg]
    dx2 = dx * dx
    dy2 = dy * dy
    distance_return = Math.sqrt(dx2 + dy2)
    distance_return = Math.floor(distance_return)
}
function remove_slowest_hoop () {
    B_changing_hoops = false
    Min_dd = 100
    ndx = 0
    if (hoop_list.length > 1) {
        while (ndx < hoop_list.length - 2) {
            This_dd = distance_list[ndx]
            if (This_dd < Min_dd) {
                Min_dd = This_dd
                min_ndx = ndx
            }
            ndx += 1
        }
        this_hoop = hoop_list.removeAt(min_ndx)
        Tmp_N = X_list.removeAt(min_ndx)
        Tmp_N = Y_list.removeAt(min_ndx)
        Tmp_N = distance_list.removeAt(min_ndx)
        Tmp_N = Hoop_color_list.removeAt(min_ndx)
        this_hoop.destroy()
    }
}
function get_random_velocity () {
    v_return = randint(10, max_velocity)
    if (randint(0, 1) == 0) {
        v_return = 0 - v_return
    }
}
info.onCountdownEnd(function () {
    if (Level == levels) {
        game.over(true)
    } else {
        Level += 1
        info.setLife(Level)
        max_velocity = 100 / Level
        stickiness = stickiness - 10
        New_countdown = true
    }
})
function init_constants () {
    levels = 4
    change_per_level = 10
    s_pi = "3.1415926535897932384626433832795"
    Pi = parseFloat(s_pi)
    red = 2
}
controller.down.onEvent(ControllerButtonEvent.Pressed, function () {
    remove_slowest_hoop()
})
function get_hoop_color (sprite_arg: Sprite) {
    color_return = 0
    color_ndx = 0
    while (color_return == 0 && color_ndx < Hoop_color_list.length) {
        if (sprite_arg == hoop_list[color_ndx]) {
            color_return = Hoop_color_list[color_ndx]
        }
        color_ndx += 1
    }
}
let time = 0
let color_ndx = 0
let s_pi = ""
let change_per_level = 0
let levels = 0
let Tmp_N = 0
let min_ndx = 0
let This_dd = 0
let ndx = 0
let Min_dd = 0
let B_changing_hoops = false
let dy2 = 0
let dx2 = 0
let dy = 0
let dx = 0
let Y_prior = 0
let X_prior = 0
let degrees = 0
let CenterY = 0
let CenterX = 0
let degrees_per_point = 0
let v_return = 0
let Hoop_color = 0
let sH_m1 = 0
let sW_m1 = 0
let new_hoop: Sprite = null
let hoop_img: Image = null
let side = 0
let n_points = 0
let msg = ""
let Y = 0
let X = 0
let color_return = 0
let red = 0
let distance_return = 0
let N_this_hoop_points = 0
let This_hoop_size = 0
let this_hoop: Sprite = null
let distance_prior = 0
let hoops_in_motion_return = 0
let Point_y = 0
let Point_X = 0
let Pi = 0
let radians = 0
let max_velocity = 0
let stickiness = 0
let Level = 0
let clr_cnt = 0
let New_countdown = false
let Hoop_color_list: number[] = []
let distance_list: number[] = []
let Y_list: number[] = []
let X_list: number[] = []
let hoop_list: Sprite[] = []
let cmt = "Code by " + "WeCodeMakeCode.com"
cmt = "Please " + "use, modify and learn"
hoop_list = sprites.allOfKind(SpriteKind.hoop)
X_list = []
Y_list = []
distance_list = []
Hoop_color_list = []
New_countdown = false
clr_cnt = 11
Level = 1
// lower values are most sticky
stickiness = 31
max_velocity = 100 / Level
info.setLife(Level)
init_constants()
show_instructions_question()
make_one_hoop()
let prior_time = game.runtime()
game.onUpdate(function () {
    if (New_countdown) {
        New_countdown = false
        info.startCountdown(change_per_level * Level)
    }
    time = game.runtime() - prior_time
    if (time > 200) {
        prior_time = game.runtime()
        count_hoops_in_motion()
        info.setScore(hoops_in_motion_return)
        if (info.score() == 0) {
            game.over(false)
        }
    }
})
