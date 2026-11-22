# Prompt tạo ảnh nhân vật — "Mùa Cuối Của Mẹ"

> Viết theo skill `b2-mo-phong-cong-viec-dao-dien` (dựa trên Visual Skills của **Serge Shima**, CC BY 4.0 — https://github.com/smixs/visual-skills) và quy tắc chuỗi nhận dạng của `b2-ho-tro-danh-sach-canh-quay` (DirectorSKILL). Tất cả nhân vật là **hư cấu**.

## Cài đặt chung

| | |
|---|---|
| Model | **GPT Image 2.5** — `gpt-image-2.5-sunburst` cho ảnh nhận dạng và chỉnh sửa (giữ mặt tốt nhất), `flare` cho bản nháp |
| Ảnh chân dung (mục 1) | `quality: medium` (mức `high` làm da bị "chỉnh sửa"), `size: 1024x1536` |
| Bảng 3 góc (mục 2) | `quality: high`, `size: 1536x1024` |
| Bảng biểu cảm (mục 3) | `quality: high`, `size: 1536x1024` |
| Ảnh cũ trắng đen (mục 4) | `quality: medium`, `size: 1536x1024` |
| Ngôn ngữ prompt | Tiếng Anh (model hiểu tốt nhất); ghi chú tiếng Việt |

**Quy trình:** tạo chân dung (mục 1) → chọn ảnh đúng nhất làm **Image 1** khóa nhận dạng → dùng Image 1 làm ảnh tham chiếu cho bảng 3 góc, bảng biểu cảm và mọi keyframe sau này (mục 5). Mỗi lần chỉ đổi một thứ. Chân dung lệch mô tả thì sửa đúng câu mô tả đó, đừng tạo lại y nguyên prompt cũ.

**Kiểm tra ảnh trả về (mỗi nhân vật):** dấu nhận dạng đúng vị trí (sẹo, nốt ruồi, răng); tuổi đúng; da có lỗ chân lông; không tự thêm kính, khuyên tai, chữ; chỉ một người.

## Chuỗi nhận dạng (dán NGUYÊN VĂN vào mọi prompt ảnh và video, không sửa)

| Nhân vật | Chuỗi | Số từ |
|---|---|---:|
| Minh — em út, nhân vật chính | `MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button` | 48 |
| Bà Thu — Mẹ | `BÀ THU, 58, a small Vietnamese woman with a round face, high cheekbones, deep-set double-lidded eyes with heavy crow's feet, a flat brown mole on her right cheekbone, salt-and-pepper hair in a low bun, in a faded light-brown cotton collarless blouse with cloth knot buttons` | 45 |
| Nhung — chị Hai | `NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow` | 45 |
| Yến — chị Ba | `YẾN, 34, a slender Vietnamese woman with an oval face, large slightly downturned eyes, a small rounded nose, a beauty mark just below her left eye, long black hair to mid-back gathered by a brown claw clip, in a pale pink cotton t-shirt with a stretched neckline` | 47 |
| Trang — chị Tư | `TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt` | 45 |
| Ông Hải — cha của Minh | `ÔNG HẢI, 62, a thin Vietnamese man with a long face, hollow cheeks, deep-set tired eyes, grey stubble on a narrow jaw, a dark liver spot on his left temple, very short almost-white hair, in a faded blue-and-brown checked short-sleeve shirt worn untucked with a frayed collar` | 47 |
| Bà Lan — vợ cả Ông Hải | `BÀ LAN, 60, a straight-backed Vietnamese woman with a square face, thin pressed lips, steady unblinking eyes, a small mole above the right corner of her mouth, dyed black hair in a neat high bun, in a dark plum cotton collarless blouse with three cloth knot buttons` | 47 |
| Tài — anh Hai | `TÀI, 40, a broad Vietnamese man with a square kind face, thick eyebrows, a wide nose, a shiny burn scar on the back of his right hand, black hair in a short buzz cut, in a grey cotton tank top stained with black engine oil across the belly` | 48 |
| Hồng — vợ anh Hai | `HỒNG, 38, a plump Vietnamese woman with a round face, thin drawn-on eyebrows, red lipstick, a single deep dimple on her left cheek, shoulder-length permed black hair in loose waves, in a red-and-yellow floral polyester blouse with puffed short sleeves` | 40 |
| Mai — chị Ba (nhà Ông Hải) | `MAI, 38, a small Vietnamese woman with a round gentle face, large clear eyes set wide apart, a soft rounded chin, a tiny mole on the tip of her nose, long black hair tied low over her left shoulder, in a cotton collarless blouse printed with small blue flowers` | 49 |
| Khang — anh Tư | `KHANG, 36, a thin Vietnamese man with a slight paunch, a puffy face, bloodshot eyes under heavy lids, a chipped upper right front tooth, long uncombed black hair falling past his ears, in a wrinkled maroon long-sleeve shirt open at two buttons` | 42 |
| Diễm — vợ anh Tư | `DIỄM, 33, a thin Vietnamese woman with a narrow face, sharp cheekbones, dark circles under her eyes, a small star tattoo on the right side of her neck, bleached yellow hair with two inches of black roots, in a tight black cotton t-shirt` | 43 |
| Phúc — anh Năm | `PHÚC, 34, a wiry Vietnamese man with an angular face, high cheekbones, an easy crooked smile, rows of small healed peck scars on his left forearm, black hair clipped short at the sides, bare-chested in faded khaki cotton shorts with a torn right pocket` | 44 |
| Loan — vợ anh Năm | `LOAN, 32, a thin Vietnamese woman with a long face, eyes that narrow when she reads, a visible gap between her upper front teeth, black hair twisted into a small bun at the crown, in a two-piece cotton home pajama set printed with pink lotus flowers` | 46 |
| Ông Sáu Lộc — ông trùm | `ÔNG SÁU, 65, a heavy-set Vietnamese man with a round placid face, gold-rimmed rectangular glasses, a large flat mole just below his left ear, grey-sided black hair combed straight back, in a freshly ironed white long-sleeve cotton shirt buttoned to the collar` | 42 |
| Thắng — tay chân ông Sáu | `THẮNG, 30, a tall lean Vietnamese man with a long face, restless narrow eyes, a thin pale scar across the bridge of his nose, gelled black hair spiked at the front, in a black cotton t-shirt under a thick gold rope chain` | 42 |
| Ông Tám (trẻ, trong ảnh) | `ÔNG TÁM, 30, a tall broad Vietnamese man with a square jaw, thick dark eyebrows, a wide laughing mouth, one gold-capped upper left canine, wavy black hair side-parted on the left, in a short-sleeve white cotton shirt with the top two buttons open` | 43 |
| Bà Thu lúc 19 tuổi (trong ảnh) | `THU at 19, a small Vietnamese woman with a round face, high cheekbones, double-lidded eyes, a flat brown mole on her right cheekbone, straight black hair hanging loose to her waist, in a plain white cotton collarless blouse holding a conical palm-leaf hat` | 43 |
| Ông Hải lúc 40 tuổi (trong ảnh) | `HẢI at 40, a thin Vietnamese man with a long face, hollow cheeks, deep-set eyes, a dark liver spot on his left temple, short black hair with a side parting on the right, in a dark short-sleeve work shirt with rolled sleeves` | 42 |

Trạng thái thay đổi theo truyện (ướt mưa, băng đầu của Ông Hải tập 7–8, kẹp tóc con bướm của Mai) **không** nằm trong chuỗi; thêm vào phần Subject của từng prompt cảnh.

## 1. Chân dung nhận dạng (16 nhân vật)

### Minh — em út, nhân vật chính

```text
Scene: the upstairs bedroom of an old two-storey Mekong Delta house at night, a yellow bedside lamp the only source, dark wooden wardrobe behind him
Subject: MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button, sitting on the edge of a bed, shoulders slightly rounded, hands in his coat pockets, looking just past the camera
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; faint pores and oil on the nose, mild redness at the nostril wings, a small shaving nick under the jaw, two hairs sticking up at the crown, creases at the coat's elbow bend; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: EYES: monolid, outer corners drooping, not enlarged, not double-lidded; FACE: narrow and slightly asymmetric, no V-line sharpening; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Bà Thu — Mẹ

```text
Scene: a provincial hospital ward in early morning, pale green walls, a metal bed rail, cold fluorescent light mixed with grey window light
Subject: BÀ THU, 58, a small Vietnamese woman with a round face, high cheekbones, deep-set double-lidded eyes with heavy crow's feet, a flat brown mole on her right cheekbone, salt-and-pepper hair in a low bun, in a faded light-brown cotton collarless blouse with cloth knot buttons, propped on two pillows, a thin oxygen cannula under her nose, one hand resting on the blanket, eyes half-open
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; age spots on the back of the hand, fine wrinkles around the mouth, dry lips, a few grey strands escaping the bun on the left, a hospital ID band on the right wrist; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: SKIN: real 58-year-old skin with wrinkles and age spots, no smoothing; BODY: small and slightly frail, not glamorized; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Nhung — chị Hai

```text
Scene: a covered hospital veranda in heavy rain, a sheet of rain falling past the roof edge behind her
Subject: NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow, standing with arms crossed over a paper medical file, weight on both feet, jaw set
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; rain spots on the shoulders of the shirt, faint dark circles, a loose strand stuck to the cheek on the right, a chipped nail on the left thumb; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: EYES: monolid and narrow, not enlarged; FACE: square jaw kept square; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Yến — chị Ba

```text
Scene: a hospital corridor at midday, plastic chairs along the wall, a window at the far end
Subject: YẾN, 34, a slender Vietnamese woman with an oval face, large slightly downturned eyes, a small rounded nose, a beauty mark just below her left eye, long black hair to mid-back gathered by a brown claw clip, in a pale pink cotton t-shirt with a stretched neckline, holding a phone to her ear with both hands, looking down and to the side
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; reddened rims of the eyes and nose tip, smudged eyeliner on the left lower lid, flyaways around the claw clip, a crease across the t-shirt hem; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: FACE: soft and ordinary, not idealized; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Trang — chị Tư

```text
Scene: the front porch of an old wooden house in late afternoon, a straw broom leaning on a pillar, banana leaves behind
Subject: TRANG, 31, a sturdy Vietnamese woman with a long face, long narrow eyes, a straight nose, a crooked upper left canine that shows when she smiles, shoulder-length black hair tucked behind both ears, in a teal canvas apron dusted with flour over a white t-shirt, half-turned, holding the broom handle, mid-sentence, a small smile showing the crooked canine
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; flour on the right forearm, a small healed burn mark on the left wrist, sweat at the hairline, apron strings knotted unevenly; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: TEETH: the upper left canine stays crooked and visible; SKIN: sun-warm and uneven, no glow; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Ông Hải — cha của Minh

```text
Scene: beside a small dusty flatbed truck at dusk, a blue tarp and string of bare bulbs out of focus far behind
Subject: ÔNG HẢI, 62, a thin Vietnamese man with a long face, hollow cheeks, deep-set tired eyes, grey stubble on a narrow jaw, a dark liver spot on his left temple, very short almost-white hair, in a faded blue-and-brown checked short-sleeve shirt worn untucked with a frayed collar, leaning on the truck door, a cheap phone at his ear, looking away down a dirt road
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; deep sun creases on the neck, cracked skin on the knuckles, a grease smudge on the right thumb, stubble patchy on the left cheek, a cigarette burn on the shirt pocket; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: SKIN: weathered, dark tan, deep lines, no smoothing; BODY: thin and slightly stooped; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Bà Lan — vợ cả Ông Hải

```text
Scene: a clean brick house interior with a large ancestral altar, incense smoke, late morning light from a side door
Subject: BÀ LAN, 60, a straight-backed Vietnamese woman with a square face, thin pressed lips, steady unblinking eyes, a small mole above the right corner of her mouth, dyed black hair in a neat high bun, in a dark plum cotton collarless blouse with three cloth knot buttons, standing with a folded cloth in one hand beside the altar, facing camera squarely
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; fine lines around the mouth, a faint vein at the left temple, a thread pulled on the blouse cuff, a slightly uneven hairline at the bun; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: FACE: stern and real, no beauty filter; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Tài — anh Hai

```text
Scene: a roadside motorbike repair shop under a corrugated tin roof, tyres stacked behind, a plastic table with children's notebooks
Subject: TÀI, 40, a broad Vietnamese man with a square kind face, thick eyebrows, a wide nose, a shiny burn scar on the back of his right hand, black hair in a short buzz cut, in a grey cotton tank top stained with black engine oil across the belly, wiping his hands slowly with a black rag, looking at someone off-camera with a shy half-smile
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; oil in the creases of the knuckles, a sweat patch at the chest, a sunburned nose, short stubble; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: BODY: broad and ordinary, not muscle-sculpted; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Hồng — vợ anh Hai

```text
Scene: a wet morning market aisle, a vegetable stall behind, a woven basket on her arm
Subject: HỒNG, 38, a plump Vietnamese woman with a round face, thin drawn-on eyebrows, red lipstick, a single deep dimple on her left cheek, shoulder-length permed black hair in loose waves, in a red-and-yellow floral polyester blouse with puffed short sleeves, leaning in as if sharing a secret, one hand pressed to her blouse pocket
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; lipstick slightly worn at the centre of the lower lip, a sweat sheen on the upper lip, frizz at the perm ends, a loose thread on the sleeve; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: BODY: plump and ordinary, not slimmed; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Mai — chị Ba (nhà Ông Hải)

```text
Scene: stone steps down to a brown river at morning, a wooden boat passing far behind
Subject: MAI, 38, a small Vietnamese woman with a round gentle face, large clear eyes set wide apart, a soft rounded chin, a tiny mole on the tip of her nose, long black hair tied low over her left shoulder, in a cotton collarless blouse printed with small blue flowers, sitting on the steps holding a leaf-wrapped rice cake in both hands, smiling openly at the camera
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; a faded pink plastic butterfly hair clip above her right ear, a small food crumb at the corner of the mouth, a mended seam on the right sleeve, sun freckles on the cheeks; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: EXPRESSION: warm and sincere, never mocking or exaggerated; FACE: an ordinary adult face, not childlike, no caricature; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Khang — anh Tư

```text
Scene: the dirt floor at the edge of a crowded open-air betting ground at night under a blue tarp, a bamboo post behind him
Subject: KHANG, 36, a thin Vietnamese man with a slight paunch, a puffy face, bloodshot eyes under heavy lids, a chipped upper right front tooth, long uncombed black hair falling past his ears, in a wrinkled maroon long-sleeve shirt open at two buttons, sitting on the ground leaning on the bamboo post, a bottle of clear rice liquor in one hand, looking up
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; sweat on the forehead, flushed cheeks, dirt on the right sleeve, a stain on the shirt front, a three-day beard; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: EYES: bloodshot and heavy-lidded; BODY: thin with a small paunch, not athletic; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Diễm — vợ anh Tư

```text
Scene: the same night-time betting ground, a pile of rice sacks behind her
Subject: DIỄM, 33, a thin Vietnamese woman with a narrow face, sharp cheekbones, dark circles under her eyes, a small star tattoo on the right side of her neck, bleached yellow hair with two inches of black roots, in a tight black cotton t-shirt, crouching, counting a fan of crumpled paper betting slips, glancing up
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; chipped red nail polish, smudged mascara, black roots clearly visible, a cheap plastic bracelet on the left wrist; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: SKIN: tired and uneven, no glow; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Phúc — anh Năm

```text
Scene: a backyard of an old thatched house, rows of bamboo rooster cages on the ground, a guava tree
Subject: PHÚC, 34, a wiry Vietnamese man with an angular face, high cheekbones, an easy crooked smile, rows of small healed peck scars on his left forearm, black hair clipped short at the sides, bare-chested in faded khaki cotton shorts with a torn right pocket, squatting beside a cage, one forearm resting on his knee, smiling sideways
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; dust on the shins, a mosquito bite on the shoulder, sweat on the chest, cracked heels in rubber sandals; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: BODY: wiry and ordinary, not gym-sculpted; ANIMALS: roosters stay inside closed cages, no fighting; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Loan — vợ anh Năm

```text
Scene: the porch of the same thatched house, a lottery results slip in her hand
Subject: LOAN, 32, a thin Vietnamese woman with a long face, eyes that narrow when she reads, a visible gap between her upper front teeth, black hair twisted into a small bun at the crown, in a two-piece cotton home pajama set printed with pink lotus flowers, sitting on a low stool, squinting at the slip, lips moving
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; a crease of the pajama fabric at the knee, chapped lips, loose hair at the nape, a rubber band around the left wrist; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: FACE: thin and tired, not glamorized; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Ông Sáu Lộc — ông trùm

```text
Scene: the small office of an old rice mill at night, a wooden desk, a porcelain teapot, a ceiling fan
Subject: ÔNG SÁU, 65, a heavy-set Vietnamese man with a round placid face, gold-rimmed rectangular glasses, a large flat mole just below his left ear, grey-sided black hair combed straight back, in a freshly ironed white long-sleeve cotton shirt buttoned to the collar, seated, holding a small porcelain teacup at chest height, looking at the camera calmly
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; light reflecting on one lens of the glasses, a liver spot on the back of the right hand, a faint tea stain on the cuff; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: EXPRESSION: calm and polite, not theatrically evil; FACE: round and benign-looking; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

### Thắng — tay chân ông Sáu

```text
Scene: next to a parked motorbike on a dark country road, a single streetlight
Subject: THẮNG, 30, a tall lean Vietnamese man with a long face, restless narrow eyes, a thin pale scar across the bridge of his nose, gelled black hair spiked at the front, in a black cotton t-shirt under a thick gold rope chain, standing with one hand on the handlebar, chewing gum, eyes flicking sideways
Important Details: a real photograph taken on a mirrorless camera in available light, no flash, no retouch; a fresh scratch on the left knuckle, sweat on the neck, a small acne mark on the jaw; fine sensor noise in the shadows, natural colour, low contrast, muted saturation
Use Case: casting-style character reference still for a Vietnamese family drama, must read as an unretouched photo of an ordinary person
Constraints: FACE: ordinary young man, not a movie villain; SKIN: visible pores, no smoothing, no glow, no HDR; HAIR: natural, a few flyaways, not glossy; MEDIUM: real photo, not a 3D render, not illustration; no text, no watermark, no jewellery or glasses unless described, only one person in frame
```

## 2. Bảng 3 góc cho dựng 3D

Dùng chung một mẫu, chỉ thay chuỗi nhận dạng. Đính kèm chân dung đã chọn làm Image 1 nếu công cụ cho phép. Bốn nhân vật ưu tiên:

### Minh — em út, nhân vật chính

```text
Scene: clean white background, flat even lighting with no cast shadows, thin horizontal height reference lines in #CCCCCC at head, shoulder, waist, knee and foot level
Subject: MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button — shown three times left to right: front view facing camera, three-quarter view turned 75 degrees right, back view facing away
Important Details: identical proportions and outfit in all three views, feet on the same baseline, arms relaxed at the sides, neutral closed-mouth expression, realistic skin and fabric with visible creases, clothing seams consistent across views
Use Case: 3D modelling reference sheet for a realistic character
Constraints: same person in all three views, no props, no dramatic pose, no background elements, no drop shadows, no text labels, not stylized or cartoon
```

### Bà Thu — Mẹ

```text
Scene: clean white background, flat even lighting with no cast shadows, thin horizontal height reference lines in #CCCCCC at head, shoulder, waist, knee and foot level
Subject: BÀ THU, 58, a small Vietnamese woman with a round face, high cheekbones, deep-set double-lidded eyes with heavy crow's feet, a flat brown mole on her right cheekbone, salt-and-pepper hair in a low bun, in a faded light-brown cotton collarless blouse with cloth knot buttons — shown three times left to right: front view facing camera, three-quarter view turned 75 degrees right, back view facing away
Important Details: identical proportions and outfit in all three views, feet on the same baseline, arms relaxed at the sides, neutral closed-mouth expression, realistic skin and fabric with visible creases, clothing seams consistent across views
Use Case: 3D modelling reference sheet for a realistic character
Constraints: same person in all three views, no props, no dramatic pose, no background elements, no drop shadows, no text labels, not stylized or cartoon
```

### Ông Hải — cha của Minh

```text
Scene: clean white background, flat even lighting with no cast shadows, thin horizontal height reference lines in #CCCCCC at head, shoulder, waist, knee and foot level
Subject: ÔNG HẢI, 62, a thin Vietnamese man with a long face, hollow cheeks, deep-set tired eyes, grey stubble on a narrow jaw, a dark liver spot on his left temple, very short almost-white hair, in a faded blue-and-brown checked short-sleeve shirt worn untucked with a frayed collar — shown three times left to right: front view facing camera, three-quarter view turned 75 degrees right, back view facing away
Important Details: identical proportions and outfit in all three views, feet on the same baseline, arms relaxed at the sides, neutral closed-mouth expression, realistic skin and fabric with visible creases, clothing seams consistent across views
Use Case: 3D modelling reference sheet for a realistic character
Constraints: same person in all three views, no props, no dramatic pose, no background elements, no drop shadows, no text labels, not stylized or cartoon
```

### Nhung — chị Hai

```text
Scene: clean white background, flat even lighting with no cast shadows, thin horizontal height reference lines in #CCCCCC at head, shoulder, waist, knee and foot level
Subject: NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow — shown three times left to right: front view facing camera, three-quarter view turned 75 degrees right, back view facing away
Important Details: identical proportions and outfit in all three views, feet on the same baseline, arms relaxed at the sides, neutral closed-mouth expression, realistic skin and fabric with visible creases, clothing seams consistent across views
Use Case: 3D modelling reference sheet for a realistic character
Constraints: same person in all three views, no props, no dramatic pose, no background elements, no drop shadows, no text labels, not stylized or cartoon
```

Các nhân vật khác: chép một khối trên, thay dòng `Subject:` bằng chuỗi nhận dạng tương ứng ở bảng trên.

## 3. Bảng biểu cảm (4 nhân vật chính)

### Minh — em út, nhân vật chính

```text
Scene: plain warm-grey background, 3x2 grid with thin #DDDDDD divider lines, each cell a head-and-shoulders portrait
Subject: MINH, 27, a slim Vietnamese man with a narrow oval face, monolid eyes with drooping outer corners, a straight nose, a pale 1.5 cm scar through his left eyebrow, short black hair longer on top falling right, in a knee-length black wool coat with a dented top button — same three-quarter-left head angle and same soft window light in every cell
Important Details:
  Cell 1: guarded neutral, eyes lowered
  Cell 2: a small closed-mouth smile
  Cell 3: jaw tight, holding back anger
  Cell 4: eyes wet, lips pressed together
  Cell 5: startled, eyebrows up, mouth slightly open
  Cell 6: listening, head tilted a little
  real photographic skin with pores and wrinkles in every cell, identical hair and clothing in every cell
Use Case: expression reference for actors, animators and AI keyframes
Constraints: the same person in all six cells, no labels or text, no hand gestures except where described, no smoothing, not cartoon
```

### Bà Thu — Mẹ

```text
Scene: plain warm-grey background, 3x2 grid with thin #DDDDDD divider lines, each cell a head-and-shoulders portrait
Subject: BÀ THU, 58, a small Vietnamese woman with a round face, high cheekbones, deep-set double-lidded eyes with heavy crow's feet, a flat brown mole on her right cheekbone, salt-and-pepper hair in a low bun, in a faded light-brown cotton collarless blouse with cloth knot buttons — same three-quarter-left head angle and same soft window light in every cell
Important Details:
  Cell 1: tired neutral
  Cell 2: a soft smile with crow's feet deepening
  Cell 3: worried, brows drawn together
  Cell 4: quietly crying, no sobbing
  Cell 5: stern, lips pressed thin
  Cell 6: eyes closed, resting
  real photographic skin with pores and wrinkles in every cell, identical hair and clothing in every cell
Use Case: expression reference for actors, animators and AI keyframes
Constraints: the same person in all six cells, no labels or text, no hand gestures except where described, no smoothing, not cartoon
```

### Ông Hải — cha của Minh

```text
Scene: plain warm-grey background, 3x2 grid with thin #DDDDDD divider lines, each cell a head-and-shoulders portrait
Subject: ÔNG HẢI, 62, a thin Vietnamese man with a long face, hollow cheeks, deep-set tired eyes, grey stubble on a narrow jaw, a dark liver spot on his left temple, very short almost-white hair, in a faded blue-and-brown checked short-sleeve shirt worn untucked with a frayed collar — same three-quarter-left head angle and same soft window light in every cell
Important Details:
  Cell 1: evasive neutral, looking down-left
  Cell 2: a short embarrassed laugh
  Cell 3: ashamed, chin lowered
  Cell 4: covering his eyes with one hand
  Cell 5: determined, looking straight
  Cell 6: pained, wincing
  real photographic skin with pores and wrinkles in every cell, identical hair and clothing in every cell
Use Case: expression reference for actors, animators and AI keyframes
Constraints: the same person in all six cells, no labels or text, no hand gestures except where described, no smoothing, not cartoon
```

### Nhung — chị Hai

```text
Scene: plain warm-grey background, 3x2 grid with thin #DDDDDD divider lines, each cell a head-and-shoulders portrait
Subject: NHUNG, 36, a Vietnamese woman with a square jaw, thick straight dark eyebrows, sharp monolid eyes, a small round chicken-pox scar on the point of her chin, black hair in a tight high ponytail, in a white cotton shirt with sleeves rolled to the elbow — same three-quarter-left head angle and same soft window light in every cell
Important Details:
  Cell 1: hard neutral
  Cell 2: a brief dry laugh
  Cell 3: furious, nostrils flared
  Cell 4: crying for the first time, face crumpling
  Cell 5: suspicious, eyes narrowed
  Cell 6: exhausted, staring at nothing
  real photographic skin with pores and wrinkles in every cell, identical hair and clothing in every cell
Use Case: expression reference for actors, animators and AI keyframes
Constraints: the same person in all six cells, no labels or text, no hand gestures except where described, no smoothing, not cartoon
```

## 4. Tấm ảnh cũ trắng đen: Ông Tám, Thu, Hải (tập 7, 8, 9, 12)

```text
Scene: a dusty roadside truck stop in the Mekong Delta in the mid-1990s, an old flatbed truck parked behind the group, coconut palms
Subject: three people standing in a row in front of the truck. Left: ÔNG TÁM, 30, a tall broad Vietnamese man with a square jaw, thick dark eyebrows, a wide laughing mouth, one gold-capped upper left canine, wavy black hair side-parted on the left, in a short-sleeve white cotton shirt with the top two buttons open, laughing widely. Middle: THU at 19, a small Vietnamese woman with a round face, high cheekbones, double-lidded eyes, a flat brown mole on her right cheekbone, straight black hair hanging loose to her waist, in a plain white cotton collarless blouse holding a conical palm-leaf hat. Right: HẢI at 40, a thin Vietnamese man with a long face, hollow cheeks, deep-set eyes, a dark liver spot on his left temple, short black hair with a side parting on the right, in a dark short-sleeve work shirt with rolled sleeves, standing half a step back, smiling shyly
Important Details: a real black-and-white film photograph from the 1990s, printed on paper and scanned decades later: visible grain, soft focus, slight overexposure on the sky, faded greys, a crease across the lower right corner, small foxing spots, a white paper border
Use Case: an old family photograph prop that appears in several episodes
Constraints: only these three people, each appears once; black and white only, no colour; no text or date stamp; not a modern photo with a filter; faces must match their descriptions
```

Ba người trong một ảnh là việc khó với model: nếu mặt bị lẫn, tạo từng người riêng rồi ghép, hoặc chỉnh từng người bằng mẫu ở mục 5.

## 5. Mẫu chỉnh sửa: đặt nhân vật vào cảnh (dùng cho keyframe)

Image 1 = chân dung đã khóa; Image 2 = ảnh bối cảnh trống. Mỗi lần chỉ một thay đổi, lặp lại dòng Preserve mỗi lần.

```text
Change: place the person from Image 1 into the scene from Image 2 — [hành động một câu, có trạng thái kết thúc]
Preserve: face, identity, age, scar/mole positions, hair, clothing from Image 1; perspective, lighting direction and colour temperature of Image 2
Constraints: one person only, no extra objects, no redesign of the face, no beautification, no text
```

## Chưa làm

- Sáu đứa trẻ (Ty, Na, Bi, Tèo, Mít, Bông): chưa viết prompt chân dung. Nên làm theo phong cách chung, tránh ảnh cận mặt quá thật của trẻ em khi chưa cần.
- Các keyframe theo từng cảnh của tập 1: xem `tap/tap-01-danh-sach-canh-quay.md`, cột Ghi chú tạo AI.
