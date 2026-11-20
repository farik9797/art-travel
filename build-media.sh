#!/bin/bash
# Сжимает исходники из Flow в файлы, которые ждёт страница.
# Запуск: bash build-media.sh (из maket). Соответствие задаётся в map.txt:
#   <файл страницы> <ширина> <исходник>      например: img/hotel-1.jpg 1000 ../../assets-src/flow/xxx.jpg
#   video/hero.mp4 1920 <исходник видео>     (заодно делает постер img/hero.jpg)
set -euo pipefail
cd "$(dirname "$0")"
while read -r out w src; do src="${src%$'\r'}"
  [[ -z "${out:-}" || "$out" == \#* ]] && continue
  mkdir -p "$(dirname "$out")"
  case "$out" in
    *.mp4)
      ffmpeg -nostdin -y -loglevel error -i "$src" -an -vf "scale='min($w,iw)':-2" -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -movflags +faststart "$out"
      ffmpeg -nostdin -y -loglevel error -i "$src" -vframes 1 -vf "scale='min($w,iw)':-2" -q:v 3 img/hero.jpg ;;
    *.jpg)
      sips -s format jpeg -s formatOptions 78 --resampleWidth "$w" "$src" --out "$out" >/dev/null ;;
  esac
  printf "%-24s %6s KB\n" "$out" "$(( $(stat -f%z "$out") / 1024 ))"
done < map.txt
