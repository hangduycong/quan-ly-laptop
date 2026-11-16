#!/usr/bin/env python3
"""Dựng 3D (Blender / bpy) các nhân vật xuất hiện ở tập 1 từ thông số trong NHAN_VAT bên dưới
(khớp nhan-vat-3d/*.json và chuoi_nhan_dang.py). Mỗi nhân vật: bảng 3 góc (PNG), mô hình .glb.

Đây là mô hình người DỰNG BẰNG CODE từ hình khối: đúng chiều cao, vai, dáng, màu da, tóc, trang phục và các dấu nhận dạng
(sẹo, nốt ruồi...). Dùng làm tham chiếu tỉ lệ / tư thế / ánh sáng. KHÔNG phải mặt người "giống thật 90%":
mức đó cần mô hình quét 3D hoặc dựng từ ảnh nhân vật đã khóa (image-to-3D).

Chạy (cần gói bpy, Python 3.13):
    python3 dung_nhan_vat_blender.py [--only minh nhung] [--out DIR] [--samples 32] [--res 520x860]
"""
import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Euler, Matrix, Vector

# ---------------------------------------------------------------- thông số ----
# h: chiều cao (m); sw: bề rộng vai; hw: bề rộng hông; td: bề dày thân; fat: hệ số mập; stoop: độ cúi (độ);
# jaw: 0 thon → 1 vuông; skin/hair/eye: màu; cloth: danh sách (bộ phận → màu); marks: dấu nhận dạng
NHAN_VAT = {
    "minh": dict(ten="Minh (27)", h=1.72, sw=0.40, hw=0.30, td=0.20, fat=0.92, stoop=3, jaw=0.35, skin="#C99A74", hair="#1B1714",
                 hair_style="short_top", eye="monolid", brow=0.9, nose=0.9, lips=0.8,
                 top=("#242424", "coat"), under="#8A8D91", pants="#2A2A2D", shoes="#222222", sleeve="long",
                 marks=[("scar", "L", 0.0)], extra=["scarf"]),
    "ba-thu": dict(ten="Bà Thu (58)", h=1.52, sw=0.34, hw=0.34, td=0.21, fat=1.0, stoop=6, jaw=0.2, skin="#BE8F6C", hair="#8C8680",
                   hair_style="bun_low", eye="double", brow=0.8, nose=0.9, lips=0.7, wrinkles=True,
                   top=("#9C7F5F", "blouse"), under="#9C7F5F", pants="#2B2B2B", shoes="#3A3028", sleeve="long",
                   marks=[("mole", "R", 0.5)]),
    "nhung": dict(ten="Nhung (36)", h=1.60, sw=0.36, hw=0.33, td=0.20, fat=0.98, stoop=0, jaw=0.85, skin="#C4936C", hair="#14110F",
                  hair_style="ponytail_high", eye="monolid_sharp", brow=1.3, nose=1.0, lips=0.7,
                  top=("#EDEDED", "shirt"), under="#EDEDED", pants="#232326", shoes="#2A2A2A", sleeve="long_rolled",
                  marks=[("scar_chin", "C", 0.0)]),
    "yen": dict(ten="Yến (34)", h=1.55, sw=0.34, hw=0.32, td=0.19, fat=0.88, stoop=4, jaw=0.25, skin="#D0A07A", hair="#14110F",
                hair_style="long_clip", eye="large_down", brow=0.9, nose=0.8, lips=0.9,
                top=("#E8B8C0", "tee"), under="#E8B8C0", pants="#6F7F94", shoes="#C8B8A0", sleeve="short", skirt="#6F7F94",
                marks=[("mole_eye", "L", 0.0)]),
    "trang": dict(ten="Trang (31)", h=1.58, sw=0.36, hw=0.34, td=0.21, fat=1.08, stoop=0, jaw=0.45, skin="#C99A74", hair="#16120F",
                  hair_style="bob", eye="long_narrow", brow=1.0, nose=1.0, lips=1.0,
                  top=("#F2F2F2", "tee"), under="#F2F2F2", pants="#3E4A63", shoes="#555555", sleeve="short", apron="#2B7F84",
                  marks=[]),
    "ong-hai": dict(ten="Ông Hải (62)", h=1.68, sw=0.38, hw=0.30, td=0.19, fat=0.80, stoop=11, jaw=0.5, skin="#A97A56", hair="#CBC7C0",
                    hair_style="crop", eye="deep_tired", brow=1.1, nose=1.1, lips=0.6, wrinkles=True, stubble="#9A9893",
                    top=("#6E7A86", "checks"), under="#6E7A86", pants="#4A3E34", shoes="#2E2A26", sleeve="short",
                    marks=[("liver", "L", 0.0)]),
    "thang": dict(ten="Thắng (30)", h=1.78, sw=0.42, hw=0.31, td=0.20, fat=0.85, stoop=2, jaw=0.4, skin="#BF8C65", hair="#0F0D0B",
                  hair_style="spiky", eye="restless", brow=1.0, nose=1.0, lips=0.8,
                  top=("#171717", "tee"), under="#171717", pants="#2A2F3A", shoes="#EEEEEE", sleeve="short",
                  marks=[("scar_nose", "C", 0.0)], extra=["gold_chain"]),
}


def hexc(h, a=1.0):
    h = h.lstrip("#")
    lin = lambda c: ((c / 255 + 0.055) / 1.055) ** 2.4 if c / 255 > 0.04045 else c / 255 / 12.92
    return (lin(int(h[0:2], 16)), lin(int(h[2:4], 16)), lin(int(h[4:6], 16)), a)


_MAT = {}


def mat(color, rough=0.6, sss=0.0, name=None):
    key = (color, rough, sss)
    if key in _MAT:
        return _MAT[key]
    m = bpy.data.materials.new(name or f"m{len(_MAT)}")
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hexc(color)
    b.inputs["Roughness"].default_value = rough
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (1.0, 0.35, 0.2)
        b.inputs["Subsurface Scale"].default_value = 0.012
    _MAT[key] = m
    return m


def checks_mat(c1, c2):
    m = bpy.data.materials.new("checks")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexChecker")
    t.inputs["Color1"].default_value = hexc(c1)
    t.inputs["Color2"].default_value = hexc(c2)
    t.inputs["Scale"].default_value = 28
    co = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(co.outputs["Object"], t.inputs["Vector"])
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.85
    return m


def put(obj, m, parent=None, smooth=True):
    obj.data.materials.clear()
    obj.data.materials.append(m)
    if smooth:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.shade_smooth()
        obj.select_set(False)
    if parent:
        obj.parent = parent
        obj.matrix_parent_inverse = parent.matrix_world.inverted()
    return obj


def sphere(loc, scale, m, parent, seg=32, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, location=loc)
    o = bpy.context.active_object
    o.scale = scale
    return put(o, m, parent)


def limb(p0, p1, r0, r1, m, parent):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=r0, radius2=r1, depth=d.length, location=(p0 + p1) / 2)
    o = bpy.context.active_object
    o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    put(o, m, parent)
    sphere(p0, (r0, r0, r0), m, parent, 20, 10)
    sphere(p1, (r1, r1, r1), m, parent, 20, 10)
    return o


# ------------------------------------------------------------------ dựng ----
def build(key, c):
    H = c["h"]
    root = bpy.data.objects.new(f"{key}_root", None)
    bpy.context.collection.objects.link(root)
    hip_z = 0.53 * H
    pivot = bpy.data.objects.new(f"{key}_pivot", None)
    bpy.context.collection.objects.link(pivot)
    pivot.parent = root
    pivot.location = (0, 0, hip_z)
    pivot.rotation_euler = (0, 0, 0)  # cúi áp dụng sau cùng để matrix_parent_inverse không triệt tiêu
    P = pivot  # mọi thứ phía trên hông gắn vào P (toạ độ thế giới khi không cúi)
    skin = mat(c["skin"], 0.55, 0.25, "skin")
    cloth_c, kind = c["top"]
    cloth = mat(cloth_c, 0.85, 0, "cloth")
    pants = mat(c["pants"], 0.8, 0, "pants")
    shoes = mat(c["shoes"], 0.6, 0, "shoes")
    hairm = mat(c["hair"], 0.5, 0, "hair")
    dark = mat("#120E0C", 0.4)
    white = mat("#E9E4DA", 0.3)

    head_h = 0.132 * H
    chin_z = H - head_h
    neck_z = chin_z - 0.028 * H
    sh_z = neck_z - 0.012 * H
    sw, hw, td, fat = c["sw"], c["hw"], c["td"], c["fat"]

    def up(z):  # giữ nguyên toạ độ thế giới: put() đã bù phép biến đổi của pivot
        return z

    # ---- chân (không cúi: gắn vào root)
    for sx in (-1, 1):
        hipx = sx * hw * 0.28
        limb((hipx, 0, hip_z - 0.03), (sx * hw * 0.23, 0.005, 0.30 * H), 0.075 * fat, 0.055 * fat, pants, root)
        limb((sx * hw * 0.23, 0.005, 0.30 * H), (sx * hw * 0.22, 0, 0.055 * H), 0.055 * fat, 0.042 * fat, pants, root)
        sphere((sx * hw * 0.22, -0.045, 0.035 * H), (0.045, 0.115, 0.04), shoes, root)
    # váy (Yến)
    if c.get("skirt"):
        bpy.ops.mesh.primitive_cone_add(vertices=40, radius1=hw * 0.66, radius2=hw * 0.50, depth=0.42 * H, location=(0, 0, hip_z - 0.18 * H))
        sk = bpy.context.active_object
        put(sk, mat(c["skirt"], 0.9), root)
    # ---- khung chậu + thân
    sphere((0, 0, up(hip_z - 0.035 * H)), (hw / 2 + 0.01, td / 2 + 0.005, 0.06 * H), pants if not c.get("skirt") else mat(c["skirt"], 0.9), P)
    torso_len = (sh_z - hip_z)
    torso_m = cloth
    tor = sphere((0, 0, up(hip_z + torso_len * 0.47)), (sw / 2 * 0.92, td / 2 * fat, torso_len * 0.63), torso_m, P)
    if kind == "coat":  # áo khoác dài tới gối (~0.30H)
        coat_h = hip_z + 0.05 * H - 0.30 * H
        bpy.ops.mesh.primitive_cone_add(vertices=40, radius1=hw * 0.66, radius2=sw * 0.40, depth=coat_h,
                                        location=(0, 0, 0.30 * H + coat_h / 2))
        co = bpy.context.active_object
        co.scale = (1.0, td / sw * 2.0, 1.0)
        put(co, cloth, P)
    # áo trong / cổ áo
    if c.get("apron"):
        top_z, bot_z = sh_z - 0.07 * H, 0.36 * H
        bpy.ops.mesh.primitive_cube_add(location=(0, -(td / 2 * fat + 0.012), (top_z + bot_z) / 2))
        ap = bpy.context.active_object
        ap.scale = (sw * 0.30, 0.007, (top_z - bot_z) / 2)
        put(ap, mat(c["apron"], 0.9), P, smooth=False)
        for sx in (-1, 1):  # dây quàng cổ
            limb((sx * sw * 0.16, -(td / 2 * fat + 0.010), top_z), (sx * 0.03, -0.01, neck_z + 0.01), 0.006, 0.006, mat(c["apron"], 0.9), P)
    # ---- cổ + đầu
    limb((0, 0, up(neck_z - 0.01)), (0, -0.004, up(chin_z + 0.02 * H)), 0.058 * fat, 0.050 * fat, skin, P)
    head_c = Vector((0, 0, up(H - head_h * 0.5)))
    hw_, hd_, hh_ = 0.088 * (H / 1.7) * 1.0, 0.098 * (H / 1.7), head_h * 0.52
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, location=head_c)
    head = bpy.context.active_object
    head.scale = (hw_, hd_, hh_)
    # tạo hàm hàm hàm: chỉnh hàm — thu hẹp nửa dưới theo độ "thon/vuông"
    me = head.data
    jaw = c["jaw"]
    for v in me.vertices:
        if v.co.z < 0:
            t = -v.co.z  # 0..1
            narrow = 1 - (0.28 * (1 - jaw)) * (t ** 1.4) - 0.08 * t
            v.co.x *= narrow
            v.co.y *= 1 - 0.10 * t
            if jaw > 0.7:
                v.co.z *= 0.96  # cằm vuông, phẳng hơn
    put(head, skin, P)
    fz = lambda dz: head_c.z + dz * head_h  # cao độ trên mặt
    fy = -hd_ * 0.93  # mặt trước
    # tai
    for sx in (-1, 1):
        sphere((sx * hw_ * 0.97, 0.005, head_c.z - 0.01), (0.014, 0.022, 0.04), skin, P, 16, 8)
    # mũi
    nose = c["nose"]
    sphere((0, fy - 0.003, fz(-0.10)), (0.013 * nose, 0.015 * nose, 0.032 * nose), skin, P, 20, 10)
    sphere((0, fy - 0.010 * nose, fz(-0.165)), (0.015 * nose, 0.011, 0.011), skin, P, 20, 10)
    # mắt
    eye = c["eye"]
    for sx in (-1, 1):
        ex = sx * hw_ * 0.40
        ez = fz(0.06)
        sphere((ex, fy + 0.002, ez), (0.0165, 0.010, 0.0105 if "large" not in eye else 0.0135), white, P, 20, 10)
        sphere((ex, fy - 0.005, ez), (0.0075, 0.005, 0.0075), mat("#2B1B12", 0.2), P, 16, 8)
        # mí trên: một mí (monolid) = mí phủ thấp, khối mí phẳng; hai mí = mí cao hơn
        lid_h = {"monolid": 0.0072, "monolid_sharp": 0.0075, "double": 0.0050, "large_down": 0.0040, "long_narrow": 0.0070,
                 "deep_tired": 0.0080, "restless": 0.0065}[eye]
        sphere((ex, fy - 0.001, ez + 0.0085 - lid_h * 0.2), (0.0185, 0.0105, lid_h + 0.0035), skin, P, 20, 10)
        # lông mày
        tilt = 0.0
        if eye == "large_down":
            tilt = 0.25 * sx
        if eye in ("monolid_sharp",):
            tilt = -0.18 * sx
        bpy.ops.mesh.primitive_cube_add(location=(ex, fy - 0.003, ez + 0.032))
        br = bpy.context.active_object
        br.scale = (0.021, 0.004, 0.0035 * c["brow"])
        br.rotation_euler = (0, tilt, 0)
        put(br, hairm if c["hair"] not in ("#CBC7C0", "#8C8680") else mat("#6A645E", 0.6), P, smooth=False)
    # miệng
    sphere((0, fy - 0.004, fz(-0.30)), (0.024 * c["lips"] + 0.006, 0.006, 0.0042 * c["lips"] + 0.0012), mat("#7B3F3A", 0.5), P, 20, 10)
    if c.get("stubble"):
        for dz in (-0.26, -0.34):
            sphere((0, fy + 0.012, fz(dz)), (hw_ * 0.62, 0.02, 0.020), mat(c["stubble"], 0.9), P, 24, 8)
    if c.get("wrinkles"):
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_cube_add(location=(sx * hw_ * 0.43, fy - 0.002, fz(0.115)))
            w = bpy.context.active_object
            w.scale = (0.018, 0.002, 0.0009)
            put(w, mat("#6C4A37", 0.9), P, smooth=False)
    # dấu nhận dạng
    for kind_m, side, _ in c["marks"]:
        sx = {"L": 1, "R": -1, "C": 0}[side]  # chủ thể trái = +X (nhân vật nhìn về -Y)
        if kind_m == "scar":  # sẹo 1.5cm xuyên lông mày trái
            bpy.ops.mesh.primitive_cube_add(location=(sx * hw_ * 0.40 + 0.003, fy - 0.0055, fz(0.06) + 0.032))
            s = bpy.context.active_object
            s.scale = (0.0022, 0.0022, 0.0105)
            s.rotation_euler = (0, 0.45, 0)
            put(s, mat("#D9BBAA", 0.5), P, smooth=False)
        elif kind_m == "mole":  # nốt ruồi trên gò má phải
            sphere((sx * hw_ * 0.62, fy + 0.010, fz(-0.10)), (0.0065, 0.004, 0.0065), mat("#4A3022", 0.5), P, 12, 8)
        elif kind_m == "mole_eye":
            sphere((sx * hw_ * 0.40, fy + 0.002, fz(-0.03)), (0.004, 0.003, 0.004), mat("#2A1B12", 0.5), P, 12, 8)
        elif kind_m == "scar_chin":
            sphere((0, fy + 0.020, fz(-0.46)), (0.0045, 0.003, 0.0045), mat("#D2AE9E", 0.6), P, 12, 8)
        elif kind_m == "liver":
            sphere((sx * hw_ * 0.90, fy + 0.050, fz(0.06)), (0.010, 0.004, 0.010), mat("#4B2E20", 0.7), P, 12, 8)
        elif kind_m == "scar_nose":
            bpy.ops.mesh.primitive_cube_add(location=(0, fy - 0.022, fz(0.02)))
            s = bpy.context.active_object
            s.scale = (0.022, 0.0018, 0.0014)
            put(s, mat("#EBD6C8", 0.5), P, smooth=False)
    # ---- tóc
    hs = c["hair_style"]
    top = head_c.z
    def cap(scale_z=0.62, sy=1.05, dz=0.01, back=0.0):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=20, location=(0, back, top + dz))
        h = bpy.context.active_object
        h.scale = (hw_ * 1.06, hd_ * sy, hh_ * 1.04)
        # cắt nửa dưới: đẩy đỉnh z<-scale_z về scale_z (phủ nón + gáy, chừa trán/mặt)
        for v in h.data.vertices:
            if v.co.z < -scale_z * 0.15:
                v.co.z = -scale_z * 0.15 - (-(v.co.z) - scale_z * 0.15) * 0.1
            if v.co.y < -0.35 and v.co.z < 0.45:  # chừa trán thấy da
                v.co.y = -0.35 + (v.co.y + 0.35) * 0.3
        return put(h, hairm, P)
    if hs in ("short_top", "crop", "spiky", "bob", "ponytail_high", "long_clip", "bun_low"):
        cap()
    if hs in ("short_top", "crop", "spiky", "ponytail_high"):  # che gáy
        sphere((0, hd_ * 0.30, top - hh_ * 0.20), (hw_ * 1.03, hd_ * 0.72, hh_ * 0.78), hairm, P)
    if hs == "short_top":
        sphere((hw_ * 0.20, -hd_ * 0.42, top + hh_ * 0.78), (hw_ * 0.60, hd_ * 0.34, hh_ * 0.12), hairm, P)  # phần trên dài hơn, rũ về phải
    if hs == "spiky":
        for k in range(7):
            a = k / 6 * math.pi
            x = math.cos(a) * hw_ * 0.7
            bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.016, radius2=0.002, depth=0.05, location=(x, -hd_ * 0.40, top + hh_ * 0.98))
            sp = bpy.context.active_object
            sp.rotation_euler = (math.radians(-35), 0, 0)
            put(sp, hairm, P)
    if hs == "ponytail_high":
        limb((0, hd_ * 0.55, top + hh_ * 0.75), (0, hd_ * 1.25, top - hh_ * 0.55), 0.028, 0.016, hairm, P)
    if hs == "bun_low":
        sphere((0, hd_ * 0.95, top - hh_ * 0.30), (0.05, 0.045, 0.048), hairm, P)
    if hs == "long_clip":
        sphere((0, hd_ * 0.50, top - hh_ * 0.95), (hw_ * 1.02, hd_ * 0.50, hh_ * 1.55), hairm, P)
        sphere((0.05, hd_ * 0.55, top + hh_ * 0.7), (0.025, 0.02, 0.018), mat("#6B4A3A", 0.6), P, 12, 8)
    if hs == "bob":
        sphere((0, hd_ * 0.30, top - hh_ * 0.55), (hw_ * 1.12, hd_ * 0.95, hh_ * 0.85), hairm, P)
        sphere((0, -hd_ * 0.15, top - hh_ * 0.52), (hw_ * 0.93, hd_ * 0.55, hh_ * 0.58), skin, P)  # lộ mặt ở phía trước
    # ---- tay
    sleeve = c["sleeve"]
    sleeve_m = cloth if kind != "coat" else cloth
    for sx in (-1, 1):
        sj = Vector((sx * (sw / 2 + 0.005), 0.0, up(sh_z - 0.025 * H)))
        elbow = Vector((sx * (sw / 2 + 0.03), 0.005, up(0.64 * H)))
        wrist = Vector((sx * (sw / 2 + 0.045), -0.01, up(0.47 * H)))
        r_up, r_lo = 0.040 * fat, 0.030 * fat
        upper_m = sleeve_m
        lower_m = sleeve_m if sleeve.startswith("long") else skin
        if sleeve == "long_rolled":
            mid = elbow.lerp(wrist, 0.2)
            limb(sj, elbow, r_up * 1.2, r_up, sleeve_m, P)
            limb(elbow, mid, r_up, r_lo * 1.15, sleeve_m, P)
            limb(mid, wrist, r_lo * 1.0, r_lo * 0.85, skin, P)
        elif sleeve == "short":
            mid = sj.lerp(elbow, 0.55)
            limb(sj, mid, r_up * 1.25, r_up * 1.1, sleeve_m, P)
            limb(mid, elbow, r_up * 1.0, r_up * 0.9, skin, P)
            limb(elbow, wrist, r_lo * 1.05, r_lo * 0.85, skin, P)
        else:
            limb(sj, elbow, r_up * 1.25, r_up * 1.05, upper_m, P)
            limb(elbow, wrist, r_up * 1.05, r_lo * 1.0, lower_m, P)
        sphere(wrist + Vector((0, -0.01, -0.07)), (0.036, 0.022, 0.058), skin, P, 20, 10)
        # móng tay / ngón: một khối bàn tay mỏng
    # phụ kiện
    if "scarf" in c.get("extra", []):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.07, minor_radius=0.028, location=(0, -0.005, up(neck_z + 0.01)))
        put(bpy.context.active_object, mat("#6B6F73", 0.95), P)
    if "gold_chain" in c.get("extra", []):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.072, minor_radius=0.0065, location=(0, -0.025, up(neck_z - 0.02)))
        ch = bpy.context.active_object
        put(ch, mat("#D4AF37", 0.25), P)
        ch.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0
    pivot.rotation_euler = (math.radians(c["stoop"]), 0, 0)
    return root, H


# --------------------------------------------------------------- cảnh + render ----
def setup_scene(w, h, samples):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = "CYCLES"
    s.cycles.device = "CPU"
    s.cycles.samples = samples
    s.cycles.use_denoising = True
    s.render.resolution_x, s.render.resolution_y = w, h
    s.render.film_transparent = False
    s.view_settings.view_transform = "Standard"
    s.view_settings.look = "None"
    s.render.image_settings.file_format = "PNG"
    # nền xám phẳng + sàn
    wd = bpy.data.worlds.new("w")
    wd.use_nodes = True
    bg = wd.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = hexc("#B9B9B9")
    bg.inputs["Strength"].default_value = 0.9
    s.world = wd
    bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
    fl = bpy.context.active_object
    fl.data.materials.append(mat("#8F8F8F", 0.95, 0, "floor"))
    return s


def lights(H):
    def area(loc, energy, size, name):
        d = bpy.data.lights.new(name, "AREA")
        d.energy, d.size = energy, size
        o = bpy.data.objects.new(name, d)
        bpy.context.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = (Vector((0, 0, H * 0.55)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    area((-2.2, -3.0, 2.6), 260, 2.4, "key")
    area((2.8, -2.4, 1.4), 90, 3.0, "fill")
    area((0.5, 3.2, 2.8), 140, 2.0, "rim")


def camera(H, loc_y=-5.0, f=85):
    cam = bpy.data.cameras.new("cam")
    cam.lens = f
    cam.sensor_width = 36
    o = bpy.data.objects.new("cam", cam)
    bpy.context.collection.objects.link(o)
    o.location = (0, loc_y, H * 0.52)
    o.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.camera = o
    return o


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent / "nhan-vat-3d" / "blender"))
    ap.add_argument("--samples", type=int, default=32)
    ap.add_argument("--res", default="520x860")
    ap.add_argument("--no-glb", action="store_true")
    a = ap.parse_args()
    w, h = map(int, a.res.split("x"))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    keys = a.only or list(NHAN_VAT)
    for key in keys:
        c = NHAN_VAT[key]
        s = setup_scene(w, h, a.samples)
        _MAT.clear()
        root, H = build(key, c)
        lights(H)
        camera(H)
        views = [("truoc", 0), ("ba-phan-tu", 40), ("sau", 180)]
        for name, deg in views:
            root.rotation_euler = (0, 0, math.radians(deg))
            s.render.filepath = str(out / f"{key}_{name}.png")
            bpy.ops.render.render(write_still=True)
        # ảnh cận mặt (kiểm tra dấu nhận dạng)
        cam = bpy.context.scene.camera
        cam.location = (0, -1.25, H - 0.132 * H * 0.5)
        root.rotation_euler = (0, 0, 0)
        s.render.filepath = str(out / f"{key}_mat.png")
        bpy.ops.render.render(write_still=True)
        cam.location = (0, -5.0, H * 0.52)
        if not a.no_glb:
            # glTF chỉ xuất nhân vật
            bpy.ops.object.select_all(action="DESELECT")
            def sel(o):
                o.select_set(True)
                for ch in o.children:
                    sel(ch)
            sel(root)
            bpy.ops.export_scene.gltf(filepath=str(out / f"{key}.glb"), use_selection=True, export_format="GLB")
        print(f"ok {key}", flush=True)


if __name__ == "__main__":
    main()
