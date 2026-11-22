// Be Vietnam Pro: đủ dấu tiếng Việt. Tải từ Google Fonts lúc render, Remotion chờ font xong mới chụp khung.
import {loadFont} from "@remotion/google-fonts/BeVietnamPro";

export const {fontFamily} = loadFont("normal", {
  weights: ["500", "700", "900"],
  subsets: ["latin", "latin-ext", "vietnamese"],
});
