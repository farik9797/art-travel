#!/usr/bin/env python3
"""Собирает HTML-страницы макета Afsun из общих шаблонов.

Запуск из папки maket:  python3 src/build.py
Правки шапки, подвала и попапа делаются здесь один раз и попадают на все страницы.
Факты, которых нет в брифе и макете клиента, помечены классом .fill и словом «уточняется».
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(__file__).resolve().parent

PHONE, PHONE_TEL = "+998 71 123 45 67", "+998711234567"  # из макета клиента, не проверен
FILL = '<span class="fill">уточняется</span>'

# Названия отелей из макета; координаты условные.
HOTELS = [
    {"id": "registan", "name": "Afsun Hotel Registan", "short": "Registan", "img": "img/hotel-1.jpg", "ll": [39.6548, 66.9757]},
    {"id": "siyob", "name": "Afsun Hotel Siyob", "short": "Siyob", "img": "img/hotel-2.jpg", "ll": [39.6628, 66.9832]},
    {"id": "bukhara", "name": "Afsun Hotel Bukhara", "short": "Bukhara", "img": "img/hotel-3.jpg", "ll": [39.6505, 66.9640]},
    {"id": "afrosiyob", "name": "Afsun Hotel Afrosiyob", "short": "Afrosiyob", "img": "img/hotel-4.jpg", "ll": [39.6672, 66.9900]},
]
for h in HOTELS:
    h["url"] = f"hotel-{h['id']}.html"

ROOMS = [
    {"id": "standard", "name": "Стандартный номер", "plural": "Стандартные номера", "img": "img/room-standard.jpg",
     "lead": "Номер для одного или двух гостей. Подходит, если днём вы в городе, а в отель возвращаетесь отдохнуть."},
    {"id": "superior", "name": "Улучшенный номер", "plural": "Улучшенные номера", "img": "img/room-superior.jpg",
     "lead": "Номер повышенной категории для одного или двух гостей. Чем он отличается от стандартного в конкретном отеле, подскажет администратор."},
    {"id": "family", "name": "Семейный номер", "plural": "Семейные номера", "img": "img/room-family.jpg",
     "lead": "Номер для семьи с детьми или компании, которой удобнее жить вместе."},
    {"id": "suite", "name": "Люкс", "plural": "Люкс", "img": "img/room-suite.jpg",
     "lead": "Самая просторная категория номеров в наших отелях."},
]
for r in ROOMS:
    r["url"] = f"room-{r['id']}.html"

AMENITIES = [  # из брифа и макета клиента
    ("bed-double", "Уютные номера"), ("coffee", "Вкусный завтрак"), ("car", "Охраняемая парковка"),
    ("wifi", "Бесплатный Wi-Fi"), ("air-vent", "Кондиционер"), ("calendar-x", "Отмена до 18:00 дня заезда"),
]

CDN = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:wght@500;600&family=Manrope:wght@400;500;600;700&display=swap">"""
LEAFLET_CSS = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">'
LEAFLET_JS = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'
LIBS = """<script src="https://unpkg.com/lucide@0.468.0/dist/umd/lucide.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>"""

LOGO_SVG = '<svg viewBox="0 0 34 14" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M2 13V9c0-4 6.7-7.5 15-7.5S32 5 32 9v4"/><path d="M8 13V10c0-2.6 4-4.6 9-4.6s9 2 9 4.6v3"/></svg>'


def ic(name):
    return f'<i data-lucide="{name}"></i>'


def ph(src, alt="", lazy=True):
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return f'<div class="ph"><img src="{src}" alt="{alt}"{load} onerror="this.remove()"></div>'


def header(active):
    def cur(key):
        return ' aria-current="page"' if key == active else ""
    hotels_sub = "".join(f'<li><a href="{h["url"]}">{h["name"]}</a></li>' for h in HOTELS)
    rooms_sub = "".join(f'<li><a href="{r["url"]}">{r["plural"]}</a></li>' for r in ROOMS)
    return f"""<header class="hdr" id="hdr">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Afsun Hotels Group, на главную">{LOGO_SVG}<b>Afsun</b><small>HOTELS GROUP</small></a>
    <ul class="menu" id="menu">
      <li><a href="hotels.html"{cur('hotels')}>Отели {ic('chevron-down')}</a><ul class="sub">{hotels_sub}</ul></li>
      <li><a href="rooms.html"{cur('rooms')}>Номера {ic('chevron-down')}</a><ul class="sub">{rooms_sub}</ul></li>
      <li><a href="samarkand.html"{cur('samarkand')}>О Самарканде</a></li>
      <li><a href="services.html"{cur('services')}>Услуги</a></li>
      <li><a href="reviews.html"{cur('reviews')}>Отзывы</a></li>
      <li><a href="faq.html"{cur('faq')}>FAQ</a></li>
      <li><a href="contacts.html"{cur('contacts')}>Контакты</a></li>
    </ul>
    <div class="hdr__right">
      <div class="langs">{ic('globe')}<a href="#" lang="uz">UZ</a><a href="#" aria-current="true">RU</a><a href="#" lang="en">EN</a></div>
      <span class="sep" aria-hidden="true"></span>
      <span class="cur">UZS</span>
      <a class="phone" href="tel:{PHONE_TEL}" aria-label="Позвонить">{ic('phone')}<span>{PHONE}</span></a>
      <button class="burger" type="button" id="burger" aria-label="Меню" aria-expanded="false" aria-controls="menu">{ic('menu')}</button>
    </div>
  </div>
</header>"""


def footer():
    return f"""<footer class="foot" id="contacts-foot">
  <div class="wrap">
    <div class="foot__top">
      <a class="logo" href="index.html" aria-label="Afsun Hotels Group, на главную">{LOGO_SVG}<b>Afsun</b><small>HOTELS GROUP</small></a>
      <ul class="foot__links">
        <li><a href="hotels.html">Отели</a></li><li><a href="rooms.html">Номера</a></li><li><a href="samarkand.html">О Самарканде</a></li>
        <li><a href="services.html">Услуги</a></li><li><a href="faq.html">FAQ</a></li><li><a href="contacts.html">Контакты</a></li>
      </ul>
      <div class="socials">
        <a href="contacts.html" aria-label="Telegram">{ic('send')}</a>
        <a href="contacts.html" aria-label="Instagram">{ic('instagram')}</a>
        <a href="#" data-popup="callback" aria-label="Обратный звонок">{ic('phone-incoming')}</a>
      </div>
      <a class="phone" href="tel:{PHONE_TEL}">{ic('phone')}<span>{PHONE}</span></a>
    </div>
    <div class="foot__bottom">
      <span>© 2025 Afsun Hotels Group. Все права защищены.</span>
      <nav><a href="privacy.html">Политика конфиденциальности</a><a href="terms.html">Условия проживания</a><a href="offer.html">Публичная оферта</a></nav>
    </div>
  </div>
</footer>"""


def popup():
    return f"""<dialog class="modal" id="lead" aria-labelledby="leadTitle">
  <form class="lf" id="leadForm" data-mode="booking" data-endpoint="" novalidate>
    <button class="lead__close" type="button" id="leadClose" aria-label="Закрыть">{ic('x')}</button>
    <h2 id="leadTitle">Заявка на бронирование</h2>
    <p class="lead__sub" id="leadSub"></p>
    <div class="lead__row only-booking">
      <div class="fld"><label for="l-hotel">Отель</label><select id="l-hotel" name="hotel"><option value="">Любой из 4 отелей</option></select></div>
      <div class="fld"><label for="l-room">Номер</label><select id="l-room" name="room"><option value="">Подберите мне</option></select></div>
    </div>
    <div class="lead__row only-booking">
      <div class="fld"><label for="l-in">Заезд</label><input id="l-in" name="checkin" type="date"></div>
      <div class="fld"><label for="l-out">Выезд</label><input id="l-out" name="checkout" type="date"></div>
    </div>
    <div class="fld only-booking"><label for="l-guests">Гости</label><select id="l-guests" name="guests"><option>1 взрослый</option><option selected>2 взрослых</option><option>2 взрослых, 1 ребёнок</option><option>2 взрослых, 2 детей</option><option>3 взрослых</option><option>Больше 3 гостей</option></select></div>
    <div class="lead__row">
      <div class="fld"><label for="l-name">Имя</label><input id="l-name" name="name" type="text" autocomplete="name" required></div>
      <div class="fld"><label for="l-phone">Телефон</label><input id="l-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="+998 __ ___ __ __" required></div>
    </div>
    <div class="fld only-booking"><label for="l-msg">Комментарий</label><textarea id="l-msg" name="comment" placeholder="Например: поздний заезд, детская кроватка, трансфер"></textarea></div>
    <label class="check"><input type="checkbox" name="consent" required> <span>Согласен на обработку персональных данных по <a href="privacy.html" target="_blank">политике конфиденциальности</a></span></label>
    <button class="btn btn--fill" type="submit" id="leadSubmit">Отправить заявку</button>
    <p class="lead__note" id="leadNote" aria-live="polite"></p>
    <p class="lead__meta only-booking">{ic('shield-check')}Бесплатная отмена до 18:00 дня заезда</p>
  </form>
</dialog>"""


def layout(fname, title, desc, body, active="", map_=False):
    data = {"hotels": HOTELS, "rooms": [{"id": r["id"], "name": r["name"]} for r in ROOMS], "phone": PHONE, "phoneTel": PHONE_TEL}
    html = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{CDN}
{LEAFLET_CSS if map_ else ''}
<link rel="icon" href="data:,">
<link rel="stylesheet" href="assets/site.css">
</head>
<body class="no-js">
{header(active)}
<main id="top">
{body}
</main>
{footer()}
{popup()}
<script>window.AFSUN = {json.dumps(data, ensure_ascii=False)};</script>
{LEAFLET_JS if map_ else ''}
{LIBS}
<script src="assets/site.js"></script>
</body>
</html>
"""
    (ROOT / fname).write_text(html, encoding="utf-8")
    print("wrote", fname)


def crumbs(items):
    lis = []
    for label, href in items:
        lis.append(f'<li><a href="{href}">{label}</a></li>' if href else f'<li aria-current="page">{label}</li>')
    return f'<ol class="crumbs" aria-label="Навигация">{"".join(lis)}</ol>'


def phero(title, lead, crumb_items, img=None, actions=""):
    media = f'<div class="phero__media">{ph(img, "", lazy=False)}</div>' if img else ""
    cls = "phero" if img else "phero phero--plain"
    acts = f'<div class="phero__actions">{actions}</div>' if actions else ""
    return f"""<section class="{cls}">
  {media}
  <div class="wrap">
    {crumbs(crumb_items)}
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
    {acts}
  </div>
</section>"""


def btn_booking(text="Забронировать", hotel="", room="", cls="btn btn--fill"):
    attrs = (f' data-hotel="{hotel}"' if hotel else "") + (f' data-room="{room}"' if room else "")
    return f'<a class="{cls}" href="#" data-popup="booking"{attrs}>{text} {ic("arrow-right")}</a>'


def hcard(h):
    return f'<a class="hcard rv" href="{h["url"]}">{ph(h["img"], h["name"])}<span class="hcard__name">Afsun Hotel<br>{h["short"]}</span></a>'


def rcard(r):
    return f'<a class="rcard rv" href="{r["url"]}">{ph(r["img"], r["name"])}<div class="rcard__row"><span class="rcard__name">{r["plural"]}</span><span class="rcard__go">{ic("arrow-right")}</span></div></a>'


def chips(items):
    return '<ul class="chips">' + "".join(f"<li>{ic(i)}{t}</li>" for i, t in items) + "</ul>"


def info(icon, title, text):
    return f'<div class="info"><span class="info__ic">{ic(icon)}</span><div><h3>{title}</h3><p>{text}</p></div></div>'


HOME_TITLE = "Afsun Hotels Group — отели в самом сердце Самарканда"
HOME_DESC = "Четыре отеля Afsun в Самарканде: уютные номера, вкусный завтрак, охраняемая парковка и бронирование онлайн с бесплатной отменой до 18:00 дня заезда."


def page_home():
    body = (SRC / "home.html").read_text(encoding="utf-8")
    repl = {
        '<div class="cards4" id="hotelCards"></div>': '<div class="cards4">' + "".join(hcard(h) for h in HOTELS) + "</div>",
        '<ul class="hlist" id="hotelList"></ul>': '<ul class="hlist">' + "".join(
            f'<li><button type="button" data-focus="{h["id"]}" aria-pressed="false">{ph(h["img"])}{h["name"]}</button></li>' for h in HOTELS) + "</ul>",
        '<div class="map" id="map" role="region"': f'<div class="map" data-map="{",".join(h["id"] for h in HOTELS)}" role="region"',
        'href="#location">Все отели': 'href="hotels.html">Все отели',
        'href="#services">Узнать больше': 'href="services.html">Узнать больше',
        'href="#top">Все номера': 'href="rooms.html">Все номера',
        'href="#faq">Узнать больше': 'href="services.html#breakfast">Узнать больше',
        'href="#reviews">Читать все отзывы': 'href="reviews.html">Читать все отзывы',
        'href="#faq">Подробнее': 'href="terms.html">Подробнее',
        'href="#faq">Все вопросы': 'href="faq.html">Все вопросы',
    }
    for a, b in repl.items():
        assert a in body, a
        body = body.replace(a, b)
    for r in ROOMS:
        body = body.replace(f'<a class="rcard rv" href="#top"><div class="ph"><img src="{r["img"]}"', f'<a class="rcard rv" href="{r["url"]}"><div class="ph"><img src="{r["img"]}"')
    assert 'href="#top"><div class="ph"><img src="img/room' not in body
    layout("index.html", HOME_TITLE, HOME_DESC, body, "", map_=True)


def page_hotels():
    rows = []
    for h in HOTELS:
        rows.append(f"""<article class="hrow">
  <a class="hrow__img" href="{h['url']}">{ph(h['img'], h['name'])}</a>
  <div>
    <h2><a href="{h['url']}">{h['name']}</a></h2>
    <p>Самарканд, {FILL}</p>
    {chips([('coffee', 'Завтрак'), ('car', 'Парковка'), ('wifi', 'Wi-Fi')])}
    <div class="actions"><a class="btn" href="{h['url']}">Об отеле {ic('arrow-right')}</a>{btn_booking('Забронировать', h['id'])}</div>
  </div>
</article>""")
    body = phero("Отели Afsun в Самарканде",
                 "Четыре отеля в одном городе. Выберите тот, что ближе к вашим планам, или оставьте заявку, и мы подберём номер сами.",
                 [("Главная", "index.html"), ("Отели", None)], "img/hotel-2.jpg", btn_booking("Подобрать номер"))
    body += f"""
<section class="sec sec--l"><div class="wrap">{''.join(rows)}</div></section>
<section class="sec sec--l sec--band"><div class="wrap loc">
  <div class="shead"><h2>Все отели на карте</h2><p class="lead">Нажмите на название, чтобы найти отель на карте.</p></div>
  <div class="map" data-map="{','.join(h['id'] for h in HOTELS)}" role="region" aria-label="Карта отелей Afsun"></div>
  <ul class="hlist">{''.join(f'<li><button type="button" data-focus="{h["id"]}" aria-pressed="false">{ph(h["img"])}{h["name"]}</button></li>' for h in HOTELS)}</ul>
</div></section>"""
    layout("hotels.html", "Отели Afsun Hotels Group в Самарканде", "Четыре отеля Afsun в Самарканде: Registan, Siyob, Bukhara и Afrosiyob. Уютные номера, завтрак, охраняемая парковка и онлайн-бронирование.", body, "hotels", map_=True)


def page_hotel(h):
    others = [x for x in HOTELS if x["id"] != h["id"]]
    gal = "".join(f"<figure>{ph(src, alt)}</figure>" for src, alt in [
        (h["img"], f"{h['name']}, фасад"), ("img/room-standard.jpg", "Стандартный номер"), ("img/room-superior.jpg", "Улучшенный номер"),
        ("img/breakfast.jpg", "Завтрак"), ("img/room-family.jpg", "Семейный номер")])
    body = phero(h["name"], f"Отель Afsun Hotels Group в Самарканде. Адрес: {FILL}.",
                 [("Главная", "index.html"), ("Отели", "hotels.html"), (h["name"], None)], h["img"],
                 btn_booking("Забронировать", h["id"]) + f'<a class="btn" href="#map">На карте {ic("map-pin")}</a>')
    body += f"""
<section class="sec sec--l"><div class="wrap"><div class="gal">{gal}</div>
<p class="note">Фото временные, заменим на снимки отеля.</p></div></section>
<section class="sec sec--l"><div class="wrap room">
  <div>
    <div class="shead"><h2>Об отеле</h2></div>
    <div class="prose">
      <p>{h['name']} входит в Afsun Hotels Group. У нас уютные номера, вкусный завтрак и охраняемая парковка. Для нас сервис на первом месте: хотим, чтобы в Самарканде вам было спокойно, как дома.</p>
      <p>Бронь можно отменить бесплатно до 18:00 дня заезда.</p>
    </div>
    <div class="grid2" style="margin-top:22px">
      {''.join(info(i, t, '') for i, t in AMENITIES)}
    </div>
  </div>
  <aside class="side">
    <div class="cta"><h3>Свободные даты</h3><p>Оставьте даты и телефон, администратор проверит номера и перезвонит.</p>{btn_booking('Оставить заявку', h['id'], cls='btn btn--white')}</div>
    <table class="spec"><tbody>
      <tr><th>Адрес</th><td>Самарканд, {FILL}</td></tr>
      <tr><th>Номеров</th><td>{FILL}</td></tr>
      <tr><th>Заезд и выезд</th><td>{FILL}</td></tr>
      <tr><th>Отмена</th><td>Бесплатно до 18:00 дня заезда</td></tr>
    </tbody></table>
  </aside>
</div></section>
<section class="sec sec--l sec--band"><div class="wrap">
  <div class="shead"><h2>Номера</h2><p class="lead">Какие категории есть в этом отеле, уточнит администратор.</p></div>
  <div class="cards4">{''.join(rcard(r) for r in ROOMS)}</div>
</div></section>
<section class="sec sec--l" id="map"><div class="wrap">
  <div class="shead"><h2>Расположение</h2></div>
  <div class="map map--tall" data-map="{h['id']}" role="region" aria-label="{h['name']} на карте"></div>
  <p class="note">Точка на карте условная, поставим по точному адресу.</p>
</div></section>
<section class="sec sec--l"><div class="wrap">
  <div class="shead"><h2>Другие отели Afsun</h2></div>
  <div class="grid3">{''.join(hcard(x) for x in others)}</div>
</div></section>"""
    layout(h["url"], f"{h['name']} — отель в Самарканде | Afsun Hotels Group",
           f"{h['name']} в Самарканде: уютные номера, завтрак, охраняемая парковка, Wi-Fi. Бесплатная отмена до 18:00 дня заезда.",
           body, "hotels", map_=True)


def page_rooms():
    rows = []
    for r in ROOMS:
        rows.append(f"""<article class="hrow">
  <a class="hrow__img" href="{r['url']}">{ph(r['img'], r['name'])}</a>
  <div>
    <h2><a href="{r['url']}">{r['plural']}</a></h2>
    <p>{r['lead']}</p>
    {chips([('wifi', 'Wi-Fi'), ('air-vent', 'Кондиционер'), ('coffee', 'Завтрак')])}
    <div class="actions"><a class="btn" href="{r['url']}">Подробнее {ic('arrow-right')}</a>{btn_booking('Забронировать', room=r['id'])}</div>
  </div>
</article>""")
    body = phero("Номера в отелях Afsun",
                 "Четыре категории: от стандартного номера на двоих до люкса с гостиной. Цена зависит от отеля и дат, её назовёт администратор.",
                 [("Главная", "index.html"), ("Номера", None)], "img/room-superior.jpg", btn_booking("Подобрать номер"))
    body += f'<section class="sec sec--l"><div class="wrap">{"".join(rows)}</div></section>'
    layout("rooms.html", "Номера в отелях Afsun в Самарканде", "Стандартные, улучшенные и семейные номера и люкс в отелях Afsun Hotels Group в Самарканде. Бесплатная отмена до 18:00 дня заезда.", body, "rooms")


def page_room(r):
    others = [x for x in ROOMS if x["id"] != r["id"]]
    body = phero(r["plural"], r["lead"], [("Главная", "index.html"), ("Номера", "rooms.html"), (r["plural"], None)], r["img"],
                 btn_booking("Забронировать", room=r["id"]))
    body += f"""
<section class="sec sec--l"><div class="wrap room">
  <div>
    <div class="room__img">{ph(r['img'], r['name'])}</div>
    <p class="note">Фото временное, заменим на снимок номера.</p>
    <div class="shead" style="margin-top:28px"><h2>Что в номере</h2></div>
    <div class="grid2">
      {info('bed-double', 'Кровати', FILL)}
      {info('wifi', 'Wi-Fi', 'Бесплатный, во всех номерах')}
      {info('air-vent', 'Кондиционер', 'В номере')}
      {info('coffee', 'Завтрак', 'Условия завтрака уточнит администратор')}
    </div>
  </div>
  <aside class="side">
    <table class="spec"><tbody>
      <tr><th>Площадь</th><td>{FILL}</td></tr>
      <tr><th>Гостей</th><td>{FILL}</td></tr>
      <tr><th>Цена за ночь</th><td>по запросу</td></tr>
      <tr><th>Отмена</th><td>Бесплатно до 18:00 дня заезда</td></tr>
    </tbody></table>
    <div class="cta"><h3>Забронировать</h3><p>Выберите отель и даты, администратор подтвердит бронь.</p>{btn_booking('Оставить заявку', room=r['id'], cls='btn btn--white')}</div>
  </aside>
</div></section>
<section class="sec sec--l sec--band"><div class="wrap">
  <div class="shead"><h2>Другие номера</h2></div>
  <div class="grid3">{''.join(rcard(x) for x in others)}</div>
</div></section>"""
    layout(r["url"], f"{r['plural']} в Самарканде | Afsun Hotels Group",
           f"{r['plural']} в отелях Afsun в Самарканде: Wi-Fi, кондиционер, завтрак. Бесплатная отмена до 18:00 дня заезда.", body, "rooms")


SIGHTS = [
    ("Регистан", "img/hero.jpg", "Главная площадь Самарканда. Её окружают три медресе: Улугбека (XV век), Шердор и Тилля-Кари (XVII век). Вечером фасады подсвечивают, и площадь стоит увидеть дважды: днём и после заката.", ""),
    ("Гур-Эмир", "img/sight-gur-emir.jpg", "Мавзолей Амира Темура с ребристым бирюзовым куполом. Внутри много золота и резного оникса, поэтому сюда приходят даже те, кто уже насмотрелся на купола снаружи.", '<a href="https://commons.wikimedia.org/wiki/File:Gur-e_Amir_01.jpg">Bgag</a>, CC0'),
    ("Биби-Ханым", "img/sight-bibi-khanym.jpg", "Соборная мечеть, построенная по приказу Тимура на рубеже XIV и XV веков. Одна из самых больших мечетей своего времени.", '<a href="https://commons.wikimedia.org/wiki/File:Bibi-Khanym_Mosque,_Samarkand.jpg">Bgag</a>, CC0'),
    ("Шахи-Зинда", "img/sight-shah-i-zinda.jpg", "Улица мавзолеев на склоне холма Афрасиаб. Здесь собрана майолика разных веков, от светлой бирюзы до глубокого кобальта.", '<a href="https://commons.wikimedia.org/wiki/File:Shah-i-Zinda_02.jpg">Bgag</a>, CC0'),
    ("Сиабский базар", "img/sight-siyob.jpg", "Рынок рядом с мечетью Биби-Ханым. За самаркандской лепёшкой, сухофруктами и специями идут именно сюда.", '<a href="https://commons.wikimedia.org/wiki/File:Samarkand_naan_at_Siyob_Bazaar.jpg">Yoshi Canopus</a>, CC BY-SA 3.0'),
]


def page_samarkand():
    items = []
    for name, img, text, cred in SIGHTS:
        c = f'<p class="credit">Фото: {cred}, Wikimedia Commons</p>' if cred else ""
        items.append(f'<article class="sight"><div class="sight__img">{ph(img, name)}</div><div><h2>{name}</h2><p>{text}</p>{c}</div></article>')
    body = phero("О Самарканде", "Что посмотреть в городе, пока вы живёте в отеле Afsun.",
                 [("Главная", "index.html"), ("О Самарканде", None)], "img/hero.jpg")
    body += f"""<section class="sec sec--l"><div class="wrap">{''.join(items)}</div></section>
<section class="sec sec--l"><div class="wrap"><div class="terms">
  <div class="terms__img">{ph('img/arch.jpg')}</div>
  <span class="terms__ic">{ic('map')}</span>
  <div style="position:relative;z-index:1"><h2>Нужен трансфер или экскурсия?</h2><p>Напишите в заявке, администратор расскажет об условиях.</p></div>
  {btn_booking('Оставить заявку', cls='btn btn--white')}
</div></div></section>"""
    layout("samarkand.html", "Что посмотреть в Самарканде | Afsun Hotels Group", "Регистан, Гур-Эмир, Биби-Ханым, Шахи-Зинда и Сиабский базар: что посмотреть в Самарканде, пока вы живёте в отеле Afsun.", body, "samarkand")


def page_services():
    svc = [
        ("wifi", "Wi-Fi", "Бесплатный интернет в номерах."),
        ("car", "Парковка", "Охраняемая стоянка для гостей на машине."),
        ("air-vent", "Кондиционер", "В номерах, летом в Самарканде без него тяжело."),
        ("car-taxi-front", "Трансфер", "Поможем добраться до отеля. Условия и стоимость уточняйте у администратора."),
        ("landmark", "Экскурсии", "Поможем с экскурсией по городу. Подробности у администратора."),
        ("washing-machine", "Прачечная", "Постираем вещи, если вы в дороге надолго. Условия у администратора."),
    ]
    body = phero("Услуги и сервис", "Всё, что пригодится в поездке, можно попросить у администратора.",
                 [("Главная", "index.html"), ("Услуги", None)], "img/arch.jpg")
    body += f"""<section class="sec sec--l"><div class="wrap"><div class="grid3">{''.join(info(i, t, d) for i, t, d in svc)}</div></div></section>
<section class="sec sec--l" id="breakfast"><div class="wrap"><div class="bf">
  <div class="bf__photo">{ph('img/breakfast.jpg', 'Завтрак в отеле Afsun')}</div>
  <div class="bf__text">
    <div class="bf__tiles">{ph('img/arch.jpg')}</div>
    <p class="kicker">Вкусный завтрак</p>
    <h2>Завтрак — то, чем мы гордимся</h2>
    <p>Свежие продукты, разнообразное меню и уютная атмосфера. Время подачи и условия уточнит администратор.</p>
    {btn_booking('Забронировать', cls='btn btn--white')}
  </div>
</div></div></section>"""
    layout("services.html", "Услуги отелей Afsun в Самарканде", "Wi-Fi, охраняемая парковка, кондиционер, трансфер, экскурсии, прачечная и завтрак в отелях Afsun Hotels Group в Самарканде.", body, "services")


REVIEWS = [("AS", "Anna Smith", "США", "Отличный отель! Уютные номера, вкусный завтрак и внимательный персонал.", "Google"),
           ("MY", "Mehmet Yilmaz", "Турция", "Прекрасное расположение и сервис. Обязательно вернусь!", "Booking.com"),
           ("ИП", "Ирина Петрова", "Россия", "Очень понравилось пребывание в Самарканде!", "Google")]


def page_reviews():
    stars = "".join(ic("star") for _ in range(5))
    cards = "".join(f'<article class="rcv"><div class="rcv__head"><span class="ava">{a}</span><div><b>{n}</b><small>{c}</small></div></div><div class="stars">{stars}</div><p>{t}</p><span class="rcv__src">{s}</span></article>' for a, n, c, t, s in REVIEWS)
    body = phero("Отзывы гостей", "Что пишут о пребывании в Afsun Hotels Group.", [("Главная", "index.html"), ("Отзывы", None)], "img/breakfast.jpg")
    body += f"""<section class="sec sec--l"><div class="wrap">
  <div class="grid3">{cards}</div>
  <p class="sample" style="margin-top:14px">Образец из макета: перед запуском заменим на реальные отзывы гостей со ссылкой на Google и Booking.</p>
</div></section>
<section class="sec sec--l"><div class="wrap"><div class="terms">
  <div class="terms__img">{ph('img/arch.jpg')}</div>
  <span class="terms__ic">{ic('message-square-heart')}</span>
  <div style="position:relative;z-index:1"><h2>Жили у нас?</h2><p>Расскажите, что понравилось и что поправить. Мы читаем каждый отзыв.</p></div>
  <a class="btn btn--white" href="#" data-popup="callback">Связаться с нами {ic('arrow-right')}</a>
</div></div></section>"""
    layout("reviews.html", "Отзывы гостей Afsun Hotels Group", "Отзывы гостей об отелях Afsun Hotels Group в Самарканде.", body, "reviews")


FAQ = [
    ("Как отменить бронирование?", "Бронь можно отменить бесплатно до 18:00 дня заезда. Напишите или позвоните администратору отеля."),
    ("Как оплатить проживание?", "Онлайн картой при бронировании. Какие карты принимаем, уточняется."),
    ("Во сколько начинается заселение?", "Время заезда и выезда уточняется у отеля."),
    ("Есть ли парковка?", "Да, у нас охраняемая парковка для гостей на машине."),
    ("Входит ли завтрак?", "Завтрак готовим в отелях. Условия уточнит администратор при бронировании."),
    ("Предоставляется ли трансфер?", "Да, трансфер есть в списке наших услуг. Условия и стоимость уточняйте у администратора."),
    ("Можно ли разместиться с детьми?", "Да. Для семей с детьми есть семейные номера."),
    ("Есть ли Wi-Fi?", "Да, бесплатный Wi-Fi есть в номерах."),
]


def page_faq():
    qa = "".join(f'<details><summary>{q} {ic("plus")}</summary><p>{a}</p></details>' for q, a in FAQ)
    body = phero("Часто задаваемые вопросы", "Не нашли ответ? Оставьте номер, и мы перезвоним.", [("Главная", "index.html"), ("FAQ", None)], "img/dome.jpg",
                 f'<a class="btn btn--fill" href="#" data-popup="callback">Задать вопрос {ic("arrow-right")}</a>')
    body += f'<section class="sec sec--l"><div class="wrap"><div class="qa" style="max-width:860px">{qa}</div></div></section>'
    layout("faq.html", "Вопросы и ответы | Afsun Hotels Group", "Отмена брони, оплата, заселение, парковка, завтрак, трансфер, дети: ответы на частые вопросы гостей отелей Afsun в Самарканде.", body, "faq")


def page_contacts():
    cards = "".join(f'<div class="contact"><h3>{h["name"]}</h3><p>{ic("map-pin")}Самарканд, {FILL}</p><p>{ic("phone")}<a href="tel:{PHONE_TEL}">{PHONE}</a></p><div class="actions"><button class="btn" type="button" data-focus="{h["id"]}">На карте</button>{btn_booking("Забронировать", h["id"])}</div></div>' for h in HOTELS)
    body = phero("Контакты", f"Звоните: <a href=\"tel:{PHONE_TEL}\"><b>{PHONE}</b></a>. Или оставьте номер, и мы перезвоним.",
                 [("Главная", "index.html"), ("Контакты", None)], "img/hotel-1.jpg",
                 f'<a class="btn btn--fill" href="#" data-popup="callback">Заказать звонок {ic("phone-incoming")}</a>' + btn_booking("Забронировать", cls="btn"))
    body += f"""<section class="sec sec--l"><div class="wrap">
  <div class="grid2">{cards}</div>
  <div class="map map--tall" data-map="{','.join(h['id'] for h in HOTELS)}" role="region" aria-label="Отели Afsun на карте" style="margin-top:22px"></div>
  <p class="note">Точки на карте условные, поставим по точным адресам.</p>
</div></section>"""
    layout("contacts.html", "Контакты Afsun Hotels Group в Самарканде", "Телефон и адреса отелей Afsun Hotels Group в Самарканде. Заявка на бронирование и обратный звонок.", body, "contacts", map_=True)


def page_doc(fname, title, lead, sections, desc):
    secs = "".join(f"<section><h2>{h}</h2>{t}</section>" for h, t in sections)
    body = phero(title, lead, [("Главная", "index.html"), (title, None)])
    body += f'<section class="sec sec--l"><div class="wrap"><div class="prose doc">{secs}</div></div></section>'
    layout(fname, f"{title} | Afsun Hotels Group", desc, body)


def page_docs():
    page_doc("terms.html", "Условия проживания", "Правила бронирования, оплаты и отмены в отелях Afsun.", [
        ("Бронирование", "<p>Номер можно забронировать на сайте или по телефону. Бронь подтверждает администратор.</p>"),
        ("Оплата", "<p>Оплата онлайн картой при бронировании. Способы оплаты и валюта уточняются.</p>"),
        ("Отмена", "<p>Бронь можно отменить бесплатно до 18:00 дня заезда. Условия возврата при более поздней отмене уточняются.</p>"),
        ("Заезд и выезд", f"<p>Время заезда: {FILL}. Время выезда: {FILL}.</p>"),
        ("Документы", "<p>При заселении нужен паспорт. Регистрацию иностранных гостей оформляет отель.</p>"),
    ], "Условия бронирования, оплаты и бесплатной отмены до 18:00 дня заезда в отелях Afsun Hotels Group.")
    page_doc("offer.html", "Публичная оферта", "Текст оферты готовит юрист клиента. Ниже структура документа.", [
        ("1. Общие положения", f"<p>Исполнитель: {FILL}. ИНН, адрес и банковские реквизиты: {FILL}.</p>"),
        ("2. Предмет договора", "<p>Услуги временного размещения в отелях Afsun Hotels Group в Самарканде.</p>"),
        ("3. Бронирование и оплата", f"<p>{FILL}</p>"),
        ("4. Отмена и возврат", "<p>Бесплатная отмена до 18:00 дня заезда. Остальные условия: " + FILL + ".</p>"),
        ("5. Ответственность сторон", f"<p>{FILL}</p>"),
    ], "Публичная оферта на услуги размещения в отелях Afsun Hotels Group.")
    page_doc("privacy.html", "Политика конфиденциальности", "Как мы обращаемся с данными, которые вы оставляете в форме заявки.", [
        ("Какие данные собираем", "<p>Имя, телефон, даты поездки и комментарий из формы заявки.</p>"),
        ("Зачем", "<p>Чтобы подтвердить бронь и связаться с вами по поводу проживания.</p>"),
        ("Кто оператор данных", f"<p>{FILL}</p>"),
        ("Как отозвать согласие", f"<p>Позвоните по телефону <a href=\"tel:{PHONE_TEL}\">{PHONE}</a> или напишите на {FILL}.</p>"),
    ], "Политика конфиденциальности сайта Afsun Hotels Group.")


if __name__ == "__main__":
    page_home(); page_hotels(); [page_hotel(h) for h in HOTELS]
    page_rooms(); [page_room(r) for r in ROOMS]
    page_samarkand(); page_services(); page_reviews(); page_faq(); page_contacts(); page_docs()
