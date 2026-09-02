// 目的別マップの一覧。ここに項目を足す/減らす/文言を変えるだけで、
// LP（index.html）とマップ（local_map.html）の両方に反映されます。
//
// image: LPのボタン背景に使う写真。docs/images/ に置いたファイルを指定します
//        （例: images/magochi.jpeg）。無い場合は color の色だけが表示されます。
// color: 写真が無いとき／写真の上に重ねる色み（各魚種のイメージカラー）。
const FISHING_MAPS = [
  { id: 'magochi',  label: 'マゴチの釣りマップ',     desc: '砂地の底べったり。ハゼの泳がせやワームのズル引きで狙う。',       image: 'images/magochi.jpeg',  color: '#b7893f' },
  { id: 'koshodai', label: 'コショウダイの釣りマップ', desc: '大きめのイソメ・カニ餌で、夜の底を待つ大物。',                   image: 'images/koshodai.jpeg', color: '#5f6b7a' },
  { id: 'kijihata', label: 'キジハタの釣りマップ',   desc: '根の際を狙う高級魚。ワームやブラクリを穴へ落とし込む。',         image: 'images/kijihata.jpeg', color: '#a8482f' },
  { id: 'mebaru',   label: 'メバルの釣りマップ',     desc: '夜の常夜灯まわりや藻場。軽いジグ単のワームをゆっくり漂わせる。', image: 'images/mebaru.jpeg',   color: '#3f5a63' },
  { id: 'mejina',   label: 'メジナの釣りマップ',     desc: '磯際のサラシや潮目。オキアミ餌のフカセでウキを送り込む。',       image: 'images/mejina.jpeg',   color: '#2f5d4a' },
  { id: 'aji',      label: 'アジの釣りマップ',       desc: '回遊待ちの堤防。サビキやアジングのワームを表層〜中層で。',       image: 'images/aji.jpeg',      color: '#5b7f96' },
  { id: 'kurodai',  label: 'クロダイの釣りマップ',   desc: '堤防やゴロタの底。カニ・イガイ餌の落とし込みやヘチ釣りで。',     image: 'images/kurodai.jpeg',  color: '#4a4f57' },
  { id: 'suzuki',   label: 'スズキの釣りマップ',     desc: '河口や橋脚の流れ。ミノーやバイブレーションでヨレを通す。',       image: 'images/suzuki.jpeg',   color: '#6b7d88' },
  { id: 'tachiuo',  label: 'タチウオの釣りマップ',   desc: '夕まづめの沖向き。キビナゴ餌のウキ釣りやワインドで誘う。',       image: 'images/tachiuo.jpeg',  color: '#8a8f99' },
];
