export type Brand = {
  name: string; // tên kênh
  tagline?: string; // dòng phụ dưới logo ở intro
  logo: string; // file trong public/
  sting: string; // âm thanh intro trong public/ (tiếng "hit" đặt ở `impact`)
  bg: string;
  fg: string;
  accent: string;
  cta?: string; // lời kêu gọi ở outro
};

export type IntroProps = {brand: Brand; impact: number}; // impact: giây của tiếng hit trong sting
export type OutroProps = {brand: Brand; showGuides: boolean};

export type Caption = {start: number; end: number; text: string};
export type AudiogramProps = {
  audio: string; // file trong public/, đã cắt còn ≤ 90 s
  title: string;
  show?: string;
  cover?: string;
  look: "bars" | "wave";
  durationInSeconds: number;
  bg: string;
  fg: string;
  accent: string;
  captions: Caption[];
};
