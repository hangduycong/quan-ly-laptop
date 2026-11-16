#!/usr/bin/env python3
"""Dựng 8 bộ cảnh 3D của tập 1 bằng Blender (bpy), đặt 7 nhân vật vào đúng chỗ và render ảnh bố cục cho từng cảnh quay.

Camera lấy từ tap01_du_lieu.SHOTS: cỡ cảnh (EWS … ECU), tiêu cự, góc cao/thấp, "qua vai". Vị trí nhân vật: STAGE (mặc định theo
bối cảnh) và OVR (ghi đè theo từng cảnh quay). Đây là ảnh BỐ CỤC (tham chiếu vị trí, cỡ cảnh, trục máy, ánh sáng) với nhân vật hình khối
từ dung_nhan_vat_blender.py, không phải ảnh phim cuối.

Chạy (cần bpy):
    python3 dung_canh_3d_tap01.py [--scenes 1 2 ...] [--shots 5 20 ...] [--out DIR] [--samples 20]
"""
import argparse
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dung_nhan_vat_blender as nv  # noqa: E402
from tap01_du_lieu import SCENES, SHOTS  # noqa: E402

RES = (960, 540)
SENSOR_H = 36 * 9 / 16  # mm
WALLS = []  # (object, pháp tuyến hướng vào trong, điểm trên tường)
CHARS = {}  # khóa -> dict(root, pose, H)


# ------------------------------------------------------------------ tiện ích ----
def hexc(c):
    return nv.hexc(c)


def emit_mat(color, strength):
    m = bpy.data.materials.new("emit")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = hexc(color)
    e.inputs["Strength"].default_value = strength
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], o.inputs[0])
    return m


def box(c, size, color, rough=0.85, rot=(0, 0, 0), emit=0.0):
    bpy.ops.mesh.primitive_cube_add(location=c)
    o = bpy.context.active_object
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    o.rotation_euler = rot
    nv.put(o, emit_mat(color, emit) if emit else nv.mat(color, rough), None, smooth=False)
    return o


def cyl(c, r, h, color, rot=(0, 0, 0), rough=0.8, verts=24, emit=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=c)
    o = bpy.context.active_object
    o.rotation_euler = rot
    nv.put(o, emit_mat(color, emit) if emit else nv.mat(color, rough), None)
    return o


def ball(c, r, color, rough=0.8, sc=(1, 1, 1), emit=0.0):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=c)
    o = bpy.context.active_object
    o.scale = (r * sc[0], r * sc[1], r * sc[2])
    nv.put(o, emit_mat(color, emit) if emit else nv.mat(color, rough), None)
    return o


def wall(c, size, color, normal, rough=0.9, emit=0.0):
    o = box(c, size, color, rough, emit=emit)
    WALLS.append((o, Vector(normal), Vector(c)))
    return o


def light_area(loc, target, energy, size, color=(1, 1, 1)):
    d = bpy.data.lights.new("a", "AREA")
    d.energy, d.size, d.color = energy, size, color
    o = bpy.data.objects.new("a", d)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()


def light_point(loc, energy, color=(1, 1, 1), radius=0.1):
    d = bpy.data.lights.new("p", "POINT")
    d.energy, d.color, d.shadow_soft_size = energy, color, radius
    o = bpy.data.objects.new("p", d)
    bpy.context.collection.objects.link(o)
    o.location = loc


def light_sun(rot_deg, energy, color=(1, 0.95, 0.85)):
    d = bpy.data.lights.new("s", "SUN")
    d.energy, d.color = energy, color
    o = bpy.data.objects.new("s", d)
    bpy.context.collection.objects.link(o)
    o.rotation_euler = tuple(math.radians(v) for v in rot_deg)


def rot_xy(dx, dy, deg):
    a = math.radians(deg)
    return dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a)


def chair(x, y, deg, color="#7A5A3C"):
    """Ghế cho nhân vật ngồi: mặt ghế dưới hông, tựa lưng ở phía sau (local +y)."""
    bx, by = rot_xy(0, 0.03, deg)
    box((x + bx, y + by, 0.43), (0.42, 0.42, 0.04), color, rot=(0, 0, math.radians(deg)))
    rx, ry = rot_xy(0, 0.21, deg)
    box((x + rx, y + ry, 0.72), (0.42, 0.04, 0.55), color, rot=(0, 0, math.radians(deg)))
    for sx in (-1, 1):
        for sy in (-1, 1):
            lx, ly = rot_xy(sx * 0.18, 0.03 + sy * 0.18, deg)
            box((x + lx, y + ly, 0.21), (0.04, 0.04, 0.42), color)


def new_scene(samples, world_color, world_strength):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    nv._MAT.clear()
    WALLS.clear()
    CHARS.clear()
    s = bpy.context.scene
    s.render.engine = "CYCLES"
    s.cycles.device = "CPU"
    s.cycles.samples = samples
    s.cycles.use_denoising = True
    s.cycles.max_bounces = 6
    s.render.resolution_x, s.render.resolution_y = RES
    s.view_settings.view_transform = "Standard"
    s.render.image_settings.file_format = "JPEG"
    s.render.image_settings.quality = 90
    w = bpy.data.worlds.new("w")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = hexc(world_color)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = world_strength
    s.world = w
    return s


def place(key, x, y, rot=0, pose="stand"):
    c = nv.NHAN_VAT[key]
    root, H = nv.build(key, c, "sit" if pose == "sit" else "stand")
    CHARS[key] = dict(root=root, pose=pose, H=H)
    move(key, x, y, rot, pose)


def move(key, x, y, rot=0, pose=None):
    ch = CHARS[key]
    pose = pose or ch["pose"]
    r = ch["root"]
    if pose == "lie":
        r.rotation_euler = (-math.pi / 2, 0, math.radians(rot))
        r.location = (x, y, ch.get("lie_z", 0.62))
    else:
        r.rotation_euler = (0, 0, math.radians(rot))
        r.location = (x, y, 0)
    ch["xy"] = (x, y)
    ch["rot"] = rot


def head_pos(key):
    ch = CHARS[key]
    x, y = ch["xy"]
    H = ch["H"]
    if ch["pose"] == "sit":
        return Vector((x, y, 0.70 * H))
    if ch["pose"] == "lie":
        return Vector((x, y + 0.93 * H, ch.get("lie_z", 0.62) + 0.10))
    return Vector((x, y, 0.93 * H))


# -------------------------------------------------------------------- bộ cảnh ----
def set_hanhlang():
    box((0, 1, -0.05), (2.6, 20, 0.1), "#7F8587")
    wall((-1.3, 1, 1.4), (0.1, 20, 2.8), "#B4C6B8", (1, 0, 0))
    wall((1.3, 1, 1.4), (0.1, 20, 2.8), "#B4C6B8", (-1, 0, 0))
    wall((0, 1, 2.85), (2.7, 20, 0.1), "#D0D3D0", (0, 0, -1))
    wall((0, -9, 1.4), (2.7, 0.1, 2.8), "#B4C6B8", (0, 1, 0))
    wall((0, 11, 1.4), (2.7, 0.1, 2.8), "#EAF1F5", (0, -1, 0), emit=0.9)  # cửa sổ cuối hành lang
    for y in (-4.4, -3.7, -3.0, -2.3):
        box((-1.05, y, 0.43), (0.42, 0.62, 0.05), "#58656B")
        box((-1.25, y, 0.72), (0.05, 0.62, 0.55), "#58656B")
    wall((1.27, 2.0, 1.05), (0.09, 1.1, 2.1), "#5A6670", (-1, 0, 0))  # khung cửa cấp cứu
    wall((1.22, 2.0, 1.0), (0.05, 0.9, 2.0), "#C9D0D4", (-1, 0, 0))
    for y in (-6, -2, 2, 6):
        light_area((0, y, 2.7), (0, y, 0), 45, 1.1, (0.85, 0.95, 1.0))
    light_area((0, 10.5, 1.4), (0, 0, 1.4), 60, 1.4, (0.9, 0.95, 1.0))


def set_phong():
    box((0, 0, -0.05), (7, 9, 0.1), "#8E948F")
    wall((-3.5, 0, 1.4), (0.1, 9, 2.8), "#B8C9B8", (1, 0, 0))
    wall((3.5, 0, 1.4), (0.1, 9, 2.8), "#B8C9B8", (-1, 0, 0))
    wall((0, 4.5, 1.4), (7, 0.1, 2.8), "#B8C9B8", (0, -1, 0))
    wall((0, -4.5, 1.4), (7, 0.1, 2.8), "#B8C9B8", (0, 1, 0))
    wall((0, 0, 2.85), (7, 9, 0.1), "#D0D3D0", (0, 0, -1))
    box((-3.43, 0.8, 1.6), (0.04, 2.2, 1.3), "#DCE8F0", emit=2.5)  # cửa sổ trái
    light_area((-3.2, 0.8, 1.6), (0, 0.8, 1.0), 200, 1.6, (0.85, 0.9, 1.0))
    for x in (-2.4, -0.8, 2.4):
        box((x, -0.05, 0.28), (0.9, 2.0, 0.45), "#8C9490")
        box((x, 0.8, 0.52), (0.6, 0.35, 0.1), "#E8E8E4")
    box((0.8, -0.05, 0.27), (0.9, 2.0, 0.45), "#6A7378")  # giường có người
    box((0.8, 0.85, 0.52), (0.6, 0.35, 0.1), "#EDEDE8")
    box((0.8, -0.65, 0.53), (0.86, 1.0, 0.07), "#A9C2D0")  # chăn che chân
    box((1.45, 1.0, 1.0), (0.04, 0.04, 2.0), "#9AA8AA")  # cột truyền dịch
    for y in (-2, 1.5):
        light_area((0, y, 2.7), (0, y, 0), 45, 1.4, (0.9, 0.97, 1.0))


def set_hien():
    box((0, -4, -0.1), (14, 16, 0.2), "#7C8A7C")  # sân
    box((0, 1.6, 0.0), (14, 3.4, 0.14), "#9A9F9A")  # nền hiên
    wall((0, 3.3, 1.5), (14, 0.2, 3.2), "#CFC7B5", (0, -1, 0))
    wall((0, 1.6, 2.95), (14, 3.8, 0.12), "#7A5A44", (0, 0, -1))  # mái hiên
    for x in (-3.8, 3.8):
        box((x, -0.1, 1.45), (0.18, 0.18, 2.9), "#8C867A")
    ball((-2.5, -7, 2.0), 1.6, "#35503A", sc=(1, 1, 1.3))  # cây ngoài sân
    cyl((-2.5, -7, 0.6), 0.14, 1.2, "#5A4632")
    random.seed(3)
    for _ in range(320):  # mưa
        box((random.uniform(-4.5, 4.5), random.uniform(-0.45, 0.2), random.uniform(0.2, 2.8)), (0.003, 0.003, 0.22), "#E6EEF5",
            rot=(0.05, 0, 0), emit=0.9)
    light_area((0, -3.5, 3.5), (0, 1.0, 0.8), 650, 4.0, (0.85, 0.9, 1.0))
    light_area((0, 1.6, 2.8), (0, 1.6, 0), 60, 2.0, (0.95, 0.95, 1.0))


def set_truongga():
    box((0, 3, -0.05), (24, 30, 0.1), "#6A5440")
    box((0, 14, -0.04), (3.0, 24, 0.1), "#86704F")  # đường đất dẫn ra lộ
    wall((0, 3, 3.4), (16, 14, 0.06), "#2C5B9A", (0, 0, -1))  # bạt xanh
    for x in (-6.5, 6.5):
        for y in (-2, 8):
            cyl((x, y, 1.7), 0.06, 3.4, "#9A8458")
    for x in (-5, -2.5, 0, 2.5, 5):
        ball((x, 1.2, 2.9), 0.09, "#FFD27A", emit=14.0)
        light_point((x, 1.2, 2.85), 220, (1.0, 0.72, 0.4), 0.1)
    random.seed(7)
    for i in range(30):  # đám đông nhìn từ phía sau
        ang = math.radians(195 + 150 * i / 29)
        x, y = 0 + 3.6 * math.cos(ang), 4.0 + 3.0 * math.sin(ang)
        hgt = random.uniform(0.9, 1.15)
        col = random.choice(["#1F2227", "#3A2F2A", "#2A3340", "#4A3B30", "#27302B"])
        cyl((x, y, 0.5 * hgt), 0.18, 1.0 * hgt, col)
        ball((x, y, 1.12 * hgt), 0.11, "#2B211C")
    box((6.2, -1.0, 0.8), (3.2, 1.6, 1.1), "#5C6B5E")  # xe tải nhỏ
    box((4.6, -1.0, 1.05), (0.9, 1.5, 1.2), "#4F5C52")
    for x in (-7.5, -4, 4.5, 8):
        cyl((x, 9, 2.4), 0.16, 4.8, "#3B2F22")
        ball((x, 9, 5.2), 1.4, "#1E3524", sc=(1.4, 1.4, 0.8))
    light_area((0, -6, 2.6), (0, 1.5, 1.0), 320, 5.0, (0.55, 0.65, 0.95))  # ánh trời chạng vạng


def set_nha_san():
    box((0, -2, -0.1), (22, 30, 0.2), "#7E6F52")  # nền đất
    box((0, 3.3, 0.15), (7.0, 2.2, 0.3), "#B7A98A")  # hiên
    wall((0, 4.5, 1.8), (8, 0.3, 3.6), "#D9CCA6", (0, -1, 0))
    box((0, 3.9, 3.7), (9, 3.4, 0.2), "#8A3F2E", rot=(0.18, 0, 0))  # mái ngói
    for x in (-3.2, 3.2):
        box((x, 2.3, 1.5), (0.2, 0.2, 3.0), "#7A5A44")
    box((0, 4.33, 1.2), (1.1, 0.06, 2.3), "#241C18")  # cửa nhà tối
    chair(-1.6, 3.4, 0, "#B33A3A")
    broken = chair(1.9, 3.4, 0, "#B33A3A")  # ghế gãy: nghiêng nhẹ phía chân gãy
    box((1.78, 3.62, 0.25), (0.05, 0.05, 0.2), "#2A2A2A")
    for sx in (-1, 1):  # cổng gỗ bong sơn
        box((sx * 1.7, -4.0, 0.9), (1.25, 0.08, 1.8), "#4C7A4A", rot=(0, 0, math.radians(-sx * 70)))
        box((sx * 4.0, -4.0, 0.8), (3.5, 0.12, 1.6), "#C9BC9A")
        box((sx * 4.0, -12, 1.6), (0.15, 15, 3.2), "#C4B79A")
    for x, y in ((-3.6, 0.5), (3.6, 1.0), (-4.2, 3.5)):
        cyl((x, y, 0.8), 0.12, 1.6, "#5A7A3A")
        for k in range(6):
            a = k * math.pi / 3
            box((x + 0.5 * math.cos(a), y + 0.5 * math.sin(a), 1.7), (0.15, 1.2, 0.04), "#4E8A3A", rot=(0, 0.5, a))
    cyl((4.8, 3.0, 1.3), 0.22, 2.6, "#5A4632")
    ball((4.8, 3.0, 3.2), 1.7, "#2F5A2E", sc=(1, 1, 0.9))  # cây mít
    cyl((-2.4, 2.3, 0.2), 0.3, 0.4, "#8A5A3A")
    ball((-2.4, 2.3, 0.75), 0.4, "#6B5B3A", sc=(1, 1, 0.8))  # chậu hoa giấy héo
    light_sun((55, 0, 110), 4.0, (1.0, 0.86, 0.66))
    light_area((0, -3, 4), (0, 2, 0.5), 200, 6.0, (0.85, 0.9, 1.0))


def set_nha_ban():
    box((0, 0.2, -0.05), (7.4, 7, 0.1), "#B08560")
    wall((-3.7, 0.2, 1.5), (0.1, 7, 3.0), "#D6C7A4", (1, 0, 0))
    wall((3.7, 0.2, 1.5), (0.1, 7, 3.0), "#D6C7A4", (-1, 0, 0))
    wall((0, 3.7, 1.5), (7.4, 0.1, 3.0), "#D6C7A4", (0, -1, 0))
    wall((0, -3.3, 1.5), (7.4, 0.1, 3.0), "#0F0D0B", (0, 1, 0))  # cửa trước tối
    wall((0, 0.2, 3.05), (7.4, 7, 0.1), "#5C4A3A", (0, 0, -1))
    box((0, 0, 0.74), (1.0, 2.6, 0.05), "#4A3220")  # bàn
    for sx in (-1, 1):
        for sy in (-1, 1):
            box((sx * 0.45, sy * 1.2, 0.37), (0.06, 0.06, 0.74), "#4A3220")
    cyl((0, 0.15, 0.82), 0.15, 0.1, "#5A2E22")  # nồi cá kho
    ball((0, 0.15, 0.88), 0.11, "#2A1812", sc=(1, 1, 0.5))
    for (x, y, c) in ((-0.30, 0.15, "#E9E4DA"), (0.30, 0.15, "#E9E4DA"), (0, 1.0, "#E9E4DA"), (0, -1.0, "#E9E4DA")):
        cyl((x, y, 0.80), 0.07, 0.05, c)  # chén cơm (chén gần máy để trống)
    cyl((0, 3.6, 2.1), 0.24, 0.05, "#F2EEE4", rot=(math.pi / 2, 0, 0))  # đồng hồ
    box((-2.4, 3.4, 0.55), (1.7, 0.45, 1.1), "#3A2418")  # tủ thờ
    ball((0, 0.2, 2.15), 0.07, "#FFD9A0", emit=20.0)
    light_point((0, 0.2, 2.1), 420, (1.0, 0.78, 0.5), 0.08)
    light_area((0, 0.2, 2.9), (0, 0.2, 0), 25, 5, (1.0, 0.85, 0.65))


def set_phongme():
    box((0, 0, -0.05), (5.4, 6.4, 0.1), "#8A6B4C")
    wall((-2.7, 0, 1.4), (0.1, 6.4, 2.8), "#C9B99A", (1, 0, 0))
    wall((2.7, 0, 1.4), (0.1, 6.4, 2.8), "#C9B99A", (-1, 0, 0))
    wall((0, 3.2, 1.4), (5.4, 0.1, 2.8), "#C9B99A", (0, -1, 0))
    wall((0, -3.2, 1.4), (5.4, 0.1, 2.8), "#C9B99A", (0, 1, 0))
    wall((0, 0, 2.85), (5.4, 6.4, 0.1), "#6B5A48", (0, 0, -1))
    box((0.6, 2.9, 1.0), (1.6, 0.6, 2.0), "#3A2418")  # tủ áo
    box((0.35, 2.58, 1.0), (0.78, 0.04, 1.9), "#4A2E1E", rot=(0, 0, math.radians(-105)))  # cánh trái mở
    box((0.6, 2.62, 1.0), (1.45, 0.02, 1.85), "#1A110B")  # ruột tủ
    cyl((0.4, 2.7, 0.16), 0.13, 0.1, "#7A7A7A")  # hộp bánh thiếc
    box((0.65, 2.7, 0.07), (0.5, 0.4, 0.05), "#777A7E")  # khăn xám
    box((0.45, 2.66, 0.025), (0.3, 0.22, 0.012), "#6B4A2E")  # phong bì nâu
    box((-1.9, 0.4, 0.25), (0.9, 2.0, 0.45), "#7A6A55")  # giường
    box((-1.9, 1.2, 0.5), (0.6, 0.35, 0.1), "#D8D0C0")
    box((-1.95, 2.0, 0.3), (0.45, 0.4, 0.6), "#4A2E1E")  # bàn đầu giường
    ball((-1.95, 2.0, 0.75), 0.07, "#FFC56A", emit=25.0)
    light_point((-1.9, 1.95, 0.85), 80, (1.0, 0.72, 0.38), 0.05)  # đèn ngủ vàng
    box((2.63, 0.2, 1.6), (0.04, 1.6, 1.3), "#7FA0E0", emit=2.0)  # cửa sổ xanh đêm
    light_area((2.4, 0.2, 1.6), (0, 0.2, 1.2), 150, 1.4, (0.45, 0.6, 1.0))


def set_sansau():
    box((0, 0, -0.1), (22, 18, 0.2), "#6F5E44")
    cyl((0, 2.2, 0.35), 0.55, 0.7, "#7B7C70")  # giếng gạch
    cyl((0, 2.2, 0.38), 0.4, 0.72, "#22262A")
    for x, y in ((-3.2, 5.0), (-1.2, 5.6), (2.6, 5.2), (4.2, 4.2)):
        cyl((x, y, 1.0), 0.13, 2.0, "#5A7A3A")
        for k in range(6):
            a = k * math.pi / 3
            box((x + 0.6 * math.cos(a), y + 0.6 * math.sin(a), 2.2), (0.16, 1.5, 0.04), "#4E8A3A", rot=(0, 0.5, a))
    box((0, 7.0, 0.9), (14, 0.15, 1.8), "#B5A98C")  # hàng rào
    box((-3.4, 3.0, 1.5), (0.2, 6, 3), "#CDBF9D")  # góc nhà bên trái
    light_sun((62, 0, -35), 3.2, (1.0, 0.88, 0.7))
    light_area((0, -4, 4), (0, 2, 1), 140, 5, (0.9, 0.93, 1.0))


# ------------------------------------------------------------- cấu hình theo cảnh ----
# (hàm dựng, màu trời, độ sáng trời, hướng nhìn mặc định (độ, 0 = nhìn về +Y), nhân vật mặc định: khóa -> (x, y, xoay, tư thế))
SCENE_CFG = {
    1: (set_hanhlang, "#9AA6AB", 0.3, 0, dict(minh=(0.15, 2.0, 0), nhung=(1.95, 2.0, -90))),
    2: (set_phong, "#9AA6AB", 0.3, 0, dict(**{"ba-thu": (0.8, -0.85, 0, "lie"), "yen": (-0.15, 0.55, 90, "sit"),
                                              "trang": (-2.9, 1.9, -90), "minh": (0.8, -1.6, 180)})),
    3: (set_hien, "#7E8A94", 0.8, 0, dict(trang=(-1.35, 1.2, 0), nhung=(-0.45, 1.2, 0), yen=(0.45, 1.2, 0), minh=(1.35, 1.2, 0))),
    4: (set_truongga, "#1D2B4A", 0.5, 0, {"ong-hai": (3.0, -1.0, -90), "thang": (1.9, -1.0, 90)}),
    5: (set_nha_san, "#BFD3E6", 1.2, 0, dict(minh=(0.0, -3.4, 180), trang=(0.5, 3.1, 0))),
    6: (set_nha_ban, "#3A2D22", 0.15, 0, dict(nhung=(0.0, 1.75, 0, "sit"), minh=(-0.95, 0.25, 90, "sit"), trang=(0.95, 0.25, -90, "sit"))),
    7: (set_phongme, "#1A2236", 0.2, 0, dict(minh=(0.6, 1.9, 180), trang=(0.0, -4.6, 180))),
    8: (set_sansau, "#CFE0EE", 1.0, 0, dict(minh=(0.4, 0.3, 0))),
}
# Ghi đè theo cảnh quay: id -> {khóa: (x, y, xoay[, tư thế])}
OVR = {
    1: dict(minh=(0.15, 6.8, 0)),
    4: dict(minh=(0.15, 2.0, 90), nhung=(0.95, 2.0, -90)),
    5: dict(minh=(0.15, 2.0, 90), nhung=(0.95, 2.0, -90)),
    6: dict(minh=(0.15, 2.0, 90), nhung=(0.95, 2.0, -90)),
    7: dict(minh=(1.55, 2.0, 90), nhung=(0.55, 2.0, 0)),
    16: {"trang": (1.9, -0.8, -90), "minh": (1.9, -1.7, -90)},
    17: {"trang": (1.9, -0.8, -90), "minh": (1.9, -1.7, -90)},
    10: {"minh": (0.15, -0.1, 90)},
    25: dict(nhung=(-0.45, 1.2, 90), minh=(0.45, 1.2, -90)), 26: dict(nhung=(-0.45, 1.2, 90), minh=(0.45, 1.2, -90)),
    27: dict(nhung=(-0.45, 1.2, 90), minh=(0.45, 1.2, -90)), 28: dict(nhung=(-0.45, 1.2, 90), minh=(0.45, 1.2, -90), trang=(-1.0, 1.2, 0)),
    29: dict(yen=(3.0, 1.2, 90)), 30: dict(yen=(3.0, 1.2, 90)), 31: dict(yen=(-0.1, 1.2, 0), nhung=(-0.9, 1.2, 0)),
    36: {"ong-hai": (3.0, -1.0, 0)},
    37: {"ong-hai": (3.0, -1.0, -90), "thang": (2.2, -1.0, 90)},
    38: {"ong-hai": (3.0, -1.0, -90), "thang": (2.2, -1.0, 90)},
    39: {"ong-hai": (3.0, -1.0, -90), "thang": (2.2, -1.0, 90)}, 40: {"ong-hai": (3.0, -1.0, -90), "thang": (2.2, -1.0, 90)},
    41: {"ong-hai": (3.0, -1.0, -90), "thang": (2.2, -1.0, 90)},
    43: {"ong-hai": (3.0, -1.0, 0)}, 44: {"ong-hai": (3.0, -1.0, 90)},
    48: dict(minh=(0.0, -9.0, 0)), 49: dict(minh=(0.0, -3.2, 180)),
    50: dict(minh=(0.0, -3.4, 180), trang=(0.5, 3.1, 0)),
    53: dict(minh=(0.0, 2.2, 0)), 54: dict(trang=(0.5, 3.1, 0)),
    75: dict(minh=(0.6, 1.9, 180)),
    80: {"minh": (-1.35, 0.4, 90, "sit")}, 81: {"minh": (-1.35, 0.4, 90, "sit")}, 88: {"minh": (-1.35, 0.4, 90, "sit")},
    76: dict(minh=(-0.6, 0.4, 180)), 77: dict(minh=(-0.6, 0.4, 180)),
    82: {"trang": (0.0, -2.7, 180), "minh": (-1.35, 0.4, 90, "sit")}, 83: {"trang": (0.0, -2.7, 180), "minh": (-1.35, 0.4, 90, "sit")},
    84: {"minh": (-1.35, 0.4, 90, "sit")}, 85: {"trang": (0.0, -2.7, 180), "minh": (-1.35, 0.4, 90, "sit")},
    86: dict(trang=(-1.2, 0.1, 180), minh=(-1.35, 0.4, 90, "sit")),
    87: dict(trang=(0.0, -2.7, 0), minh=(-1.35, 0.4, 90, "sit")),
    93: dict(minh=(0.4, -2.2, 0)),
}
# Hướng nhìn (độ) riêng cho từng cảnh quay; mặc định lấy từ SCENE_CFG
AZ = {13: 180, 82: 180, 83: 180, 84: -90, 85: 180, 86: 90, 87: 180, 8: 0, 20: 0, 21: 0, 48: 0, 49: 0, 61: 0, 60: 0,
      62: -90, 64: -90, 65: 0, 67: -90, 68: 0, 69: 90, 61: 90, 70: 0, 71: 0, 63: 0, 73: -90}
# Cảnh không có nhân vật: id -> (focus x, y, z, độ phủ dọc m, hướng nhìn độ)
INSERT = {
    11: (0.95, -0.1, 0.72, 0.45, -90), 34: (0, 3, 1.2, 9.0, 0), 35: (1.0, 2.2, 1.6, 3.0, 0), 38: (2.6, -1.0, 1.0, 0.45, 0), 45: (0, 12, 1.2, 6.0, 0),
    55: (1.9, 3.4, 0.4, 0.8, 0), 59: (0, 0.15, 0.85, 0.35, 0), 66: (0, 3.5, 2.1, 0.55, 0), 74: (-3.0, 3.0, 1.4, 3.0, 0),
    76: (0.5, 2.6, 0.2, 0.7, 0), 77: (0.5, 2.6, 0.15, 0.5, 0), 91: (0.4, 0.2, 1.0, 0.4, 0),
}
CHAR_COL = {"minh": "MINH", "ba-thu": "BÀ THU", "nhung": "NHUNG", "yen": "YẾN", "trang": "TRANG", "ong-hai": "ÔNG HẢI", "thang": "THẮNG"}

SIZE_COV = [("extreme wide", 7.5), ("extreme close", 0.30), ("medium close", 1.0), ("close", 0.62), ("medium", 1.7), ("wide", 3.4)]


def cover_of(framing):
    f = framing.lower()
    for k, v in SIZE_COV:
        if k in f:
            return v
    return 1.7


def lens_of(framing):
    import re
    m = re.search(r"(\d+)mm", framing)
    return float(m.group(1)) if m else 50.0


def camera_for(shot, scene_az):
    i, d, loc, chars, framing, kf, mv, motif, dlg, ai = shot
    f = lens_of(framing)
    fl = framing.lower()
    cov = cover_of(framing)
    az = AZ.get(i, scene_az)
    if not chars:
        if i in INSERT:
            fx, fy, fz, cov, az = INSERT[i]
            focus = Vector((fx, fy, fz))
        else:
            focus = Vector((0, 0, 1.2))
        dir_ = Vector((math.sin(math.radians(az)), math.cos(math.radians(az)), 0))
        dist = max(0.7, cov * f / SENSOR_H)
        cam = focus - dir_ * dist
        cam.z = focus.z + (0.0 if cov < 1 else 0.3)
        return cam, focus, f
    subj = chars[0]
    if "over" in fl and "shoulder" in fl and len(chars) >= 2:
        sh = chars[1]
        a = head_pos(sh)
        b = head_pos(subj)
        dir_ = (b - a)
        dir_.z = 0
        dir_.normalize()
        focus = b.copy()
        focus.z -= 0.05
        dist = max(0.9, cov * f / SENSOR_H)
        cam = a - dir_ * 0.35
        cam.z = a.z + 0.05
        # lùi ra sau vai để đủ cỡ cảnh: camera sau vai người kia, nhìn chủ thể
        cam = focus - dir_ * max(dist, (focus - a).length + 0.35)
        cam += Vector((-dir_.y, dir_.x, 0)) * 0.30  # lệch ngang để vai người kia nằm ở mép khung
        cam.z = a.z + 0.04
        return cam, focus, f
    pts = [head_pos(c) for c in chars]
    focus = sum(pts, Vector()) / len(pts)
    drop = {1.0: 0.18, 0.62: 0.05, 0.30: 0.02, 1.7: 0.30, 3.4: 0.55, 7.5: 0.75}.get(cov, 0.3)
    if "hand" in fl and cov <= 0.4:
        drop = 0.85
    focus.z -= drop
    dir_ = Vector((math.sin(math.radians(az)), math.cos(math.radians(az)), 0))
    perp = Vector((dir_.y, -dir_.x, 0))
    spread = (max((p - focus).dot(perp) for p in pts) - min((p - focus).dot(perp) for p in pts)) + 1.0 if len(pts) > 1 else 0
    cov = max(cov, spread * 1.15 * 9 / 16 * 1.0)
    dist = max(0.8, cov * f / SENSOR_H)
    cam = focus - dir_ * dist
    cam.z = focus.z + (0.0)
    if cov <= 1.0 and any(CHARS[c]["pose"] == "lie" for c in chars):  # cận mặt người nằm: nhìn chếch từ trên xuống
        cam = focus - dir_ * dist * 0.45
        cam.z = focus.z + dist * 0.85
        return cam, focus, f
    if "high angle" in fl or "above eye" in fl or "from a palm crown" in fl or "top-down" in fl:
        cam.z += dist * (0.55 if "palm" in fl else 0.25)
    if "low" in fl and "slow" not in fl.split("low")[-1][:1]:
        cam.z = max(0.35, cam.z - dist * 0.12)
    return cam, focus, f


def update_walls(cam):
    for o, n, p in WALLS:
        o.visible_camera = (cam - p).dot(n) > 0.05


def set_camera(cam_loc, focus, f):
    s = bpy.context.scene
    if s.camera is None:
        d = bpy.data.cameras.new("cam")
        d.sensor_fit = "VERTICAL"
        d.sensor_height = SENSOR_H
        o = bpy.data.objects.new("cam", d)
        bpy.context.collection.objects.link(o)
        s.camera = o
    c = s.camera
    c.data.lens = f
    c.location = cam_loc
    c.rotation_euler = (focus - cam_loc).to_track_quat("-Z", "Y").to_euler()
    update_walls(cam_loc)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scenes", nargs="*", type=int)
    ap.add_argument("--shots", nargs="*", type=int)
    ap.add_argument("--out", default=str(HERE.parent / "tap" / "hinh-3d-tap01"))
    ap.add_argument("--samples", type=int, default=20)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for n, (s0, s1, name) in enumerate(SCENES, 1):
        if a.scenes and n not in a.scenes:
            continue
        fn, wcol, wstr, az, stage = SCENE_CFG[n]
        shots = [s for s in SHOTS if s0 <= s[0] <= s1 and s[9] and (not a.shots or s[0] in a.shots)]
        if not shots:
            continue
        sc = new_scene(a.samples, wcol, wstr)
        fn()
        for key, v in stage.items():
            place(key, v[0], v[1], v[2], v[3] if len(v) > 3 else "stand")
            if len(v) > 3 and v[3] == "sit":
                chair(v[0], v[1], v[2])
        if n == 2:
            CHARS["ba-thu"]["lie_z"] = 0.62
            move("ba-thu", 0.8, -0.85, 0, "lie")
        for shot in shots:
            i = shot[0]
            for key, v in OVR.get(i, {}).items():
                if key in CHARS:
                    move(key, v[0], v[1], v[2], CHARS[key]["pose"])
            cam, focus, f = camera_for(shot, az)
            set_camera(cam, focus, f)
            sc.render.filepath = str(out / f"{i:02d}.jpg")
            bpy.ops.render.render(write_still=True)
            print(f"ok {i:02d}", flush=True)
            # trả nhân vật về vị trí mặc định cho cảnh quay sau
            for key, v in stage.items():
                move(key, v[0], v[1], v[2], CHARS[key]["pose"])


if __name__ == "__main__":
    main()
