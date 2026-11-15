# Prompt hình ảnh — Tập 1: Về nhà

> Sinh tự động bởi `cong-cu/tao_prompt_tap01.py` từ `cong-cu/tap01_du_lieu.py` (93 cảnh, khớp `tap-01-danh-sach-canh-quay.md`) và `cong-cu/chuoi_nhan_dang.py`. Viết theo skill `mo-phong-cong-viec-dao-dien` (Visual Skills của **Serge Shima**, CC BY 4.0 — https://github.com/smixs/visual-skills) và `ho-tro-danh-sach-canh-quay` (DirectorSKILL). Sửa dữ liệu rồi chạy lại script; đừng sửa tay file này.

## Quy trình

1. **Ảnh bối cảnh trống** (mục A): GPT Image 2.5 Sunburst, `quality: medium`, `size: 1536x864`. Chọn một ảnh mỗi bối cảnh, dùng lại cho mọi cảnh.
2. **Chân dung khóa nhận dạng**: theo `../nhan-vat-3d/prompt-anh-nhan-vat.md`.
3. **Keyframe từng cảnh** (mục B): GPT Image 2.5 Sunburst chế độ edit, đính kèm đúng các ảnh tham chiếu ghi ở dòng `References`. `quality: medium`, `size: 1536x864`. Kiểm tra: đúng số người, dấu nhận dạng đúng chỗ, không có chữ.
4. **Clip** (mục B, khối Kling): Kling 3.0 image-to-video, keyframe làm ảnh đầu, `duration` = số giây ghi ở cảnh (tối thiểu theo công cụ, cắt lại khi dựng), `aspect_ratio: 16:9`, `cfg_scale: 0.6`, **`generate_audio: false`**. Cảnh Vàng: tạo 2–3 bản, chọn một; Xanh: 1–2 bản.
5. **Tiếng**: thu giọng diễn viên (hoặc lồng tiếng) theo thoại ghi ở từng cảnh; nhép môi khi dựng hoặc bằng chức năng lip-sync của công cụ nếu có. Không tin vào âm thanh do model video tự sinh cho tiếng Việt.
6. **Dựng**: ghép theo thứ tự cảnh bằng skill `bien-tap` (phụ đề tiếng Việt, nhạc nền, chuẩn âm lượng).

Cảnh **không tạo AI** (có chữ tiếng Việt trong khung): 02, 42, 72, 78, 79 — quay đạo cụ thật hoặc làm đồ họa khi dựng. Cảnh 47: bảng chỉ đường thêm khi dựng.

## A. Ảnh bối cảnh trống (8)

### `bv_hanhlang` — Hành lang bệnh viện tỉnh, sáng sớm

```text
Scene: a long provincial hospital corridor at dawn, pale green walls, scuffed grey floor tiles, a row of joined plastic chairs along the left wall, a window at the far end
Subject: the empty location itself, no people
Important Details: flat cold fluorescent light from ceiling tubes, one tube flickering at the far end, grey dawn light from the end window; the flickering tube at the far end; real wear: scuffs, water stains, faded paint, dust in corners; a real photograph from a location scout, natural light, no retouch, fine sensor noise, muted colour
Use Case: background plate for keyframes of a Vietnamese family drama, reused across many shots
Constraints: no people, no animals, no readable text or signs, no watermark, not a 3D render, 16:9 composition with the main action area left clear
```

### `bv_phong` — Phòng bệnh 4 giường

```text
Scene: a four-bed provincial hospital ward, three beds empty with folded grey blankets, metal bed rails, a dusty window on the left, an IV stand
Subject: the empty location itself, no people
Important Details: grey overcast morning light from the left window, weak fluorescent fill from above; an IV drip falling slowly in its chamber; real wear: scuffs, water stains, faded paint, dust in corners; a real photograph from a location scout, natural light, no retouch, fine sensor noise, muted colour
Use Case: background plate for keyframes of a Vietnamese family drama, reused across many shots
Constraints: no people, no animals, no readable text or signs, no watermark, not a 3D render, 16:9 composition with the main action area left clear
```

### `bv_hien` — Mái hiên bệnh viện, mưa

```text
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree
Subject: the empty location itself, no people
Important Details: soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge; water pouring off the roof edge in a steady sheet; real wear: scuffs, water stains, faded paint, dust in corners; a real photograph from a location scout, natural light, no retouch, fine sensor noise, muted colour
Use Case: background plate for keyframes of a Vietnamese family drama, reused across many shots
Constraints: no people, no animals, no readable text or signs, no watermark, not a 3D render, 16:9 composition with the main action area left clear
```

### `truongga` — Trường gà ven sông, chạng vạng

```text
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge
Subject: the empty location itself, no people
Important Details: a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke; bare bulbs swinging slightly on their wire; real wear: scuffs, water stains, faded paint, dust in corners; a real photograph from a location scout, natural light, no retouch, fine sensor noise, muted colour
Use Case: background plate for keyframes of a Vietnamese family drama, reused across many shots
Constraints: no people, no animals, no readable text or signs, no watermark, not a 3D render, 16:9 composition with the main action area left clear
```

### `nha_san` — Ngõ, cổng gỗ, sân nhà cũ

```text
Scene: a narrow Mekong Delta lane leading to an old two-storey house with a tiled roof, a wooden gate with peeling green paint, a yard with banana plants, an old jackfruit tree, a pot of dried bougainvillea, two plastic chairs on the porch, one missing its back left leg
Subject: the empty location itself, no people
Important Details: low late-afternoon sun after rain from camera right, wet leaves catching light, puddles on packed earth; water dripping from banana leaves; real wear: scuffs, water stains, faded paint, dust in corners; a real photograph from a location scout, natural light, no retouch, fine sensor noise, muted colour
Use Case: background plate for keyframes of a Vietnamese family drama, reused across many shots
Constraints: no people, no animals, no readable text or signs, no watermark, not a 3D render, 16:9 composition with the main action area left clear
```

### `nha_ban` — Bàn ăn giữa nhà

```text
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty
Subject: the empty location itself, no people
Important Details: a single warm tungsten bulb hanging over the table, the doorway behind dark; the wall clock's second hand ticking; real wear: scuffs, water stains, faded paint, dust in corners; a real photograph from a location scout, natural light, no retouch, fine sensor noise, muted colour
Use Case: background plate for keyframes of a Vietnamese family drama, reused across many shots
Constraints: no people, no animals, no readable text or signs, no watermark, not a 3D render, 16:9 composition with the main action area left clear
```

### `nha_phongme` — Phòng Mẹ, tầng hai, đêm

```text
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table
Subject: the empty location itself, no people
Important Details: a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window; the yellow lamp glow on the wardrobe wood; real wear: scuffs, water stains, faded paint, dust in corners; a real photograph from a location scout, natural light, no retouch, fine sensor noise, muted colour
Use Case: background plate for keyframes of a Vietnamese family drama, reused across many shots
Constraints: no people, no animals, no readable text or signs, no watermark, not a 3D render, 16:9 composition with the main action area left clear
```

### `nha_sansau` — Sân sau, giếng nước, sáng sớm

```text
Scene: the back yard of the same old house, a round brick well with moss, a plastic bucket on a rope, banana plants, damp earth
Subject: the empty location itself, no people
Important Details: low soft morning sun raking across the yard from camera left, faint mist; mist lifting off the damp ground; real wear: scuffs, water stains, faded paint, dust in corners; a real photograph from a location scout, natural light, no retouch, fine sensor noise, muted colour
Use Case: background plate for keyframes of a Vietnamese family drama, reused across many shots
Constraints: no people, no animals, no readable text or signs, no watermark, not a 3D render, 16:9 composition with the main action area left clear
```

## B. Keyframe + chuyển động theo từng cảnh

### Cảnh 1 · Hành lang bệnh viện (cảnh 01–07)

Năm điểm neo — cảm xúc: xa cách · mô-típ: ánh đèn huỳnh quang chớp · đồ vật: hồ sơ bệnh án · điểm vỡ: Nhung khựng lại khi thấy Minh · hình cuối: Nhung đứng nhìn hành lang trống

#### 01 · 6s · MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hanhlang` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a long provincial hospital corridor at dawn, pale green walls, scuffed grey floor tiles, a row of joined plastic chairs along the left wall, a window at the far end; flat cold fluorescent light from ceiling tubes, one tube flickering at the far end, grey dawn light from the end window
Subject: MINH is a small figure entering at the far end of the empty corridor carrying a black duffel bag in his right hand. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: wide shot, eye level, 35mm feel, locked camera; first frame of the shot, before the action starts; the flickering tube at the far end; the flickering tube behind him; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-6s). Locked camera. He walks toward camera along the chairs and stops in front of a closed door at frame right, standing still. Background: the flickering tube at the far end.
Ends on: he walks toward camera along the chairs and stops in front of a closed door at frame right, standing still.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 02 · 4s · không mặt người

*Không tạo AI* — a phone screen with a Vietnamese text message. Làm bằng đạo cụ thật hoặc đồ họa khi dựng.

#### 03 · 4s · MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hanhlang` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a long provincial hospital corridor at dawn, pale green walls, scuffed grey floor tiles, a row of joined plastic chairs along the left wall, a window at the far end; flat cold fluorescent light from ceiling tubes, one tube flickering at the far end, grey dawn light from the end window
Subject: MINH looks down at a phone held low in both hands, thumbs over the keyboard. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: close-up, eye level, 85mm feel, locked camera; first frame of the shot, before the action starts; the flickering tube at the far end; the phone glow on his chin; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-4s). Locked camera. His thumbs type a short reply, he exhales through his nose and lowers the phone to his thigh. Background: the flickering tube at the far end.
Ends on: his thumbs type a short reply, he exhales through his nose and lowers the phone to his thigh.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 04 · 6s · NHUNG, MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hanhlang` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a long provincial hospital corridor at dawn, pale green walls, scuffed grey floor tiles, a row of joined plastic chairs along the left wall, a window at the far end; flat cold fluorescent light from ceiling tubes, one tube flickering at the far end, grey dawn light from the end window
Subject: a closed emergency-room door; MINH's shoulder blurred at frame left. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium shot, eye level, 50mm feel, locked camera; first frame of the shot, before the action starts; the flickering tube at the far end; the medical file pressed to her chest; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: NHUNG, as in the image]
[Character B: MINH, as in the image]
Shot (0-6s). Locked camera. The door opens, NHUNG steps out holding a paper medical file against her chest, sees him and stops dead, standing still. Background: the flickering tube at the far end.
Ends on: the door opens, NHUNG steps out holding a paper medical file against her chest, sees him and stops dead, standing still.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 05 · 5s · NHUNG, MINH

Thoại (thu riêng): **Nhung:** Mày về rồi. / **Minh:** Mẹ sao rồi chị? / **Nhung:** Đột quỵ nhẹ. Bác sĩ nói qua giai đoạn nguy hiểm rồi.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hanhlang` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a long provincial hospital corridor at dawn, pale green walls, scuffed grey floor tiles, a row of joined plastic chairs along the left wall, a window at the far end; flat cold fluorescent light from ceiling tubes, one tube flickering at the far end, grey dawn light from the end window
Subject: NHUNG faces camera, MINH's out-of-focus shoulder at frame left. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium close-up on NHUNG over MINH's shoulder, 50mm feel, locked camera; first frame of the shot, before the action starts; the flickering tube at the far end; her thumb pressing into the file's edge; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: NHUNG, as in the image]
[Character B: MINH, as in the image]
Shot (0-5s). Locked camera. She speaks briefly, jaw tight, eyes not leaving his face; falls silent. Lips move with quiet speech. Background: the flickering tube at the far end.
Ends on: NHUNG silent, lips pressed flat, the file held tight against her chest.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 06 · 5s · MINH, NHUNG

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hanhlang` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose
Scene: a long provincial hospital corridor at dawn, pale green walls, scuffed grey floor tiles, a row of joined plastic chairs along the left wall, a window at the far end; flat cold fluorescent light from ceiling tubes, one tube flickering at the far end, grey dawn light from the end window
Subject: MINH faces camera, NHUNG's ponytail blurred at frame right. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow.
Important Details: medium close-up on MINH over NHUNG's shoulder, 50mm feel, locked camera; first frame of the shot, before the action starts; the flickering tube at the far end; the duffel strap twisting in his hand; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
[Character B: NHUNG, as in the image]
Shot (0-5s). Locked camera. He listens, swallows once, gives a small nod and does not speak. Background: the flickering tube at the far end.
Ends on: he listens, swallows once, gives a small nod and does not speak.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 07 · 9s · NHUNG, MINH

Thoại (thu riêng): **Nhung:** Vào đi. Bà hỏi mày từ tối qua.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hanhlang` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a long provincial hospital corridor at dawn, pale green walls, scuffed grey floor tiles, a row of joined plastic chairs along the left wall, a window at the far end; flat cold fluorescent light from ceiling tubes, one tube flickering at the far end, grey dawn light from the end window
Subject: NHUNG stands by the open door facing MINH. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium two-shot, eye level, 35mm feel, locked camera; first frame of the shot, before the action starts; the flickering tube at the far end; the door swinging slowly shut behind him; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: NHUNG, as in the image]
[Character B: MINH, as in the image]
Shot (0-9s). Locked camera. She speaks one line and steps aside; he walks past her through the door and out of frame; she stays, looking down the corridor. Lips move with quiet speech. Background: the flickering tube at the far end.
Ends on: she stays, looking down the corridor.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

### Cảnh 2 · Phòng bệnh (cảnh 08–19)

Năm điểm neo — cảm xúc: thương mà không nói · mô-típ: ống thở mờ hơi · đồ vật: tay Mẹ chạm tay Minh · điểm vỡ: Mẹ gọi Trang lại gần · hình cuối: giường Mẹ và ghế trống

#### 08 · 6s · BÀ THU, YẾN, TRANG, MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_phong` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of BÀ THU — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of YẾN — use only face, hair and clothing; ignore its background and pose; Image 4: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose; Image 5: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a four-bed provincial hospital ward, three beds empty with folded grey blankets, metal bed rails, a dusty window on the left, an IV stand; grey overcast morning light from the left window, weak fluorescent fill from above
Subject: BÀ THU lies on her side in the only occupied bed; YẾN sits on a plastic chair beside it holding prayer beads; TRANG stands at the window with her back to the room. BÀ THU, 58, a small Vietnamese woman with a round face, high cheekbones, deep-set double-lidded eyes with heavy crow's feet, a flat brown mole on her right cheekbone, salt-and-pepper hair in a low bun, in a faded light-brown cotton collarless blouse with cloth knot buttons. YẾN, 34, a slender Vietnamese woman with an oval face, large slightly downturned eyes, a small rounded nose, a beauty mark just below her left eye, long black hair to mid-back gathered by a brown claw clip, in a pale pink cotton t-shirt with a stretched neckline. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: wide shot, slightly above eye level, 35mm feel, locked camera; first frame of the shot, before the action starts; an IV drip falling slowly in its chamber; prayer beads sliding through YẾN's fingers; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 4 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: BÀ THU, as in the image]
[Character B: YẾN, as in the image]
[Character C: TRANG, as in the image]
[Character D: MINH, as in the image]
Shot (0-6s). Locked camera. MINH steps in from frame left and stops at the foot of the bed; no one else moves. Background: an IV drip falling slowly in its chamber.
Ends on: MINH standing at the foot of the bed, the three women unchanged.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 09 · 4s · BÀ THU

Thoại (thu riêng): **Bà Thu:** Minh.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_phong` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of BÀ THU — use only face, hair and clothing; ignore its background and pose
Scene: a four-bed provincial hospital ward, three beds empty with folded grey blankets, metal bed rails, a dusty window on the left, an IV stand; grey overcast morning light from the left window, weak fluorescent fill from above
Subject: BÀ THU's face on the pillow, eyes closed, a thin clear oxygen cannula under her nose. BÀ THU, 58, a small Vietnamese woman with a round face, high cheekbones, deep-set double-lidded eyes with heavy crow's feet, a flat brown mole on her right cheekbone, salt-and-pepper hair in a low bun, in a faded light-brown cotton collarless blouse with cloth knot buttons.
Important Details: close-up at pillow height, 85mm feel, locked camera; first frame of the shot, before the action starts; an IV drip falling slowly in its chamber; the oxygen cannula fogging faintly; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: BÀ THU, as in the image]
Shot (0-4s). Locked camera. Her eyes open slowly and her lips shape one word. Lips move with quiet speech. Background: an IV drip falling slowly in its chamber.
Ends on: her eyes open slowly and her lips shape one word.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 10 · 6s · MINH, BÀ THU

Thoại (thu riêng): **Minh:** Mẹ, con về rồi.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_phong` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of BÀ THU — use only face, hair and clothing; ignore its background and pose
Scene: a four-bed provincial hospital ward, three beds empty with folded grey blankets, metal bed rails, a dusty window on the left, an IV stand; grey overcast morning light from the left window, weak fluorescent fill from above
Subject: MINH stands beside the bed holding his duffel. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button. BÀ THU, 58, a small Vietnamese woman with a round face, high cheekbones, deep-set double-lidded eyes with heavy crow's feet, a flat brown mole on her right cheekbone, salt-and-pepper hair in a low bun, in a faded light-brown cotton collarless blouse with cloth knot buttons.
Important Details: medium shot, eye level, 50mm feel, locked camera; first frame of the shot, before the action starts; an IV drip falling slowly in its chamber; the bed rail cold under his hand; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
[Character B: BÀ THU, as in the image]
Shot (0-6s). Locked camera. He sets the bag on the floor and bends over the bed until his face is level with hers; holds still. Lips move with quiet speech. Background: an IV drip falling slowly in its chamber.
Ends on: MINH bent over the bed, his face level with hers, both still.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 11 · 3s · không mặt người

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_phong` — use for the room, perspective, light direction and colour; ignore any people in it
Scene: a four-bed provincial hospital ward, three beds empty with folded grey blankets, metal bed rails, a dusty window on the left, an IV stand; grey overcast morning light from the left window, weak fluorescent fill from above
Subject: an old woman's hand with age spots resting on a grey blanket beside a young man's hand on the bed rail
Important Details: extreme close-up on two hands, 85mm feel, locked camera; first frame of the shot, before the action starts; an IV drip falling slowly in its chamber; the hospital ID band on her wrist; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: no faces visible; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
Shot (0-3s). Locked camera. Her fingertips lift and come to rest on the back of his hand and stay still. Background: an IV drip falling slowly in its chamber.
Ends on: her fingertips lift and come to rest on the back of his hand and stay still.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 12 · 4s · BÀ THU

Thoại (thu riêng): **Bà Thu:** Con gầy quá.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_phong` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of BÀ THU — use only face, hair and clothing; ignore its background and pose
Scene: a four-bed provincial hospital ward, three beds empty with folded grey blankets, metal bed rails, a dusty window on the left, an IV stand; grey overcast morning light from the left window, weak fluorescent fill from above
Subject: BÀ THU looks up at MINH from the pillow. BÀ THU, 58, a small Vietnamese woman with a round face, high cheekbones, deep-set double-lidded eyes with heavy crow's feet, a flat brown mole on her right cheekbone, salt-and-pepper hair in a low bun, in a faded light-brown cotton collarless blouse with cloth knot buttons.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; an IV drip falling slowly in its chamber; the oxygen cannula; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: BÀ THU, as in the image]
Shot (0-4s). Locked camera. She speaks softly, the corners of her eyes creasing. Lips move with quiet speech. Background: an IV drip falling slowly in its chamber.
Ends on: BÀ THU looking up at him, a faint smile, eyes creased.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 13 · 5s · MINH

Thoại (thu riêng): **Minh:** Con ăn đủ mà mẹ. / **Bà Thu:** Ăn đủ không có nghĩa là ăn ngon.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_phong` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a four-bed provincial hospital ward, three beds empty with folded grey blankets, metal bed rails, a dusty window on the left, an IV stand; grey overcast morning light from the left window, weak fluorescent fill from above
Subject: MINH bent close, looking down. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; an IV drip falling slowly in its chamber; the scar in his left eyebrow catching the window light; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-5s). Locked camera. A small closed-mouth smile, he answers quietly. Lips move with quiet speech. Background: an IV drip falling slowly in its chamber.
Ends on: MINH's small smile fading as he keeps looking at her.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 14 · 6s · YẾN, TRANG

Thoại (thu riêng): **Yến:** Mẹ đấy. Bệnh nằm viện vẫn còn lo chuyện ăn uống.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_phong` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of YẾN — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: a four-bed provincial hospital ward, three beds empty with folded grey blankets, metal bed rails, a dusty window on the left, an IV stand; grey overcast morning light from the left window, weak fluorescent fill from above
Subject: YẾN on the plastic chair, prayer beads in her lap; TRANG's back at the window behind her. YẾN, 34, a slender Vietnamese woman with an oval face, large slightly downturned eyes, a small rounded nose, a beauty mark just below her left eye, long black hair to mid-back gathered by a brown claw clip, in a pale pink cotton t-shirt with a stretched neckline. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: medium shot on YẾN, TRANG soft in background, 50mm feel, locked camera; first frame of the shot, before the action starts; an IV drip falling slowly in its chamber; prayer beads; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: YẾN, as in the image]
[Character B: TRANG, as in the image]
Shot (0-6s). Locked camera. YẾN laughs once and wipes her eyes with the back of her wrist; the woman at the window does not move. Lips move with quiet speech. Background: an IV drip falling slowly in its chamber.
Ends on: YẾN with her wrist against her cheek, TRANG's back still turned.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 15 · 4s · BÀ THU

Thoại (thu riêng): **Bà Thu:** Trang. Con đứng đó làm gì, lại đây.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_phong` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of BÀ THU — use only face, hair and clothing; ignore its background and pose
Scene: a four-bed provincial hospital ward, three beds empty with folded grey blankets, metal bed rails, a dusty window on the left, an IV stand; grey overcast morning light from the left window, weak fluorescent fill from above
Subject: BÀ THU turns her eyes toward the window. BÀ THU, 58, a small Vietnamese woman with a round face, high cheekbones, deep-set double-lidded eyes with heavy crow's feet, a flat brown mole on her right cheekbone, salt-and-pepper hair in a low bun, in a faded light-brown cotton collarless blouse with cloth knot buttons.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; an IV drip falling slowly in its chamber; the oxygen cannula; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: BÀ THU, as in the image]
Shot (0-4s). Locked camera. She calls out, voice thin. Lips move with quiet speech. Background: an IV drip falling slowly in its chamber.
Ends on: BÀ THU's eyes fixed on the window, waiting.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 16 · 6s · TRANG, MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_phong` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a four-bed provincial hospital ward, three beds empty with folded grey blankets, metal bed rails, a dusty window on the left, an IV stand; grey overcast morning light from the left window, weak fluorescent fill from above
Subject: TRANG at the window, back turned. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium shot, eye level, 35mm feel, locked camera; first frame of the shot, before the action starts; an IV drip falling slowly in its chamber; her hands knotted in her apron; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
[Character B: MINH, as in the image]
Shot (0-6s). Locked camera. She turns, walks to the bed and stops one step from MINH, looking at the bed, not at him. Background: an IV drip falling slowly in its chamber.
Ends on: she turns, walks to the bed and stops one step from MINH, looking at the bed, not at him.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 17 · 6s · MINH, TRANG

Thoại (thu riêng): **Bà Thu:** Hai đứa làm lành đi. Mẹ không muốn nhìn cảnh này thêm nữa.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_phong` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: a four-bed provincial hospital ward, three beds empty with folded grey blankets, metal bed rails, a dusty window on the left, an IV stand; grey overcast morning light from the left window, weak fluorescent fill from above
Subject: MINH and TRANG side by side beside the bed, looking in different directions. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: medium close-up two-shot, 50mm feel, locked camera; first frame of the shot, before the action starts; an IV drip falling slowly in its chamber; the IV drip; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
[Character B: TRANG, as in the image]
Shot (0-6s). Locked camera. Neither moves; only breathing; TRANG's jaw tightens once. Lips move with quiet speech. Background: an IV drip falling slowly in its chamber.
Ends on: the two of them side by side, TRANG's jaw set, neither looking at the other.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 18 · 6s · BÀ THU

Thoại (thu riêng): **Bà Thu:** Mẹ mệt rồi. Đi ra ngoài đi, để mẹ ngủ.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_phong` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of BÀ THU — use only face, hair and clothing; ignore its background and pose
Scene: a four-bed provincial hospital ward, three beds empty with folded grey blankets, metal bed rails, a dusty window on the left, an IV stand; grey overcast morning light from the left window, weak fluorescent fill from above
Subject: BÀ THU on the pillow, eyes half open. BÀ THU, 58, a small Vietnamese woman with a round face, high cheekbones, deep-set double-lidded eyes with heavy crow's feet, a flat brown mole on her right cheekbone, salt-and-pepper hair in a low bun, in a faded light-brown cotton collarless blouse with cloth knot buttons.
Important Details: close-up, slow push-in to extreme close-up, 85mm feel; first frame of the shot, before the action starts; an IV drip falling slowly in its chamber; her breath fogging the cannula; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: BÀ THU, as in the image]
Shot (0-6s). Slow push-in. She closes her eyes; nothing else moves. Lips move with quiet speech. Background: an IV drip falling slowly in its chamber.
Ends on: an extreme close-up of BÀ THU's closed eyes and the cannula.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 19 · 4s · BÀ THU

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_phong` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of BÀ THU — use only face, hair and clothing; ignore its background and pose
Scene: a four-bed provincial hospital ward, three beds empty with folded grey blankets, metal bed rails, a dusty window on the left, an IV stand; grey overcast morning light from the left window, weak fluorescent fill from above
Subject: the ward seen from the door, BÀ THU asleep in the only occupied bed, an empty plastic chair. BÀ THU, 58, a small Vietnamese woman with a round face, high cheekbones, deep-set double-lidded eyes with heavy crow's feet, a flat brown mole on her right cheekbone, salt-and-pepper hair in a low bun, in a faded light-brown cotton collarless blouse with cloth knot buttons.
Important Details: wide shot from the doorway, 35mm feel, locked camera; first frame of the shot, before the action starts; an IV drip falling slowly in its chamber; the empty plastic chair; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: BÀ THU, as in the image]
Shot (0-4s). Locked camera. The last of three shadows slides off the floor as footsteps leave; the room is still. Background: an IV drip falling slowly in its chamber.
Ends on: the sleeping mother and the empty chair, no one in the doorway.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

### Cảnh 3 · Mái hiên, mưa (cảnh 20–33)

Năm điểm neo — cảm xúc: giận dồn nén · mô-típ: màn mưa · đồ vật: điện thoại của Yến · điểm vỡ: Nhung: 'mỗi lần về là một lần khách' · hình cuối: Yến cụp mắt nhìn sân mưa

#### 20 · 7s · TRANG, NHUNG, YẾN, MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose; Image 4: locked portrait of YẾN — use only face, hair and clothing; ignore its background and pose; Image 5: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: four siblings stand in a row under the roof edge, left to right TRANG, NHUNG, YẾN, MINH, each looking a different way. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow. YẾN, 34, a slender Vietnamese woman with an oval face, large slightly downturned eyes, a small rounded nose, a beauty mark just below her left eye, long black hair to mid-back gathered by a brown claw clip, in a pale pink cotton t-shirt with a stretched neckline. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: wide shot from the courtyard through the rain, eye level, 35mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; the sheet of rain off the roof edge; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 4 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
[Character B: NHUNG, as in the image]
[Character C: YẾN, as in the image]
[Character D: MINH, as in the image]
Shot (0-7s). Locked camera. No one moves; rain pours between camera and them. Background: water pouring off the roof edge in a steady sheet.
Ends on: four still figures behind the falling rain.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 21 · 4s · NHUNG

Thoại (thu riêng): **Nhung:** Mẹ muốn về nhà.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: NHUNG, arms crossed over the file. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; rain behind her; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: NHUNG, as in the image]
Shot (0-4s). Locked camera. She speaks without looking at anyone. Lips move with quiet speech. Background: water pouring off the roof edge in a steady sheet.
Ends on: NHUNG looking out at the rain, arms crossed.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 22 · 5s · YẾN

Thoại (thu riêng): **Yến:** Chị nói bác sĩ rồi, không được đi xa.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of YẾN — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: YẾN, shoulders hunched. YẾN, 34, a slender Vietnamese woman with an oval face, large slightly downturned eyes, a small rounded nose, a beauty mark just below her left eye, long black hair to mid-back gathered by a brown claw clip, in a pale pink cotton t-shirt with a stretched neckline.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; rain behind her; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: YẾN, as in the image]
Shot (0-5s). Locked camera. She objects quietly, eyes on the ground. Lips move with quiet speech. Background: water pouring off the roof edge in a steady sheet.
Ends on: YẾN's eyes on the wet ground.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 23 · 4s · TRANG

Thoại (thu riêng): **Trang:** Ai trả tiền điều dưỡng?

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: TRANG, hands in apron pocket. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; rain behind her; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
Shot (0-4s). Locked camera. She asks flatly. Lips move with quiet speech. Background: water pouring off the roof edge in a steady sheet.
Ends on: TRANG looking straight ahead, waiting for an answer.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 24 · 4s · MINH

Thoại (thu riêng): **Minh:** Để em lo.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: MINH looking at the rain. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; rain behind him; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-4s). Locked camera. He turns his head toward his sisters and speaks. Lips move with quiet speech. Background: water pouring off the roof edge in a steady sheet.
Ends on: MINH facing his sisters, mouth closed.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 25 · 6s · NHUNG, MINH

Thoại (thu riêng): **Nhung:** Mày lo bằng gì? Tiền lương kỹ sư âm thanh à?

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: NHUNG half-turned away. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium shot on NHUNG over MINH's shoulder, 50mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; her ponytail swinging as she turns; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: NHUNG, as in the image]
[Character B: MINH, as in the image]
Shot (0-6s). Locked camera. She turns fully to face MINH and speaks, chin lifted. Lips move with quiet speech. Background: water pouring off the roof edge in a steady sheet.
Ends on: she turns fully to face MINH and speaks, chin lifted.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 26 · 4s · MINH, NHUNG

Thoại (thu riêng): **Minh:** Chị đừng nói như vậy.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: MINH facing NHUNG. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow.
Important Details: medium close-up on MINH over NHUNG's shoulder, 50mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; the duffel strap; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
[Character B: NHUNG, as in the image]
Shot (0-4s). Locked camera. His hand tightens on the duffel strap; he answers low. Lips move with quiet speech. Background: water pouring off the roof edge in a steady sheet.
Ends on: MINH's knuckles white on the duffel strap.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 27 · 6s · NHUNG

Thoại (thu riêng): **Nhung:** Tao nói sự thật. Mày đi bao năm, mỗi lần về là một lần khách.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: NHUNG facing MINH. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; rain behind her; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: NHUNG, as in the image]
Shot (0-6s). Locked camera. She speaks steadily, eyes wet but not blinking. Lips move with quiet speech. Background: water pouring off the roof edge in a steady sheet.
Ends on: NHUNG holding his gaze, eyes wet, not blinking.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 28 · 5s · TRANG, NHUNG, MINH

Thoại (thu riêng): **Trang:** Thôi, đừng cãi nhau ở đây. Ai cũng mệt rồi.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose; Image 4: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: NHUNG and MINH facing each other, TRANG at frame left. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium three-shot, 35mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; rain behind them; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 3 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
[Character B: NHUNG, as in the image]
[Character C: MINH, as in the image]
Shot (0-5s). Locked camera. TRANG takes one step forward between them and stops. Lips move with quiet speech. Background: water pouring off the roof edge in a steady sheet.
Ends on: TRANG takes one step forward between them and stops.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 29 · 6s · YẾN

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of YẾN — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: YẾN at the group's edge, a phone buzzing in her hand. YẾN, 34, a slender Vietnamese woman with an oval face, large slightly downturned eyes, a small rounded nose, a beauty mark just below her left eye, long black hair to mid-back gathered by a brown claw clip, in a pale pink cotton t-shirt with a stretched neckline.
Important Details: medium shot, 50mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; the phone buzzing; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: YẾN, as in the image]
Shot (0-6s). Locked camera. She looks at the screen, turns and walks a few steps away, stopping with her back to the group. Background: water pouring off the roof edge in a steady sheet.
Ends on: she looks at the screen, turns and walks a few steps away, stopping with her back to the group.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 30 · 6s · YẾN

Thoại (thu riêng): **Yến:** Dạ, anh Hai. Mẹ qua cơn rồi. Dạ… em biết. Anh đừng nói với ba vội.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of YẾN — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: YẾN with the phone at her ear, rain beyond. YẾN, 34, a slender Vietnamese woman with an oval face, large slightly downturned eyes, a small rounded nose, a beauty mark just below her left eye, long black hair to mid-back gathered by a brown claw clip, in a pale pink cotton t-shirt with a stretched neckline.
Important Details: close-up in profile, 85mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; rain drowning her words; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: YẾN, as in the image]
Shot (0-6s). Locked camera. She speaks very quietly, eyes closed for a moment. Lips move with quiet speech. Background: water pouring off the roof edge in a steady sheet.
Ends on: YẾN with the phone still at her ear, eyes closed.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 31 · 5s · YẾN, NHUNG

Thoại (thu riêng): **Nhung:** Ai gọi? / **Yến:** Bạn em. Hỏi thăm mẹ.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of YẾN — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: YẾN walking back toward NHUNG. YẾN, 34, a slender Vietnamese woman with an oval face, large slightly downturned eyes, a small rounded nose, a beauty mark just below her left eye, long black hair to mid-back gathered by a brown claw clip, in a pale pink cotton t-shirt with a stretched neckline. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow.
Important Details: medium two-shot, 50mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; the phone pushed into her pocket; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: YẾN, as in the image]
[Character B: NHUNG, as in the image]
Shot (0-5s). Locked camera. She stops beside NHUNG; NHUNG asks, YẾN answers without looking up. Lips move with quiet speech. Background: water pouring off the roof edge in a steady sheet.
Ends on: YẾN looking down beside NHUNG, the phone gone into her pocket.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 32 · 4s · NHUNG

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: NHUNG staring at YẾN. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; rain behind her; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: NHUNG, as in the image]
Shot (0-4s). Locked camera. She does not blink; a muscle moves in her jaw. Background: water pouring off the roof edge in a steady sheet.
Ends on: a muscle moves in her jaw.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 33 · 3s · YẾN

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `bv_hien` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of YẾN — use only face, hair and clothing; ignore its background and pose
Scene: a covered concrete veranda of a provincial hospital, a tin roof edge, a courtyard beyond with a frangipani tree; soft grey daylight from the courtyard in front of the subjects, a curtain of heavy rain pouring off the roof edge
Subject: YẾN facing NHUNG. YẾN, 34, a slender Vietnamese woman with an oval face, large slightly downturned eyes, a small rounded nose, a beauty mark just below her left eye, long black hair to mid-back gathered by a brown claw clip, in a pale pink cotton t-shirt with a stretched neckline.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; water pouring off the roof edge in a steady sheet; rain; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: YẾN, as in the image]
Shot (0-3s). Locked camera. Her eyes drop to the wet courtyard and stay there. Background: water pouring off the roof edge in a steady sheet.
Ends on: her eyes drop to the wet courtyard and stay there.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

### Cảnh 3b · Trường gà (cảnh 34–47)

Năm điểm neo — cảm xúc: tội lỗi · mô-típ: bóng đèn tròn đung đưa · đồ vật: xấp giấy tên khách · điểm vỡ: cuộc gọi từ Tài · hình cuối: đèn hậu xe tải đi ngược hướng bệnh viện

#### 34 · 6s · không mặt người

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `truongga` — use for the room, perspective, light direction and colour; ignore any people in it
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge; a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke
Subject: the blue tarp structure behind the palm grove at dusk, bulbs glowing, a crowd seen only from behind, no animals visible
Important Details: extreme wide shot, high angle from a palm crown, 35mm feel, locked camera; first frame of the shot, before the action starts; bare bulbs swinging slightly on their wire; bare bulbs swinging; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: no faces visible; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
Shot (0-6s). Locked camera. Smoke drifts slowly up through the bulbs; the crowd sways. Background: bare bulbs swinging slightly on their wire.
Ends on: smoke hanging among the bulbs above the crowd.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 35 · 4s · không mặt người

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `truongga` — use for the room, perspective, light direction and colour; ignore any people in it
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge; a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke
Subject: raised hands gripping folded paper money above the backs of heads
Important Details: medium shot on hands, 50mm feel, locked camera; first frame of the shot, before the action starts; bare bulbs swinging slightly on their wire; money in raised fists; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: no faces visible; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
Shot (0-4s). Locked camera. Hands wave and slap betting slips; no faces. Background: bare bulbs swinging slightly on their wire.
Ends on: a raised fist of crumpled money held still above the heads.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 36 · 5s · ÔNG HẢI

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `truongga` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of ÔNG HẢI — use only face, hair and clothing; ignore its background and pose
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge; a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke
Subject: ÔNG HẢI stands at the edge of the crowd beside his small truck, not watching the ring. ÔNG HẢI, 62, a thin Vietnamese man with a long face, hollow cheeks, deep-set tired eyes, grey stubble on a narrow jaw, a dark liver spot on his left temple, very short almost-white hair, in a faded blue-and-brown checked short-sleeve shirt worn untucked with a frayed collar.
Important Details: medium shot, eye level, 50mm feel, locked camera; first frame of the shot, before the action starts; bare bulbs swinging slightly on their wire; a cheap steel wristwatch; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: ÔNG HẢI, as in the image]
Shot (0-5s). Locked camera. He lifts his wrist, checks his watch, lowers it. Background: bare bulbs swinging slightly on their wire.
Ends on: he lifts his wrist, checks his watch, lowers it.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 37 · 4s · THẮNG, ÔNG HẢI

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `truongga` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of THẮNG — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of ÔNG HẢI — use only face, hair and clothing; ignore its background and pose
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge; a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke
Subject: ÔNG HẢI by the truck. THẮNG, 30, a tall lean Vietnamese man with a long face, restless narrow eyes, a thin pale scar across the bridge of his nose, gelled black hair spiked at the front, in a black cotton t-shirt under a thick gold rope chain. ÔNG HẢI, 62, a thin Vietnamese man with a long face, hollow cheeks, deep-set tired eyes, grey stubble on a narrow jaw, a dark liver spot on his left temple, very short almost-white hair, in a faded blue-and-brown checked short-sleeve shirt worn untucked with a frayed collar.
Important Details: medium two-shot, 50mm feel, locked camera; first frame of the shot, before the action starts; bare bulbs swinging slightly on their wire; the gold chain swinging; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: THẮNG, as in the image]
[Character B: ÔNG HẢI, as in the image]
Shot (0-4s). Locked camera. THẮNG walks into frame and holds out a folded stack of paper; it is offered, not yet taken. Background: bare bulbs swinging slightly on their wire.
Ends on: the folded paper held out between them, not yet taken.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 38 · 3s · không mặt người

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `truongga` — use for the room, perspective, light direction and colour; ignore any people in it
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge; a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke
Subject: a young man's hand pressing a folded stack of paper toward an older man's calloused hand
Important Details: extreme close-up on hands, 85mm feel, locked camera; first frame of the shot, before the action starts; bare bulbs swinging slightly on their wire; the stack of paper; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: no faces visible; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
Shot (0-3s). Locked camera. The paper is pushed into the older hand, which closes around it. Background: bare bulbs swinging slightly on their wire.
Ends on: the paper is pushed into the older hand, which closes around it.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 39 · 5s · THẮNG

Thoại (thu riêng): **Thắng:** Chú Hải. Tối nay chở mấy ông này về thị xã. Anh Sáu dặn đi đường trong, đừng đi quốc lộ.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `truongga` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of THẮNG — use only face, hair and clothing; ignore its background and pose
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge; a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke
Subject: THẮNG chewing gum. THẮNG, 30, a tall lean Vietnamese man with a long face, restless narrow eyes, a thin pale scar across the bridge of his nose, gelled black hair spiked at the front, in a black cotton t-shirt under a thick gold rope chain.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; bare bulbs swinging slightly on their wire; bulbs behind him; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: THẮNG, as in the image]
Shot (0-5s). Locked camera. He speaks casually, eyes flicking to the crowd. Lips move with quiet speech. Background: bare bulbs swinging slightly on their wire.
Ends on: THẮNG chewing, looking past the old man at the crowd.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 40 · 3s · ÔNG HẢI

Thoại (thu riêng): **Ông Hải:** Tối nay tôi bận.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `truongga` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of ÔNG HẢI — use only face, hair and clothing; ignore its background and pose
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge; a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke
Subject: ÔNG HẢI holding the paper. ÔNG HẢI, 62, a thin Vietnamese man with a long face, hollow cheeks, deep-set tired eyes, grey stubble on a narrow jaw, a dark liver spot on his left temple, very short almost-white hair, in a faded blue-and-brown checked short-sleeve shirt worn untucked with a frayed collar.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; bare bulbs swinging slightly on their wire; smoke; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: ÔNG HẢI, as in the image]
Shot (0-3s). Locked camera. He answers without looking up. Lips move with quiet speech. Background: bare bulbs swinging slightly on their wire.
Ends on: ÔNG HẢI looking down at the paper in his hand.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 41 · 5s · THẮNG

Thoại (thu riêng): **Thắng:** Chú bận gì? Thằng Tư nhà chú còn nợ bên này hai trăm. Chú không chạy thì ai trả?

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `truongga` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of THẮNG — use only face, hair and clothing; ignore its background and pose
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge; a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke
Subject: THẮNG. THẮNG, 30, a tall lean Vietnamese man with a long face, restless narrow eyes, a thin pale scar across the bridge of his nose, gelled black hair spiked at the front, in a black cotton t-shirt under a thick gold rope chain.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; bare bulbs swinging slightly on their wire; the gold chain; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: THẮNG, as in the image]
Shot (0-5s). Locked camera. He grins and leans in, lowering his voice. Lips move with quiet speech. Background: bare bulbs swinging slightly on their wire.
Ends on: THẮNG leaning close, grinning.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 42 · 3s · không mặt người

*Không tạo AI* — a phone screen showing an incoming call named Tài. Làm bằng đạo cụ thật hoặc đồ họa khi dựng.

#### 43 · 8s · ÔNG HẢI

Thoại (thu riêng): **Ông Hải:** Gì? / **Ông Hải:** Nằm viện nào? … Ừ. Ừ. Thôi, ba biết rồi.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `truongga` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of ÔNG HẢI — use only face, hair and clothing; ignore its background and pose
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge; a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke
Subject: ÔNG HẢI with a cheap phone at his ear. ÔNG HẢI, 62, a thin Vietnamese man with a long face, hollow cheeks, deep-set tired eyes, grey stubble on a narrow jaw, a dark liver spot on his left temple, very short almost-white hair, in a faded blue-and-brown checked short-sleeve shirt worn untucked with a frayed collar.
Important Details: medium close-up, slow push-in, 85mm feel; first frame of the shot, before the action starts; bare bulbs swinging slightly on their wire; the roar of the crowd swelling behind him; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: ÔNG HẢI, as in the image]
Shot (0-8s). Slow push-in. He listens; his face drains; he turns his back to the crowd and speaks quietly. Lips move with quiet speech. Background: bare bulbs swinging slightly on their wire.
Ends on: ÔNG HẢI with his back to the crowd, phone at his ear, head bowed.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 44 · 5s · ÔNG HẢI

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `truongga` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of ÔNG HẢI — use only face, hair and clothing; ignore its background and pose
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge; a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke
Subject: ÔNG HẢI lowering the phone. ÔNG HẢI, 62, a thin Vietnamese man with a long face, hollow cheeks, deep-set tired eyes, grey stubble on a narrow jaw, a dark liver spot on his left temple, very short almost-white hair, in a faded blue-and-brown checked short-sleeve shirt worn untucked with a frayed collar.
Important Details: medium shot, 50mm feel, locked camera; first frame of the shot, before the action starts; bare bulbs swinging slightly on their wire; the dirt road; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: ÔNG HẢI, as in the image]
Shot (0-5s). Locked camera. He hangs up and looks out along the dirt road toward the highway, motionless. Background: bare bulbs swinging slightly on their wire.
Ends on: he hangs up and looks out along the dirt road toward the highway, motionless.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 45 · 4s · không mặt người

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `truongga` — use for the room, perspective, light direction and colour; ignore any people in it
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge; a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke
Subject: an empty dirt road between palms leading out to a highway in the blue dusk
Important Details: wide point-of-view shot, 35mm feel, locked camera; first frame of the shot, before the action starts; bare bulbs swinging slightly on their wire; the road; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: no faces visible; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
Shot (0-4s). Locked camera. Nothing moves but a moth around a bulb. Background: bare bulbs swinging slightly on their wire.
Ends on: nothing moves but a moth around a bulb.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 46 · 5s · ÔNG HẢI

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `truongga` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of ÔNG HẢI — use only face, hair and clothing; ignore its background and pose
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge; a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke
Subject: ÔNG HẢI beside the truck door, paper in hand. ÔNG HẢI, 62, a thin Vietnamese man with a long face, hollow cheeks, deep-set tired eyes, grey stubble on a narrow jaw, a dark liver spot on his left temple, very short almost-white hair, in a faded blue-and-brown checked short-sleeve shirt worn untucked with a frayed collar.
Important Details: medium shot, 35mm feel, locked camera; first frame of the shot, before the action starts; bare bulbs swinging slightly on their wire; the truck door; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: ÔNG HẢI, as in the image]
Shot (0-5s). Locked camera. He opens the door, climbs into the driver's seat and pulls the door shut. Background: bare bulbs swinging slightly on their wire.
Ends on: he opens the door, climbs into the driver's seat and pulls the door shut.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 47 · 6s · không mặt người

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `truongga` — use for the room, perspective, light direction and colour; ignore any people in it
Scene: an illegal open-air betting ground behind a coconut grove at dusk, a blue plastic tarp roof on bamboo poles, a packed crowd seen only from behind, a dirt clearing, a small dusty flatbed truck parked at the edge; a string of bare warm bulbs hanging from a wire under the tarp, deep blue dusk sky behind the palms, drifting cigarette smoke
Subject: the small truck at the dirt road junction
Important Details: wide shot, 35mm feel, locked camera; first frame of the shot, before the action starts; bare bulbs swinging slightly on their wire; red tail lights in the dusk; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: no faces visible; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
Shot (0-6s). Locked camera. The truck pulls out and turns away down the road, tail lights shrinking. Background: bare bulbs swinging slightly on their wire.
Ends on: the truck pulls out and turns away down the road, tail lights shrinking.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

### Cảnh 4 · Nhà cũ (cảnh 48–57)

Năm điểm neo — cảm xúc: hoài niệm · mô-típ: nước nhỏ từ lá chuối · đồ vật: ghế nhựa gãy chân · điểm vỡ: 'cái ghế đó là của anh' · hình cuối: cửa trống sau khi Trang vào

#### 48 · 7s · MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_san` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a narrow Mekong Delta lane leading to an old two-storey house with a tiled roof, a wooden gate with peeling green paint, a yard with banana plants, an old jackfruit tree, a pot of dried bougainvillea, two plastic chairs on the porch, one missing its back left leg; low late-afternoon sun after rain from camera right, wet leaves catching light, puddles on packed earth
Subject: MINH riding a motorbike into the narrow wet lane. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: wide shot, slow pan following, 35mm feel; first frame of the shot, before the action starts; water dripping from banana leaves; puddles splashing under the tyres; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-7s). Slow pan following the subject. He rides up the lane and stops in front of the wooden gate, engine off. Background: water dripping from banana leaves.
Ends on: he rides up the lane and stops in front of the wooden gate, engine off.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 49 · 4s · MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_san` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a narrow Mekong Delta lane leading to an old two-storey house with a tiled roof, a wooden gate with peeling green paint, a yard with banana plants, an old jackfruit tree, a pot of dried bougainvillea, two plastic chairs on the porch, one missing its back left leg; low late-afternoon sun after rain from camera right, wet leaves catching light, puddles on packed earth
Subject: MINH's hand on the peeling wooden gate. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium shot, 50mm feel, locked camera; first frame of the shot, before the action starts; water dripping from banana leaves; peeling green paint; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-4s). Locked camera. He pushes; the gate swings inward and stops half open. Background: water dripping from banana leaves.
Ends on: the gate swings inward and stops half open.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 50 · 7s · TRANG, MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_san` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a narrow Mekong Delta lane leading to an old two-storey house with a tiled roof, a wooden gate with peeling green paint, a yard with banana plants, an old jackfruit tree, a pot of dried bougainvillea, two plastic chairs on the porch, one missing its back left leg; low late-afternoon sun after rain from camera right, wet leaves catching light, puddles on packed earth
Subject: the yard after rain; TRANG sweeping leaves on the porch; MINH at the gate in the foreground; the broken plastic chair visible at frame right. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: wide shot, eye level, 35mm feel, locked camera; first frame of the shot, before the action starts; water dripping from banana leaves; water dripping from banana leaves; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
[Character B: MINH, as in the image]
Shot (0-7s). Locked camera. TRANG sweeps twice and stops. Background: water dripping from banana leaves.
Ends on: TRANG sweeps twice and stops.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 51 · 5s · TRANG

Thoại (thu riêng): **Trang:** Anh vào đi. Em để cơm trên bàn.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_san` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: a narrow Mekong Delta lane leading to an old two-storey house with a tiled roof, a wooden gate with peeling green paint, a yard with banana plants, an old jackfruit tree, a pot of dried bougainvillea, two plastic chairs on the porch, one missing its back left leg; low late-afternoon sun after rain from camera right, wet leaves catching light, puddles on packed earth
Subject: TRANG on the porch holding a straw broom. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: medium shot, 50mm feel, locked camera; first frame of the shot, before the action starts; water dripping from banana leaves; the broom; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
Shot (0-5s). Locked camera. She stops sweeping and speaks. Lips move with quiet speech. Background: water dripping from banana leaves.
Ends on: TRANG holding the broom still, looking at him.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 52 · 5s · MINH, TRANG

Thoại (thu riêng): **Minh:** Chị về lúc nào? / **Trang:** Hồi trưa. Đi xe đò.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_san` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: a narrow Mekong Delta lane leading to an old two-storey house with a tiled roof, a wooden gate with peeling green paint, a yard with banana plants, an old jackfruit tree, a pot of dried bougainvillea, two plastic chairs on the porch, one missing its back left leg; low late-afternoon sun after rain from camera right, wet leaves catching light, puddles on packed earth
Subject: MINH at the foot of the porch steps. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: medium close-up over the shoulder, 50mm feel, locked camera; first frame of the shot, before the action starts; water dripping from banana leaves; the broom; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
[Character B: TRANG, as in the image]
Shot (0-5s). Locked camera. A short exchange; TRANG barely looks at him. Lips move with quiet speech. Background: water dripping from banana leaves.
Ends on: TRANG turning back to the broom, MINH at the foot of the steps.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 53 · 6s · MINH

Thoại (thu riêng): **Minh:** Chị nấu à?

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_san` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a narrow Mekong Delta lane leading to an old two-storey house with a tiled roof, a wooden gate with peeling green paint, a yard with banana plants, an old jackfruit tree, a pot of dried bougainvillea, two plastic chairs on the porch, one missing its back left leg; low late-afternoon sun after rain from camera right, wet leaves catching light, puddles on packed earth
Subject: MINH climbing onto the porch. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium shot, 50mm feel, locked camera; first frame of the shot, before the action starts; water dripping from banana leaves; woodsmoke drifting from the kitchen; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-6s). Locked camera. He sets his bag down, breathes in the smell of woodsmoke and fish sauce, and stands still with eyes closed for a moment. Lips move with quiet speech. Background: water dripping from banana leaves.
Ends on: he sets his bag down, breathes in the smell of woodsmoke and fish sauce, and stands still with eyes closed for a moment.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 54 · 6s · TRANG

Thoại (thu riêng): **Trang:** Ừ. Mẹ dặn nấu cá kho tiêu, ai về cũng phải ăn.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_san` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: a narrow Mekong Delta lane leading to an old two-storey house with a tiled roof, a wooden gate with peeling green paint, a yard with banana plants, an old jackfruit tree, a pot of dried bougainvillea, two plastic chairs on the porch, one missing its back left leg; low late-afternoon sun after rain from camera right, wet leaves catching light, puddles on packed earth
Subject: TRANG at the door. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; water dripping from banana leaves; the open doorway; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
Shot (0-6s). Locked camera. She answers and carries the broom inside, out of frame. Lips move with quiet speech. Background: water dripping from banana leaves.
Ends on: she answers and carries the broom inside, out of frame.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 55 · 4s · không mặt người

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_san` — use for the room, perspective, light direction and colour; ignore any people in it
Scene: a narrow Mekong Delta lane leading to an old two-storey house with a tiled roof, a wooden gate with peeling green paint, a yard with banana plants, an old jackfruit tree, a pot of dried bougainvillea, two plastic chairs on the porch, one missing its back left leg; low late-afternoon sun after rain from camera right, wet leaves catching light, puddles on packed earth
Subject: an old plastic chair missing its back left leg, leaning against the porch wall
Important Details: close-up insert, 85mm feel, locked camera; first frame of the shot, before the action starts; water dripping from banana leaves; the broken chair; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: no faces visible; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
Shot (0-4s). Locked camera. A drop of water falls from the roof onto its seat. Background: water dripping from banana leaves.
Ends on: a drop of water falls from the roof onto its seat.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 56 · 3s · MINH

Thoại (thu riêng): **Minh:** Vẫn chưa sửa.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_san` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: a narrow Mekong Delta lane leading to an old two-storey house with a tiled roof, a wooden gate with peeling green paint, a yard with banana plants, an old jackfruit tree, a pot of dried bougainvillea, two plastic chairs on the porch, one missing its back left leg; low late-afternoon sun after rain from camera right, wet leaves catching light, puddles on packed earth
Subject: MINH looking down at the chair. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; water dripping from banana leaves; the broken chair; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-3s). Locked camera. He murmurs to himself. Lips move with quiet speech. Background: water dripping from banana leaves.
Ends on: MINH looking down at the broken chair.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 57 · 6s · TRANG

Thoại (thu riêng): **Trang:** Ai sửa? Anh đi từ hồi học cấp ba, cái ghế đó là của anh.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_san` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: a narrow Mekong Delta lane leading to an old two-storey house with a tiled roof, a wooden gate with peeling green paint, a yard with banana plants, an old jackfruit tree, a pot of dried bougainvillea, two plastic chairs on the porch, one missing its back left leg; low late-afternoon sun after rain from camera right, wet leaves catching light, puddles on packed earth
Subject: TRANG leaning out of the doorway. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: medium shot, 50mm feel, locked camera; first frame of the shot, before the action starts; water dripping from banana leaves; the doorway; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
Shot (0-6s). Locked camera. She says it plainly and disappears back inside. Lips move with quiet speech. Background: water dripping from banana leaves.
Ends on: the empty doorway.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

### Cảnh 5 · Bữa cơm đầu tiên (cảnh 58–74)

Năm điểm neo — cảm xúc: vết thương cũ · mô-típ: tiếng đồng hồ · đồ vật: chén cơm để trống · điểm vỡ: Nhung đặt đũa xuống · hình cuối: Minh nhìn lên cầu thang tối

#### 58 · 8s · NHUNG, MINH, TRANG

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose; Image 4: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: NHUNG at the far head of the table, MINH at left, TRANG at right, an empty bowl nearest camera, the wall clock behind NHUNG. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: wide shot at seated eye level, 35mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; the empty bowl; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 3 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: NHUNG, as in the image]
[Character B: MINH, as in the image]
[Character C: TRANG, as in the image]
Shot (0-8s). Locked camera. They eat in silence; chopsticks click; no one looks up. Background: the wall clock's second hand ticking.
Ends on: three bowed heads over the table, the empty bowl in the foreground.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 59 · 3s · không mặt người

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: a clay pot of dark caramelised fish with cracked black pepper
Important Details: extreme close-up insert, 85mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; steam; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: no faces visible; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
Shot (0-3s). Locked camera. A thin wisp of steam rises. Background: the wall clock's second hand ticking.
Ends on: a thin wisp of steam rises.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 60 · 4s · NHUNG

Thoại (thu riêng): **Nhung:** Cá kho này là của mày nấu hay của con Trang?

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: NHUNG holding chopsticks. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; the clock behind her; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: NHUNG, as in the image]
Shot (0-4s). Locked camera. She asks without looking up. Lips move with quiet speech. Background: the wall clock's second hand ticking.
Ends on: NHUNG holding a piece of fish in her chopsticks, waiting.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 61 · 4s · TRANG

Thoại (thu riêng): **Trang:** Của em. Anh không ăn được thì đừng ăn.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: TRANG. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; the bulb above; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
Shot (0-4s). Locked camera. She answers sharply. Lips move with quiet speech. Background: the wall clock's second hand ticking.
Ends on: TRANG staring at her own bowl.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 62 · 5s · MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: MINH with chopsticks over the pot. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; steam; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-5s). Locked camera. He lifts a piece of fish to his mouth and chews slowly. Background: the wall clock's second hand ticking.
Ends on: he lifts a piece of fish to his mouth and chews slowly.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 63 · 3s · NHUNG

Thoại (thu riêng): **Nhung:** Sao?

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: NHUNG watching MINH. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; the clock; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: NHUNG, as in the image]
Shot (0-3s). Locked camera. She asks one word. Lips move with quiet speech. Background: the wall clock's second hand ticking.
Ends on: NHUNG watching him, chopsticks paused.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 64 · 4s · MINH

Thoại (thu riêng): **Minh:** Mặn một chút. Nhưng ngon.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: MINH. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; the bulb; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-4s). Locked camera. He answers honestly, a faint smile. Lips move with quiet speech. Background: the wall clock's second hand ticking.
Ends on: MINH chewing, a faint smile.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 65 · 5s · TRANG, NHUNG

Thoại (thu riêng): **Trang:** Mẹ nói con mặn quá. / **Nhung:** Mẹ lúc nào cũng nói vậy.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: TRANG and NHUNG. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow.
Important Details: medium two-shot, 50mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; the bulb; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
[Character B: NHUNG, as in the image]
Shot (0-5s). Locked camera. TRANG laughs; NHUNG replies dryly. Lips move with quiet speech. Background: the wall clock's second hand ticking.
Ends on: TRANG still smiling, NHUNG looking down at her bowl.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 66 · 3s · không mặt người

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: the round wall clock
Important Details: close-up insert, 85mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; the ticking clock; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: no faces visible; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
Shot (0-3s). Locked camera. The second hand jumps three times. Background: the wall clock's second hand ticking.
Ends on: the second hand jumps three times.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 67 · 5s · MINH

Thoại (thu riêng): **Minh:** Hồi đó nhà mình ăn cơm thế này à? Là cả nhà ngồi cùng nhau ấy. Em không nhớ nhiều.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: MINH. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; the bowl; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-5s). Locked camera. He asks quietly, turning his bowl. Lips move with quiet speech. Background: the wall clock's second hand ticking.
Ends on: MINH turning his bowl slowly, eyes on it.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 68 · 10s · NHUNG

Thoại (thu riêng): **Nhung:** Mày không nhớ vì mày nhỏ. Hồi đó tao phải nấu cơm cho cả nhà, còn con Yến thì đi học. Mẹ với ba Hải thì hay đi đâu đó.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: NHUNG. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; the clock behind her; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: NHUNG, as in the image]
Shot (0-10s). Locked camera. She puts her chopsticks down and speaks, voice steady and hard. Lips move with quiet speech. Background: the wall clock's second hand ticking.
Ends on: NHUNG's chopsticks flat on the table, her hands still beside them.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 69 · 3s · TRANG

Thoại (thu riêng): **Trang:** Chị Hai.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: TRANG. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; the bulb; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
Shot (0-3s). Locked camera. She says one word as a warning. Lips move with quiet speech. Background: the wall clock's second hand ticking.
Ends on: TRANG looking at NHUNG, lips pressed.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 70 · 4s · NHUNG

Thoại (thu riêng): **Nhung:** Gì? Tao nói sai à? Mày hỏi thì tao nói.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of NHUNG — use only face, hair and clothing; ignore its background and pose
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: NHUNG. NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; the clock; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: NHUNG, as in the image]
Shot (0-4s). Locked camera. She does not back down. Lips move with quiet speech. Background: the wall clock's second hand ticking.
Ends on: NHUNG holding TRANG's gaze.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 71 · 5s · TRANG, MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: TRANG at the table. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium shot on TRANG, MINH soft in foreground, 50mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; the empty bowl; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
[Character B: MINH, as in the image]
Shot (0-5s). Locked camera. She looks at MINH; at NHUNG, and says nothing. Background: the wall clock's second hand ticking.
Ends on: TRANG looking down at the table, silent.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 72 · 4s · không mặt người

*Không tạo AI* — a phone screen with a Vietnamese text message. Làm bằng đạo cụ thật hoặc đồ họa khi dựng.

#### 73 · 5s · MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: MINH reading his phone under the table. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; phone glow; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-5s). Locked camera. He looks up toward the staircase at frame right and stays looking. Background: the wall clock's second hand ticking.
Ends on: he looks up toward the staircase at frame right and stays looking.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 74 · 4s · không mặt người

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_ban` — use for the room, perspective, light direction and colour; ignore any people in it
Scene: the main room of an old Mekong Delta house, a heavy dark wooden dining table, an ancestral altar in the background, a round wall clock behind the head of the table, a clay pot of caramelised fish with black pepper in the centre, rice bowls, one bowl left empty; a single warm tungsten bulb hanging over the table, the doorway behind dark
Subject: a dark wooden staircase rising to the upper floor
Important Details: wide point-of-view shot, 35mm feel, locked camera; first frame of the shot, before the action starts; the wall clock's second hand ticking; the dark staircase; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: no faces visible; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
Shot (0-4s). Locked camera. Nothing moves; a faint draft stirs a curtain at the top. Background: the wall clock's second hand ticking.
Ends on: the dark top of the staircase, the curtain settling.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

### Cảnh 6 · Phòng Mẹ (cảnh 75–89)

Năm điểm neo — cảm xúc: bí mật · mô-típ: ánh đèn ngủ vàng · đồ vật: phong bì nâu · điểm vỡ: Trang nhìn túi áo · hình cuối: đèn tắt, chỉ còn ánh xanh

#### 75 · 6s · MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_phongme` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table; a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window
Subject: MINH standing before the closed wardrobe in the dim room. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: wide shot, eye level, 35mm feel, locked camera; first frame of the shot, before the action starts; the yellow lamp glow on the wardrobe wood; the lamp glow on the wood; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-6s). Locked camera. He opens the left wardrobe door. Background: the yellow lamp glow on the wardrobe wood.
Ends on: he opens the left wardrobe door.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 76 · 5s · không mặt người

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_phongme` — use for the room, perspective, light direction and colour; ignore any people in it
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table; a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window
Subject: inside the wardrobe: an old biscuit tin, a folded grey shawl, a brown paper envelope at the bottom
Important Details: medium insert, 50mm feel, locked camera; first frame of the shot, before the action starts; the yellow lamp glow on the wardrobe wood; the brown envelope; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: no faces visible; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
Shot (0-5s). Locked camera. Still; dust in the lamp light. Background: the yellow lamp glow on the wardrobe wood.
Ends on: the brown envelope at the bottom of the wardrobe in the lamp light.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 77 · 4s · không mặt người

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_phongme` — use for the room, perspective, light direction and colour; ignore any people in it
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table; a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window
Subject: a young man's hand reaching under the folded shawl
Important Details: close-up on a hand, 85mm feel, locked camera; first frame of the shot, before the action starts; the yellow lamp glow on the wardrobe wood; the brown envelope; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: no faces visible; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
Shot (0-4s). Locked camera. The hand draws out the brown envelope. Background: the yellow lamp glow on the wardrobe wood.
Ends on: the hand draws out the brown envelope.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 78 · 3s · không mặt người

*Không tạo AI* — the front of the envelope with handwriting. Làm bằng đạo cụ thật hoặc đồ họa khi dựng.

#### 79 · 4s · không mặt người

*Không tạo AI* — the back of the envelope with a faded handwritten line. Làm bằng đạo cụ thật hoặc đồ họa khi dựng.

#### 80 · 7s · MINH

Thoại (thu riêng): **Minh:** Mẹ giấu cái gì vậy…

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_phongme` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table; a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window
Subject: MINH sitting on the edge of the narrow bed holding the brown envelope in both hands. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium shot, slow push-in to medium close-up, 50mm feel; first frame of the shot, before the action starts; the yellow lamp glow on the wardrobe wood; the brown envelope; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-7s). Slow push-in. He whispers to himself, turning the envelope over. Lips move with quiet speech. Background: the yellow lamp glow on the wardrobe wood.
Ends on: MINH's face in medium close-up, eyes on the envelope in his hands.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 81 · 4s · MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_phongme` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table; a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window
Subject: MINH on the bed, envelope in hand. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; the yellow lamp glow on the wardrobe wood; creaking floorboards; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-4s). Locked camera. His head snaps toward the door at a sound; he pushes the envelope into his coat pocket, hand stays in the pocket. Background: the yellow lamp glow on the wardrobe wood.
Ends on: he pushes the envelope into his coat pocket, hand stays in the pocket.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 82 · 4s · TRANG

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_phongme` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table; a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window
Subject: TRANG standing in the doorway holding a glass of water. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: medium shot from inside the room, 50mm feel, locked camera; first frame of the shot, before the action starts; the yellow lamp glow on the wardrobe wood; the glass of water; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
Shot (0-4s). Locked camera. She stays in the doorway. Background: the yellow lamp glow on the wardrobe wood.
Ends on: TRANG motionless in the doorway, glass in hand.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 83 · 3s · TRANG

Thoại (thu riêng): **Trang:** Anh tìm gì à?

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_phongme` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table; a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window
Subject: TRANG. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; the yellow lamp glow on the wardrobe wood; the glass; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
Shot (0-3s). Locked camera. She asks evenly. Lips move with quiet speech. Background: the yellow lamp glow on the wardrobe wood.
Ends on: TRANG waiting in the doorway.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 84 · 4s · MINH

Thoại (thu riêng): **Minh:** Không. Em tìm cái khăn mẹ hay đắp.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_phongme` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table; a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window
Subject: MINH, hand in his coat pocket. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; the yellow lamp glow on the wardrobe wood; the coat pocket; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-4s). Locked camera. He answers too quickly. Lips move with quiet speech. Background: the yellow lamp glow on the wardrobe wood.
Ends on: MINH not meeting her eyes, hand still in his pocket.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 85 · 3s · TRANG

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_phongme` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table; a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window
Subject: TRANG. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; the yellow lamp glow on the wardrobe wood; the coat pocket; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
Shot (0-3s). Locked camera. Her eyes drop to his coat pocket and come back up. Background: the yellow lamp glow on the wardrobe wood.
Ends on: her eyes drop to his coat pocket and come back up.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 86 · 6s · TRANG, MINH

Thoại (thu riêng): **Trang:** Ngủ sớm đi. Mai anh còn phải vào viện.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_phongme` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose; Image 3: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table; a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window
Subject: TRANG by the bedside table, MINH on the bed. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium shot, 35mm feel, locked camera; first frame of the shot, before the action starts; the yellow lamp glow on the wardrobe wood; the glass on the table; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly 2 people with visible faces, each appearing once; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
[Character B: MINH, as in the image]
Shot (0-6s). Locked camera. She sets the glass on the bedside table, walks to the door and stops without turning. Lips move with quiet speech. Background: the yellow lamp glow on the wardrobe wood.
Ends on: she sets the glass on the bedside table, walks to the door and stops without turning.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 87 · 8s · TRANG

Thoại (thu riêng): **Trang:** Anh Minh. / **Minh:** Sao? / **Trang:** Nếu anh tìm thấy thứ gì đó của mẹ, anh đừng vội đọc. Mẹ đã chờ thứ đó lâu lắm rồi.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_phongme` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of TRANG — use only face, hair and clothing; ignore its background and pose
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table; a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window
Subject: TRANG's back in the doorway. TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt.
Important Details: medium close-up from behind, 50mm feel, locked camera; first frame of the shot, before the action starts; the yellow lamp glow on the wardrobe wood; the dark corridor beyond; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: TRANG, as in the image]
Shot (0-8s). Locked camera. She speaks without turning; walks out. Lips move with quiet speech. Background: the yellow lamp glow on the wardrobe wood.
Ends on: the empty dark doorway.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 88 · 6s · MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_phongme` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table; a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window
Subject: MINH alone on the bed. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: close-up, 85mm feel, locked camera; first frame of the shot, before the action starts; the yellow lamp glow on the wardrobe wood; the brown envelope; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-6s). Locked camera. He takes the envelope out, looks at it, and puts it back in his pocket. Background: the yellow lamp glow on the wardrobe wood.
Ends on: he takes the envelope out, looks at it, and puts it back in his pocket.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 89 · 5s · MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_phongme` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: an old upstairs bedroom, a dark wooden two-door wardrobe against the wall, a narrow bed with a woven mat and a folded blanket, a small bedside table; a yellow bedside lamp on the left of frame as the only warm source, cold blue night light from a window
Subject: the room with the lamp on, MINH a dark shape on the bed. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: wide shot, 35mm feel, locked camera; first frame of the shot, before the action starts; the yellow lamp glow on the wardrobe wood; the rain outside stops; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-5s). Locked camera. The lamp clicks off; only cold blue window light remains. Background: the yellow lamp glow on the wardrobe wood.
Ends on: only cold blue window light remains.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

### Cảnh 7 · Sân sau (cảnh 90–93)

Năm điểm neo — cảm xúc: quyết định · mô-típ: sương sớm · đồ vật: tờ giấy mực tím · điểm vỡ: Mẹ tỉnh · hình cuối: sân trống

#### 90 · 7s · MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_sansau` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: the back yard of the same old house, a round brick well with moss, a plastic bucket on a rope, banana plants, damp earth; low soft morning sun raking across the yard from camera left, faint mist
Subject: MINH in a faded white t-shirt standing by the well holding the brown envelope. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium shot, eye level, 50mm feel, locked camera; first frame of the shot, before the action starts; mist lifting off the damp ground; mist off the ground; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-7s). Locked camera. He lifts the flap and looks inside without pulling the letter out. Background: mist lifting off the damp ground.
Ends on: he lifts the flap and looks inside without pulling the letter out.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 91 · 3s · không mặt người

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_sansau` — use for the room, perspective, light direction and colour; ignore any people in it
Scene: the back yard of the same old house, a round brick well with moss, a plastic bucket on a rope, banana plants, damp earth; low soft morning sun raking across the yard from camera left, faint mist
Subject: a folded sheet of lined school paper inside the envelope, edges of faded violet ink
Important Details: extreme close-up insert, 85mm feel, locked camera; first frame of the shot, before the action starts; mist lifting off the damp ground; violet ink; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: no faces visible; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
Shot (0-3s). Locked camera. Still. Background: mist lifting off the damp ground.
Ends on: the folded paper inside the open envelope.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 92 · 6s · MINH

Thoại (thu riêng): **Yến (điện thoại):** Minh. Mẹ tỉnh rồi. Mẹ muốn anh vào ngay.

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_sansau` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: the back yard of the same old house, a round brick well with moss, a plastic bucket on a rope, banana plants, damp earth; low soft morning sun raking across the yard from camera left, faint mist
Subject: MINH with the phone at his ear. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: medium close-up, 50mm feel, locked camera; first frame of the shot, before the action starts; mist lifting off the damp ground; the well rope; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-6s). Locked camera. He listens and stands very still. Lips move with quiet speech. Background: mist lifting off the damp ground.
Ends on: MINH lowering the phone, looking toward the gate.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

#### 93 · 7s · MINH

Keyframe (GPT Image 2.5):

```text
References: Image 1: location plate `nha_sansau` — use for the room, perspective, light direction and colour; ignore any people in it; Image 2: locked portrait of MINH — use only face, hair and clothing; ignore its background and pose
Scene: the back yard of the same old house, a round brick well with moss, a plastic bucket on a rope, banana plants, damp earth; low soft morning sun raking across the yard from camera left, faint mist
Subject: MINH by the well. MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button.
Important Details: wide shot, 35mm feel, locked camera; first frame of the shot, before the action starts; mist lifting off the damp ground; the empty yard; a frame grab from a film shot on a digital cinema camera, natural light, no retouch, visible skin pores, fabric creases, low contrast, muted colour
Use Case: keyframe (first frame) for image-to-video generation, 16:9
Constraints: exactly one person with a visible face; no readable text, no subtitles, no watermark; SKIN: no smoothing, no glow; EYES: keep monolid / hooded eyes as described, not enlarged; not a 3D render, not illustration
```

Chuyển động (Kling 3.0, image-to-video):

```text
Preserve faces, wardrobe, room and light from the image.
[Character A: MINH, as in the image]
Shot (0-7s). Locked camera. He puts the envelope in his trouser pocket, walks toward the gate and out of frame; the yard is empty. Background: mist lifting off the damp ground.
Ends on: the yard is empty.
Audio: none.
Negative field: blurry, distorted hands, extra fingers, melted face, face change, extra people, text, subtitles, watermark, jitter
```

## Kiểm tra trước khi tạo

- Mỗi cảnh AI có đủ ba chi tiết: áp lực môi trường (dòng Scene / chi tiết bối cảnh), cử động trên cơ thể (dòng hành động), mô-típ (Important Details).
- Mỗi clip có một chuyển động máy và một hành động chính, kết thúc bằng dòng `Ends on`.
- Chuỗi nhận dạng được chép nguyên văn từ `chuoi_nhan_dang.py`; không sửa trong file này.
- Đổi model khác (Veo, Seedance): giữ keyframe, viết lại khối chuyển động theo file model tương ứng trong skill `mo-phong-cong-viec-dao-dien`.
