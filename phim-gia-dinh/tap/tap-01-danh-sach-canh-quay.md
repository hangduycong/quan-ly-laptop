# Danh sách cảnh quay — Tập 1: Về nhà

> Lập theo skill `b2-ho-tro-danh-sach-canh-quay` (DirectorSKILL, mode D) từ `tap-01-ve-nha.md`. Giả định: khung **16:9**, bảng dùng được cho cả quay thật lẫn tạo clip AI; clip AI giữ 3–8 giây, cảnh thoại dài hơn ghi chú cách tách.

## Luật hình ảnh của tập (director's book rút gọn)

| Hạng mục | Quy định |
|---|---|
| Ống kính | 35mm (toàn cảnh, bối cảnh), 50mm (đối thoại), 85mm (cận cảm xúc, chèn chi tiết) |
| Chuyển động máy | Mặc định **đứng yên**. Chỉ 4 chuyển động trong cả tập: đẩy vào chậm ở 18, 43, 80; lia theo ở 48 |
| Màu | Bệnh viện lạnh 5000K, hơi xanh. Trường gà: bóng đèn tròn vàng + khói, tương phản cao. Nhà cũ ấm 2700K. Phong bì nâu là mảng màu đậm nhất ở cảnh 6 |
| Nhịp | ASL khoảng 5.0 giây theo bảng. Cảnh bữa cơm cắt chậm nhất; trường gà cắt nhanh nhất |
| Chuỗi nhận dạng | Dán nguyên văn từ `../nhan-vat-3d/chuoi-nhan-dang.json` vào mọi prompt keyframe / video; không viết lại |
| Chữ trong khung | Tin nhắn, chữ trên phong bì: **không tạo bằng AI** (model hay sai dấu tiếng Việt). Quay đạo cụ thật hoặc chèn chữ khi dựng |

### Bối cảnh

| Mã | Bối cảnh | Hướng sáng chính |
|---|---|---|
| `loc_bv_hanhlang` | Hành lang bệnh viện tỉnh | đèn huỳnh quang trần, sáng phẳng, cửa sổ cuối hành lang làm viền |
| `loc_bv_phong` | Phòng bệnh 4 giường | cửa sổ trái máy (khi nhìn về giường), ánh sáng xám buổi sáng; huỳnh quang phụ |
| `loc_bv_hien` | Mái hiên bệnh viện trời mưa | ánh sáng xám từ sân, nguồn phía trước nhân vật, màn mưa làm tiền cảnh |
| `loc_truongga` | Trường gà sau vườn dừa | bóng đèn tròn treo dây trên đầu đám đông, trời chạng vạng xanh phía sau |
| `loc_nha_san` | Ngõ, cổng gỗ, sân nhà cũ | nắng chiều sau mưa, thấp, từ phải máy khi nhìn vào hiên |
| `loc_nha_ban` | Bàn ăn giữa nhà | bóng đèn sợi đốt trên bàn, ấm; cửa trước tối |
| `loc_nha_phongme` | Phòng Mẹ tầng hai | đèn ngủ vàng đầu giường (trái máy khi nhìn về tủ), cửa sổ xanh đêm |
| `loc_nha_sansau` | Sân sau, giếng nước | sáng sớm, nắng xiên mềm |

### Đồ vật cần khớp liên tục

Túi đồ đen của Minh · máy ghi âm nhỏ của Minh (túi áo ngực) · hồ sơ bệnh án của Nhung · chuỗi hạt của Yến · ống thở của Bà Thu · xấp giấy tên khách (Thắng → Ông Hải) · chổi rơm · ghế nhựa gãy một chân · nồi cá kho tiêu · chén cơm để trống · đồng hồ treo tường · phong bì nâu · ly nước của Trang.

### Cách đọc cột Rủi ro

`Mức điểm (Hành động/Người/Máy/Thời lượng/Tương tác/Liên tục)`. **Xanh** 0–5: tạo thẳng. **Vàng** 6–11: làm keyframe đầu (và cuối nếu được) trước, đơn giản hóa một yếu tố. **Đỏ** 12+, hoặc Tương tác 3 cộng một yếu tố 3: tách cảnh trước khi tạo.

---

## Cảnh 1 · Hành lang bệnh viện, sáng sớm (0:00–0:39)

`loc_bv_hanhlang` · Minh: áo khoác đen, túi đồ đen tay phải · Nhung: sơ mi trắng, hồ sơ bệnh án tay trái

| # | Thời lượng | Beat · nhiệm vụ | Nội dung khung hình · diễn xuất (đầu → cuối) | Cỡ · góc · ống kính · máy | Rủi ro | Ghi chú tạo AI |
|---:|---:|---|---|---|---|---|
| 01 | 6s | B1 · thiết lập: Minh đến một mình | Hành lang dài trống, ghế nhựa dọc tường. Minh vào từ cuối hành lang → đi về phía máy → dừng trước cửa cấp cứu, nửa người phải khung | WS, ngang mắt, 35mm, đứng yên | Xanh 5 (1/1/0/2/0/1) | Ghi "he walks toward camera and stops in front of the door, standing still". Một hành động duy nhất |
| 02 | 4s | B1 · lý do về | Màn hình điện thoại: tin của Trang "Anh về đi. Mẹ đang hỏi anh." | ECU chèn, từ trên xuống, 85mm, đứng yên | Xanh 2 (0/1/0/1/0/0) | **Không tạo AI.** Quay màn hình thật hoặc làm đồ họa khi dựng |
| 03 | 4s | B1 · Minh bị kéo về | Ngón cái Minh gõ trả lời → thở ra, hạ điện thoại | CU, ngang mắt, 85mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | Không cần thấy chữ trên màn hình |
| 04 | 6s | B2 · Nhung xuất hiện | Cửa cấp cứu mở, Nhung bước ra cầm hồ sơ → thấy Minh → khựng lại, đứng yên | MS, ngang mắt, 50mm, đứng yên | Vàng 6 (2/1/0/2/0/1) | Keyframe đầu: cửa đóng, Nhung chưa ra. Kết thúc rõ: "she stops and stands still, looking at him" |
| 05 | 5s | B2 · khoảng cách hai chị em | Nhung: "Mày về rồi." / "Đột quỵ nhẹ…" | MCU Nhung qua vai Minh, 50mm, đứng yên | Vàng 6 (1/2/0/1/0/2) | Vai Minh tiền cảnh trái khung. Thoại dài hơn 5s: quay tiếp bằng 06 |
| 06 | 5s | B2 · phản ứng | Minh nghe, gật đầu, không nói được | MCU Minh qua vai Nhung, 50mm, đứng yên | Vàng 6 (1/2/0/1/0/2) | Giữ đúng trục 180°: Minh nhìn sang trái khung, Nhung sang phải |
| 07 | 9s | B2 · Nhung nhường đường | Nhung: "Vào đi. Bà hỏi mày từ tối qua." → Minh đi lướt qua Nhung vào phòng → Nhung đứng lại nhìn xuống hành lang | MS hai người, ngang mắt, 35mm, đứng yên | Vàng 9 (2/2/0/3/1/1) | Tách cho AI: 07a Nhung nói (4s), 07b Minh đi qua, ra khỏi khung (5s) |

## Cảnh 2 · Phòng bệnh (0:39–1:39)

`loc_bv_phong` · Bà Thu: ống thở, nằm nghiêng · Yến: ghế nhựa cạnh giường, chuỗi hạt · Trang: đứng ở cửa sổ, quay lưng

| # | Thời lượng | Beat · nhiệm vụ | Nội dung khung hình · diễn xuất (đầu → cuối) | Cỡ · góc · ống kính · máy | Rủi ro | Ghi chú tạo AI |
|---:|---:|---|---|---|---|---|
| 08 | 6s | B3 · ai đang ở đâu | Phòng 4 giường, chỉ một giường có người. Yến ngồi lần chuỗi hạt; Trang quay lưng ở cửa sổ. Minh bước vào từ trái khung → dừng ở cuối giường | WS, cao hơn mắt một chút, 35mm, đứng yên | Vàng 10 (1/3/0/2/1/3) | Bốn người trong khung khó. Làm keyframe đầu có đủ 3 người, Minh vào sau |
| 09 | 4s | B3 · Mẹ nhận ra con | Bà Thu mở mắt sau ống thở, môi mấp máy "Minh" | CU, ngang gối, 85mm, đứng yên | Vàng 6 (1/1/0/1/1/2) | Ống thở là đạo cụ gắn với mặt: ghi rõ "a thin clear oxygen cannula under her nose stays in place" |
| 10 | 6s | B3 · Minh đến gần | Minh đi tới, đặt túi xuống sàn, cúi xuống giường → dừng khi mặt ngang mặt Mẹ | MS, ngang mắt, 50mm, đứng yên | Vàng 8 (2/2/0/2/1/1) | Hai hành động: đặt túi + cúi. Nếu hỏng, bỏ đặt túi khỏi khung |
| 11 | 3s | B3 · chạm | Tay Bà Thu nhấc lên, chạm khẽ ngón tay Minh → giữ yên | ECU tay, 85mm, đứng yên | Vàng 9 (2/2/0/0/3/2) | Không có mặt nên không vướng luật Đỏ. Ghi rõ "her fingertips rest on the back of his hand and stay still" |
| 12 | 4s | B3 · Mẹ lo cho con | Bà Thu: "Con gầy quá." | CU Bà Thu, 85mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 13 | 5s | B3 · Minh cười | Minh cười nhẹ: "Con ăn đủ mà mẹ." | CU Minh, 85mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | Sẹo lông mày trái phải thấy được |
| 14 | 6s | B4 · Yến xúc động, Trang đứng ngoài | Yến bật cười rồi lau nước mắt; nền: lưng Trang ở cửa sổ, không động | MS Yến, Trang mờ phía sau, 50mm, đứng yên | Vàng 6 (1/2/0/2/0/1) | Trang trong nền chỉ đứng yên: "the woman at the window does not move" |
| 15 | 4s | B4 · Mẹ gọi Trang | Bà Thu: "Trang. Con đứng đó làm gì, lại đây." | CU Bà Thu, 85mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 16 | 6s | B4 · Trang miễn cưỡng | Trang quay lại → đi tới giường → dừng cách Minh một bước, không nhìn anh | MS, ngang mắt, 35mm, đứng yên | Vàng 8 (2/2/0/2/0/2) | Kết thúc: "she stops one step from him and looks at the bed" |
| 17 | 6s | B4 · "hai đứa làm lành đi" | Minh và Trang đứng cạnh nhau, nhìn hai hướng; tiếng Bà Thu ngoài khung | MCU hai người, ngang mắt, 50mm, đứng yên | Vàng 6 (0/2/0/2/0/2) | Không hành động, chỉ thở. Dễ nhất cảnh |
| 18 | 6s | B4 · Mẹ khép lại | Bà Thu nhắm mắt: "Mẹ mệt rồi…" | CU → đẩy vào chậm thành ECU, 85mm | Vàng 6 (1/1/1/2/0/1) | Một chuyển động máy duy nhất, không chuyển động mặt khác |
| 19 | 4s | B4 · rời phòng | Phòng từ cửa: ba người con đi ra, chỉ còn Bà Thu và giường trống | WS, 35mm, đứng yên | Vàng 8 (1/3/0/1/0/3) | Có thể thay bằng giường + tiếng bước chân để giảm rủi ro |

## Cảnh 3 · Mái hiên bệnh viện, mưa (1:39–2:48)

`loc_bv_hien` · bốn người đứng thành hàng ngang dưới mái hiên, thứ tự trái → phải: Trang, Nhung, Yến, Minh · Yến: điện thoại tay phải

| # | Thời lượng | Beat · nhiệm vụ | Nội dung khung hình · diễn xuất (đầu → cuối) | Cỡ · góc · ống kính · máy | Rủi ro | Ghi chú tạo AI |
|---:|---:|---|---|---|---|---|
| 20 | 7s | B5 · bốn người, một mái hiên | Màn mưa tiền cảnh; bốn người đứng, không ai nhìn ai | WS từ phía sân, ngang mắt, 35mm, đứng yên | Vàng 8 (0/3/0/2/0/3) | Mưa và 4 người: tạo keyframe kỹ, chọn ảnh có đủ 4 khuôn mặt đúng |
| 21 | 4s | B5 · vấn đề | Nhung: "Mẹ muốn về nhà." | MCU Nhung, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 22 | 5s | B5 · phản đối | Yến: "Chị nói bác sĩ rồi…" | MCU Yến, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 23 | 4s | B5 · tiền | Trang: "Ai trả tiền điều dưỡng?" | MCU Trang, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 24 | 4s | B5 · Minh nhận | Minh: "Để em lo." | CU Minh, 85mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 25 | 6s | B6 · Nhung đánh | Nhung quay hẳn sang Minh: "Mày lo bằng gì?…" | MS Nhung qua vai Minh, 50mm, đứng yên | Vàng 7 (1/2/0/2/0/2) | — |
| 26 | 4s | B6 · Minh đỡ | Minh: "Chị đừng nói như vậy." | MCU Minh qua vai Nhung, 50mm, đứng yên | Vàng 6 (1/2/0/1/0/2) | Trục: Minh nhìn trái khung |
| 27 | 6s | B6 · vết thương cũ | Nhung: "Tao nói sự thật. Mày đi bao năm…" | MCU Nhung, 50mm, đứng yên | Xanh 5 (1/1/0/2/0/1) | — |
| 28 | 5s | B6 · Trang chen vào | Trang bước một bước vào giữa hai người → dừng | MS ba người, 35mm, đứng yên | Vàng 8 (1/3/0/1/0/3) | Kết thúc: "she stands between them and stops" |
| 29 | 6s | B7 · cuộc gọi bí mật | Điện thoại Yến rung → Yến đi ra xa vài bước → nghe, lưng quay về nhóm | MS Yến, 50mm, đứng yên | Vàng 7 (2/1/0/2/1/1) | Tách nếu cần: 29a lấy điện thoại (3s), 29b đi ra (3s) |
| 30 | 6s | B7 · nói khẽ | Yến: "Dạ, anh Hai… Anh đừng nói với ba vội." | CU Yến nghiêng, 85mm, đứng yên | Xanh 5 (1/1/0/2/1/0) | Tiếng mưa che bớt thoại |
| 31 | 5s | B7 · nói dối | Yến quay về nhóm. Nhung: "Ai gọi?" Yến: "Bạn em." | MS hai người, 50mm, đứng yên | Vàng 6 (1/2/0/1/0/2) | — |
| 32 | 4s | B7 · Nhung nghi | Nhung nhìn Yến, không chớp | CU Nhung, 85mm, đứng yên | Xanh 3 (0/1/0/1/0/1) | — |
| 33 | 3s | B7 · Yến né | Yến cụp mắt, nhìn xuống sân mưa | CU Yến, 85mm, đứng yên | Xanh 3 (1/1/0/0/0/1) | — |

## Cảnh 3b · Trường gà ven sông, chạng vạng (2:48–3:54)

`loc_truongga` · Ông Hải: áo caro, cạnh xe tải nhỏ · Thắng: áo thun đen, dây chuyền vàng · **Không quay gà chọi nhau.** Chỉ lưng người, tay cầm tiền, tiếng ồn.

| # | Thời lượng | Beat · nhiệm vụ | Nội dung khung hình · diễn xuất (đầu → cuối) | Cỡ · góc · ống kính · máy | Rủi ro | Ghi chú tạo AI |
|---:|---:|---|---|---|---|---|
| 34 | 6s | B8 · thế giới của ông Sáu | Bạt xanh sau vườn dừa, dây bóng đèn tròn, khói, đám đông chỉ thấy lưng | EWS, góc cao từ ngọn dừa, 35mm, đứng yên | Vàng 6 (0/3/0/2/0/1) | Đám đông là nền: không cần mặt. Ghi "seen only from behind, no animals visible" |
| 35 | 4s | B8 · tiền | Tay giơ tiền giấy, tay đập vé; không thấy mặt | MS tay, 50mm, đứng yên | Xanh 5 (1/3/0/1/0/0) | Không chữ, không mệnh giá rõ |
| 36 | 5s | B8 · Ông Hải đứng ngoài | Ông Hải đứng rìa đám đông cạnh xe tải, nhìn đồng hồ đeo tay → hạ tay | MS, ngang mắt, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | Đồng hồ là đạo cụ của cảnh này, không thêm vào chuỗi nhận dạng |
| 37 | 4s | B9 · áp lực | Thắng đi vào khung, chìa xấp giấy | MS hai người, 50mm, đứng yên | Vàng 7 (1/2/0/1/1/2) | Kết thúc khi giấy chìa ra, **chưa trao** |
| 38 | 3s | B9 · bị ép nhận | Xấp giấy được nhét vào tay Ông Hải | ECU tay, 85mm, đứng yên | Vàng 9 (2/2/0/0/3/2) | Không có mặt nên không thành Đỏ. Keyframe đầu và cuối nếu công cụ có |
| 39 | 5s | B9 · mệnh lệnh | Thắng: "Chú Hải. Tối nay chở mấy ông này về thị xã…" | MCU Thắng, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 40 | 3s | B9 · từ chối yếu | Ông Hải: "Tối nay tôi bận." | MCU Ông Hải, 50mm, đứng yên | Xanh 3 (1/1/0/0/0/1) | — |
| 41 | 5s | B9 · đòn | Thắng cười: "Thằng Tư nhà chú còn nợ…" | MCU Thắng, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 42 | 3s | B10 · cuộc gọi | Màn hình điện thoại: "Tài" | ECU chèn, 85mm, đứng yên | Xanh 1 (0/0/0/0/0/1) | **Không tạo AI.** Đồ họa khi dựng |
| 43 | 8s | B10 · tin dữ | Ông Hải nghe → mặt đổi sắc → quay lưng lại đám đông, nói nhỏ | MCU, đẩy vào chậm, 85mm | Vàng 9 (2/1/1/2/0/3) | Tách: 43a nghe, mặt đổi (4s); 43b quay lưng (4s, đứng yên máy) |
| 44 | 5s | B10 · giằng co | Ông Hải cúp máy, nhìn về con đường đất dẫn ra lộ | MS, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 45 | 4s | B10 · lối ra | Con đường đất vắng dẫn ra lộ (góc nhìn Ông Hải) | WS POV, 35mm, đứng yên | Xanh 1 (0/0/0/1/0/0) | Không người |
| 46 | 5s | B10 · lựa chọn | Ông Hải mở cửa xe, leo lên ghế lái, xấp giấy trên tay → đóng cửa | MS, 35mm, đứng yên | Vàng 7 (3/1/0/1/1/1) | Leo lên xe hay lỗi chân tay: tách 46a mở cửa (2s), 46b ngồi vào đóng cửa (3s) |
| 47 | 6s | B10 · đi sai hướng | Xe tải chạy ra lộ, rẽ theo hướng **ngược** với bảng chỉ đường "Bệnh viện" | WS, 35mm, đứng yên | Xanh 4 (1/0/0/2/0/1) | Bảng chỉ đường: làm khi dựng hoặc đạo cụ thật, không tạo chữ AI |

## Cảnh 4 · Nhà cũ, buổi chiều (3:54–4:47)

`loc_nha_san` · Minh: áo khoác đen, túi đồ, xe máy · Trang: áo thun trắng, tạp dề, chổi rơm · sân: 2 ghế nhựa (1 gãy chân), chậu hoa giấy héo, cây mít

| # | Thời lượng | Beat · nhiệm vụ | Nội dung khung hình · diễn xuất (đầu → cuối) | Cỡ · góc · ống kính · máy | Rủi ro | Ghi chú tạo AI |
|---:|---:|---|---|---|---|---|
| 48 | 7s | B11 · trở về | Minh chạy xe máy vào ngõ hẹp → dừng trước cổng gỗ bong sơn | WS, lia theo chậm, 35mm | Vàng 7 (1/1/1/2/0/2) | Chuyển động máy duy nhất của cảnh. Xe dừng hẳn ở cuối |
| 49 | 4s | B11 · đẩy cổng | Tay Minh đẩy cổng gỗ mở vào trong | MS, 50mm, đứng yên | Vàng 6 (1/1/0/1/2/1) | Bản lề, cánh cổng: ghi rõ "the gate swings inward and stops half open" |
| 50 | 7s | B11 · ngôi nhà | Sân sau mưa: chuối, mít, chậu hoa giấy héo, hai ghế nhựa; Trang quét lá ở hiên, Minh đứng ở cổng (tiền cảnh) | WS, ngang mắt, 35mm, đứng yên | Vàng 7 (1/2/0/2/0/2) | Ghế gãy phải nhìn thấy được ở bên phải khung |
| 51 | 5s | B11 · đón | Trang dừng chổi: "Anh vào đi. Em để cơm trên bàn." | MS Trang, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 52 | 5s | B11 · hỏi han | Minh: "Chị về lúc nào?" Trang: "Hồi trưa. Đi xe đò." | MCU qua vai, 50mm, đứng yên | Xanh 5 (1/2/0/1/0/1) | Hai câu ngắn, giữ trong một cảnh |
| 53 | 6s | B12 · mùi nhà | Minh bước lên hiên, đặt túi xuống, hít mùi củi và nước mắm | MS, 50mm, đứng yên | Xanh 5 (2/1/0/2/0/0) | Kết thúc: "he stands still on the porch, eyes closed for a moment" |
| 54 | 6s | B12 · Mẹ hiện diện | Trang: "Ừ. Mẹ dặn nấu cá kho tiêu…" → cầm chổi đi vào trong, ra khỏi khung | MCU Trang → ra khung, 50mm, đứng yên | Xanh 5 (1/1/0/2/0/1) | — |
| 55 | 4s | B12 · chỗ của Minh | Ghế nhựa gãy một chân, dựng nghiêng vào tường | CU chèn, 85mm, đứng yên | Xanh 1 (0/0/0/1/0/0) | Đồ vật quan trọng của cả mùa: chụp kỹ, giữ đúng chân gãy (chân sau bên trái) |
| 56 | 3s | B12 · lẩm bẩm | Minh nhìn ghế: "Vẫn chưa sửa." | CU Minh, 85mm, đứng yên | Xanh 3 (0/1/0/0/0/2) | — |
| 57 | 6s | B12 · Trang trả lời từ trong nhà | Trang ló đầu ra cửa: "Ai sửa? Anh đi từ hồi học cấp ba, cái ghế đó là của anh." | MS cửa, 50mm, đứng yên | Xanh 5 (1/1/0/2/0/1) | — |

## Cảnh 5 · Bữa cơm đầu tiên, tối (4:47–6:06)

`loc_nha_ban` · bàn gỗ: Nhung (đầu bàn xa máy), Minh (trái khung), Trang (phải khung), chén để trống phía gần máy · nồi cá kho tiêu giữa bàn · đồng hồ treo tường sau lưng Nhung

| # | Thời lượng | Beat · nhiệm vụ | Nội dung khung hình · diễn xuất (đầu → cuối) | Cỡ · góc · ống kính · máy | Rủi ro | Ghi chú tạo AI |
|---:|---:|---|---|---|---|---|
| 58 | 8s | B13 · ba người, một chén trống | Bàn ăn, ba người gắp cơm im lặng; chén trống gần máy, đồng hồ sau lưng Nhung | WS, ngang mắt ngồi, 35mm, đứng yên | Vàng 10 (1/3/0/2/1/3) | Keyframe kỹ cả bàn (đồ ăn, chén, vị trí ghế) và dùng lại cho mọi cảnh bàn ăn |
| 59 | 3s | B13 · Mẹ ở trong món ăn | Nồi đất cá kho tiêu còn bốc hơi | ECU chèn, 85mm, đứng yên | Xanh 0 (0/0/0/0/0/0) | Đồ ăn: dùng kiến thức sản phẩm/ẩm thực; hơi nước nhẹ |
| 60 | 4s | B13 · Nhung thử | Nhung: "Cá kho này là của mày nấu hay của con Trang?" | MCU Nhung, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 61 | 4s | B13 · Trang gai góc | Trang: "Của em. Anh không ăn được thì đừng ăn." | MCU Trang, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 62 | 5s | B14 · Minh ăn | Minh gắp miếng cá, đưa vào miệng, nhai chậm | CU Minh, 85mm, đứng yên | Xanh 5 (2/1/0/1/1/0) | Ăn uống hay lỗi miệng/đũa: tách 62a gắp (2s), 62b nhai (3s) |
| 63 | 3s | B14 · Nhung dò | Nhung nhìn Minh: "Sao?" | CU Nhung, 85mm, đứng yên | Xanh 3 (1/1/0/0/0/1) | — |
| 64 | 4s | B14 · Minh thật thà | Minh: "Mặn một chút. Nhưng ngon." | MCU Minh, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 65 | 5s | B14 · ấm lên một chút | Trang cười: "Mẹ nói con mặn quá." Nhung: "Mẹ lúc nào cũng nói vậy." | MS hai chị, 50mm, đứng yên | Xanh 5 (1/2/0/1/0/1) | — |
| 66 | 3s | B15 · im lặng | Đồng hồ treo tường, kim giây nhảy | CU chèn, 85mm, đứng yên | Xanh 1 (0/0/0/0/0/1) | Kim đồng hồ là chuyển động duy nhất |
| 67 | 5s | B15 · câu hỏi | Minh: "Hồi đó nhà mình ăn cơm thế này à?… Em không nhớ nhiều." | MCU Minh, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 68 | 10s | B15 · vết thương của Nhung | Nhung đặt đũa xuống: "Mày không nhớ vì mày nhỏ. Hồi đó tao phải nấu cơm…" | MCU Nhung, 50mm, đứng yên | Vàng 7 (1/1/0/3/1/1) | Quay thật giữ một cảnh. AI: tách 68a đặt đũa (3s) + 68b nói (7s, chỉ cử động môi) |
| 69 | 3s | B15 · can | Trang: "Chị Hai." | CU Trang, 85mm, đứng yên | Xanh 3 (0/1/0/0/0/2) | — |
| 70 | 4s | B15 · không lùi | Nhung: "Gì? Tao nói sai à? Mày hỏi thì tao nói." | MCU Nhung, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 71 | 5s | B15 · Trang im | Trang nhìn Minh, rồi nhìn Nhung, không nói | MS Trang, Minh mờ trước, 50mm, đứng yên | Xanh 5 (1/2/0/1/0/1) | Chỉ chuyển ánh mắt, hai lần |
| 72 | 4s | B16 · tin nhắn | Màn hình: tin của Yến "Mẹ hỏi em mang lá thư trong tủ về cho mẹ." | ECU chèn, 85mm, đứng yên | Xanh 1 (0/0/0/1/0/0) | **Không tạo AI.** Đồ họa khi dựng |
| 73 | 5s | B16 · móc câu | Minh đọc → ngẩng lên nhìn về phía cầu thang | CU Minh, 85mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | Hướng nhìn: phải khung (cầu thang ở bên phải nhà) |
| 74 | 4s | B16 · tầng trên | Cầu thang gỗ tối dẫn lên tầng hai | WS POV, 35mm, đứng yên | Xanh 1 (0/0/0/1/0/0) | — |

## Cảnh 6 · Phòng Mẹ, tầng hai, đêm (6:06–7:18)

`loc_nha_phongme` · đèn ngủ vàng đầu giường · tủ áo gỗ cũ sát tường · Minh: áo khoác đen, máy ghi âm túi ngực · Trang: áo thun trắng, ly nước

| # | Thời lượng | Beat · nhiệm vụ | Nội dung khung hình · diễn xuất (đầu → cuối) | Cỡ · góc · ống kính · máy | Rủi ro | Ghi chú tạo AI |
|---:|---:|---|---|---|---|---|
| 75 | 6s | B17 · căn phòng của Mẹ | Phòng tối, đèn ngủ vàng; Minh đứng trước tủ, mở cánh trái | WS, ngang mắt, 35mm, đứng yên | Vàng 6 (1/1/0/2/1/1) | Một hành động: mở cánh tủ |
| 76 | 5s | B17 · những thứ Mẹ giữ | Trong tủ: hộp bánh thiếc cũ, khăn choàng xám, phong bì nâu ở đáy | MS chèn, 50mm, đứng yên | Xanh 1 (0/0/0/1/0/0) | Phong bì nâu đậm hơn mọi thứ xung quanh |
| 77 | 4s | B17 · nhặt lên | Tay Minh rút phong bì từ dưới khăn | CU tay, 85mm, đứng yên | Vàng 6 (2/1/0/1/2/0) | — |
| 78 | 3s | B17 · tên Mẹ | Mặt trước phong bì: chữ viết tay "Thu" | ECU chèn, 85mm, đứng yên | Xanh 1 (0/0/0/0/0/1) | **Không tạo chữ AI.** Đạo cụ thật viết tay |
| 79 | 4s | B17 · lời dặn | Mặt sau: dấu niêm bong, dòng mực nhạt "Đừng để các con biết trước" | ECU chèn, 85mm, đứng yên | Xanh 2 (0/0/0/1/0/1) | **Không tạo chữ AI.** Đây là khung hình quan trọng nhất tập |
| 80 | 7s | B18 · Minh với bí mật | Minh ngồi xuống mép giường Mẹ, cầm phong bì, thì thầm "Mẹ giấu cái gì vậy…" | MS → đẩy vào chậm MCU, 50mm | Vàng 8 (1/1/1/2/2/1) | Chuyển động máy thứ ba của tập |
| 81 | 4s | B18 · giật mình | Tiếng bước chân (âm thanh) → Minh nhét phong bì vào túi áo khoác | CU, 85mm, đứng yên | Vàng 8 (2/1/0/1/2/2) | Nhét đồ vào túi hay lỗi tay: kết thúc ở tay đã nằm trong túi |
| 82 | 4s | B19 · Trang đến | Trang đứng ở cửa, cầm ly nước | MS từ trong phòng, 50mm, đứng yên | Xanh 4 (0/1/0/1/1/1) | — |
| 83 | 3s | B19 · hỏi | Trang: "Anh tìm gì à?" | MCU Trang, 50mm, đứng yên | Xanh 3 (1/1/0/0/0/1) | — |
| 84 | 4s | B19 · nói dối | Minh: "Không. Em tìm cái khăn mẹ hay đắp." | MCU Minh, 50mm, đứng yên | Xanh 4 (1/1/0/1/0/1) | — |
| 85 | 3s | B19 · Trang thấy | Mắt Trang nhìn xuống túi áo khoác của Minh | CU Trang, 85mm, đứng yên | Xanh 3 (1/1/0/0/0/1) | Hướng nhìn xuống trái khung |
| 86 | 6s | B19 · không hỏi thêm | Trang đặt ly nước xuống đầu giường → đi ra cửa → dừng, không quay lại | MS, 35mm, đứng yên | Vàng 8 (2/2/0/2/1/1) | Tách: 86a đặt ly (2s), 86b đi ra dừng ở cửa (4s) |
| 87 | 8s | B20 · lời dặn của Trang | Lưng Trang ở cửa: "Anh Minh… đừng vội đọc. Mẹ đã chờ thứ đó lâu lắm rồi." → đi ra | MCU lưng, 50mm, đứng yên | Xanh 5 (1/1/0/2/0/1) | Không thấy mặt: dễ, thoại thu riêng |
| 88 | 6s | B20 · một mình | Minh rút phong bì ra, nhìn, cất lại vào túi | CU, 85mm, đứng yên | Vàng 6 (2/1/0/2/1/0) | Kết thúc: phong bì đã vào túi |
| 89 | 5s | B20 · tắt đèn | Đèn ngủ tắt, chỉ còn ánh xanh cửa sổ; tiếng mưa ngừng | WS, 35mm, đứng yên | Xanh 2 (0/1/0/1/0/0) | Đổi ánh sáng trong một clip: làm khung đầu và khung cuối |

## Cảnh 7 · Sân sau, sáng hôm sau (7:18–7:41)

`loc_nha_sansau` · giếng nước, nắng xiên sớm · Minh: áo thun trắng cũ (đã cởi áo khoác), phong bì nâu

| # | Thời lượng | Beat · nhiệm vụ | Nội dung khung hình · diễn xuất (đầu → cuối) | Cỡ · góc · ống kính · máy | Rủi ro | Ghi chú tạo AI |
|---:|---:|---|---|---|---|---|
| 90 | 7s | B21 · gần mở | Minh đứng bên giếng, mở nắp phong bì, nhìn vào trong, không rút thư | MS, ngang mắt, 50mm, đứng yên | Vàng 7 (2/1/0/2/2/0) | — |
| 91 | 3s | B21 · tờ giấy | Tờ giấy học trò gấp đôi trong phong bì, mép mực tím | ECU chèn, 85mm, đứng yên | Xanh 0 (0/0/0/0/0/0) | Không cần chữ đọc được |
| 92 | 6s | B21 · Mẹ gọi | Điện thoại reo, Minh nghe (giọng Yến ngoài khung: "Mẹ tỉnh rồi…") | MCU, 50mm, đứng yên | Xanh 5 (1/1/0/2/0/1) | — |
| 93 | 7s | B21 · đi | Minh cất phong bì vào túi quần, đi ra phía cổng → ra khỏi khung, sân trống | WS, 35mm, đứng yên | Xanh 5 (1/1/0/2/1/0) | Cắt sang màn đen ở khung sân trống |

---

## Kiểm tra độ phủ và tổng kết

- **Số cảnh:** 93 cảnh (thêm khoảng 10 cảnh nếu tách theo ghi chú AI). Cộng thời lượng trong bảng được **7 phút 41 giây**. Kịch bản ước 10–11 phút, nên khoảng 2–3 phút còn lại phải đến từ nhịp nghỉ giữa các câu thoại và các khoảng giữ hình trước khi cắt. Khi dựng đo lại; nếu thiếu, kéo dài các cảnh không lời 20, 34, 50, 58, 75, 89, 93, đừng thêm thoại.
- **Rủi ro** (tính lại bằng script theo thang DirectorSKILL): 0 Đỏ · 36 Vàng · 57 Xanh. Vàng chủ yếu vì có 2–4 người trong khung hoặc có tay cầm, trao đạo cụ. Không cảnh nào có Tương tác 3 kèm một yếu tố 3 khác.
- **Chuyển động máy:** 4 cảnh (18, 43, 48, 80), đúng ngân sách.
- **Trục 180°:** cảnh 1 và 3: Minh luôn nhìn sang trái khung khi đối thoại với Nhung; cảnh 5: Minh trái, Trang phải, Nhung đầu bàn.
- **Đọc cột nội dung từ trên xuống:** câu chuyện vẫn hiểu được mà không cần thoại (về → gặp → mái hiên cãi nhau → cha chọn trường gà → nhà cũ → bữa cơm → phong bì → giữ bí mật).
- **Khung hình có chữ tiếng Việt (02, 42, 47, 72, 78, 79):** không tạo bằng AI; dùng đạo cụ thật hoặc đồ họa khi dựng.

## Thứ tự tạo cho AI (rủi ro thấp trước)

1. Keyframe bối cảnh trống cho 8 mã bối cảnh (dùng lại cho mọi tập).
2. Keyframe chân dung khóa nhận dạng từng nhân vật (`../nhan-vat-3d/prompt-anh-nhan-vat.md`).
3. Các cảnh Xanh, đặc biệt cận cảnh một người (12, 13, 21–24, 60, 61, 63, 64…).
4. Các cảnh Vàng có 1–2 người.
5. Cuối cùng là cảnh đông người: 08, 20, 28, 58. Nếu khó, quay thật hoặc dùng 3D.
