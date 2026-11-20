/* Afsun Hotels Group — общий скрипт всех страниц макета */
(() => {
  document.body.classList.remove('no-js');
  const D = window.AFSUN || { hotels: [], rooms: [], phone: '' };
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (window.lucide) lucide.createIcons();

  /* ---------- Header ---------- */
  const hdr = $('#hdr'), burger = $('#burger'), menu = $('#menu');
  const stuckAt = $('.hero') ? 520 : 260;
  const onScroll = () => hdr.classList.toggle('stuck', scrollY > stuckAt);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  burger.addEventListener('click', () => { const o = menu.classList.toggle('open'); burger.setAttribute('aria-expanded', o); });
  menu.addEventListener('click', (e) => { if (e.target.closest('a')) { menu.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); } });

  const vid = $('#heroVideo');
  if (vid && reduceMotion) { vid.removeAttribute('autoplay'); vid.pause(); }

  /* ---------- Popup form ---------- */
  const dlg = $('#lead'), form = $('#leadForm'), note = $('#leadNote');
  const f = (n) => form.elements[n];
  const today = new Date().toISOString().slice(0, 10);
  let lenis = null;

  D.hotels.forEach((h) => f('hotel').add(new Option(h.name, h.id)));
  D.rooms.forEach((r) => f('room').add(new Option(r.name, r.id)));
  f('checkin').min = today; f('checkout').min = today;
  f('checkin').addEventListener('change', () => { f('checkout').min = f('checkin').value || today; if (f('checkout').value && f('checkout').value <= f('checkin').value) f('checkout').value = ''; });

  const MODES = {
    booking: { title: 'Заявка на бронирование', sub: 'Оставьте даты и контакты. Администратор проверит свободные номера и свяжется с вами.', btn: 'Отправить заявку' },
    callback: { title: 'Обратный звонок', sub: 'Оставьте номер телефона, и мы перезвоним.', btn: 'Жду звонка' },
  };
  function openLead(mode = 'booking', preset = {}) {
    const m = MODES[mode] || MODES.booking;
    form.dataset.mode = mode;
    $('#leadTitle').textContent = m.title; $('#leadSub').textContent = m.sub; $('#leadSubmit').textContent = m.btn;
    note.textContent = ''; note.className = 'lead__note';
    ['hotel', 'room', 'checkin', 'checkout', 'guests'].forEach((k) => { if (preset[k] !== undefined) f(k).value = preset[k]; });
    $$('[aria-invalid]', form).forEach((el) => el.removeAttribute('aria-invalid'));
    dlg.showModal(); document.documentElement.classList.add('modal-open');
    if (lenis) lenis.stop();
    setTimeout(() => (mode === 'callback' ? f('name') : (f('checkin').value ? f('name') : f('checkin'))).focus(), 60);
  }
  const closeLead = () => dlg.close();
  dlg.addEventListener('close', () => { document.documentElement.classList.remove('modal-open'); if (lenis) lenis.start(); });
  dlg.addEventListener('click', (e) => { if (e.target === dlg) closeLead(); });
  $('#leadClose').addEventListener('click', closeLead);
  document.addEventListener('click', (e) => {
    const t = e.target.closest('[data-popup]'); if (!t) return;
    e.preventDefault();
    openLead(t.dataset.popup, { hotel: t.dataset.hotel, room: t.dataset.room });
  });

  // phone mask: +998 XX XXX XX XX
  f('phone').addEventListener('input', (e) => {
    let d = e.target.value.replace(/\D/g, ''); if (!d.startsWith('998')) d = '998' + d.replace(/^998/, '');
    d = d.slice(0, 12);
    const p = [d.slice(0, 3), d.slice(3, 5), d.slice(5, 8), d.slice(8, 10), d.slice(10, 12)].filter(Boolean);
    e.target.value = '+' + p.join(' ');
  });
  f('phone').addEventListener('focus', (e) => { if (!e.target.value) e.target.value = '+998 '; });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const booking = form.dataset.mode !== 'callback';
    const bad = (el, msg) => { el.setAttribute('aria-invalid', 'true'); note.textContent = msg; note.className = 'lead__note is-error'; el.focus(); };
    $$('[aria-invalid]', form).forEach((el) => el.removeAttribute('aria-invalid'));
    if (booking && !f('checkin').value) return bad(f('checkin'), 'Выберите дату заезда.');
    if (booking && !f('checkout').value) return bad(f('checkout'), 'Выберите дату выезда.');
    if (!f('name').value.trim()) return bad(f('name'), 'Напишите, как к вам обращаться.');
    if (f('phone').value.replace(/\D/g, '').length < 12) return bad(f('phone'), 'Проверьте номер: нужен формат +998 XX XXX XX XX.');
    if (!f('consent').checked) return bad(f('consent'), 'Нужно согласие на обработку персональных данных.');
    if (!form.dataset.endpoint) {
      note.innerHTML = `Заявка не отправлена: форма пока не подключена. Позвоните нам: <a href="tel:${D.phoneTel}">${D.phone}</a>.`;
      note.className = 'lead__note is-warn'; return;
    }
    fetch(form.dataset.endpoint, { method: 'POST', body: new FormData(form) })
      .then((r) => { note.textContent = r.ok ? 'Заявка отправлена. Администратор свяжется с вами.' : 'Не получилось отправить. Позвоните нам.'; note.className = 'lead__note ' + (r.ok ? 'is-ok' : 'is-error'); })
      .catch(() => { note.textContent = 'Не получилось отправить. Позвоните нам.'; note.className = 'lead__note is-error'; });
  });

  /* ---------- Search on the home page: opens the booking form ---------- */
  const search = $('#search');
  if (search) {
    const sIn = $('#s-in'), sOut = $('#s-out'), sHotel = $('#s-hotel');
    D.hotels.forEach((h) => sHotel.add(new Option(h.name, h.id)));
    sIn.min = today; sOut.min = today;
    sIn.addEventListener('change', () => { sOut.min = sIn.value || today; if (sOut.value && sOut.value <= sIn.value) sOut.value = ''; });
    search.addEventListener('submit', (e) => {
      e.preventDefault();
      openLead('booking', { hotel: sHotel.value, checkin: sIn.value, checkout: sOut.value, guests: $('#s-guests').value });
    });
  }

  /* ---------- Maps ---------- */
  $$('[data-map]').forEach((el) => {
    if (!window.L) return;
    const ids = el.dataset.map.split(',');
    const list = D.hotels.filter((h) => ids.includes(h.id));
    const map = L.map(el, { scrollWheelZoom: false }).setView(list.length === 1 ? list[0].ll : [39.6585, 66.977], list.length === 1 ? 15 : 14);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '&copy; OpenStreetMap' }).addTo(map);
    const icon = L.divIcon({ className: 'drop', html: '<svg width="26" height="34" viewBox="0 0 26 34"><path d="M13 0C5.8 0 0 5.6 0 12.6 0 22 13 34 13 34s13-12 13-21.4C26 5.6 20.2 0 13 0z" fill="#134a57"/><circle cx="13" cy="12.5" r="4.5" fill="#fff"/></svg>', iconSize: [26, 34], iconAnchor: [13, 34], popupAnchor: [0, -30] });
    const markers = {};
    list.forEach((h) => { markers[h.id] = L.marker(h.ll, { icon }).addTo(map).bindPopup(`<a class="pin" href="${h.url}"><img src="${h.img}" alt="" onerror="this.remove()">${h.name}</a>`, { closeButton: false }); });
    if (list[0]) markers[list[0].id].openPopup();
    const scope = el.closest('section') || document;
    $$('[data-focus]', scope).forEach((b) => b.addEventListener('click', () => {
      $$('[data-focus]', scope).forEach((x) => x.setAttribute('aria-pressed', x === b));
      const m = markers[b.dataset.focus]; if (!m) return;
      map.flyTo(m.getLatLng(), 15, { duration: .8 }); m.openPopup();
    }));
  });

  /* ---------- Reviews slider ---------- */
  const track = $('#revTrack');
  if (track) $$('.arrow').forEach((b) => b.addEventListener('click', () => track.scrollBy({ left: +b.dataset.dir * track.clientWidth / 3, behavior: 'smooth' })));

  /* ---------- Motion: Lenis + GSAP ScrollTrigger ---------- */
  const SHAPES = 'path, circle, rect, line, polyline, polygon, ellipse';
  const prepDraw = (svg) => svg && svg.querySelectorAll(SHAPES).forEach((s) => { s.setAttribute('pathLength', '1'); s.style.strokeDasharray = '1'; s.style.strokeDashoffset = '1'; });
  const draw = (svg, delay = 0) => svg && gsap.fromTo(svg.querySelectorAll(SHAPES), { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1, ease: 'power2.inOut', stagger: .08, delay, overwrite: true });
  const has = (s) => document.querySelector(s);
  const CLEAR = { clearProps: 'transform,opacity' };

  if (reduceMotion || !window.gsap || !window.ScrollTrigger || !window.Lenis) {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .12 });
    $$('.rv').forEach((el, i) => { el.style.transitionDelay = `${(i % 4) * 70}ms`; io.observe(el); });
    return;
  }

  document.documentElement.classList.add('gsap');
  gsap.registerPlugin(ScrollTrigger);
  lenis = new Lenis({ duration: 1.15, easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((t) => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
  $$('a[href^="#"]').forEach((a) => a.addEventListener('click', (e) => {
    const id = a.getAttribute('href'); if (id.length < 2) return;
    const t = $(id); if (!t) return;
    e.preventDefault(); lenis.scrollTo(id === '#top' ? 0 : t, { offset: -100, duration: 1.4 });
  }));
  if (location.hash && $(location.hash)) setTimeout(() => lenis.scrollTo($(location.hash), { offset: -100, immediate: true }), 50);

  $$('.feat__ic svg, .tile svg, .terms__ic svg, .badge svg, .sf > svg, .info__ic svg').forEach(prepDraw);

  // Intro
  const intro = gsap.timeline({ defaults: { ease: 'power3.out', ...CLEAR } })
    .from('.hdr .logo, .hdr .menu > li, .hdr__right > *', { y: -18, opacity: 0, duration: .7, stagger: .05 });
  if (has('.hero')) {
    intro.from('.hero h1', { y: 46, opacity: 0, duration: 1.1 }, '-=.45')
      .from('.hero .lead', { y: 26, opacity: 0, duration: .9 }, '-=.75')
      .from('.hero__bar', { y: 50, opacity: 0, duration: 1 }, '-=.6')
      .from('.search .sf, .search .btn', { y: 16, opacity: 0, duration: .6, stagger: .07 }, '-=.65')
      .add(() => $$('.sf > svg').forEach((s, i) => draw(s, i * .08)), '-=.5')
      .from('.badge', { x: 24, opacity: 0, duration: .7 }, '-=.6')
      .add(() => draw($('.badge svg')), '-=.4');
    gsap.to('.hero__media', { yPercent: 16, scale: 1.08, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to('.hero .wrap', { yPercent: -18, opacity: .2, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'center top', end: 'bottom top', scrub: true } });
  }
  if (has('.phero')) {
    intro.from('.crumbs, .phero h1, .phero .lead, .phero__actions', { y: 30, opacity: 0, duration: .9, stagger: .09 }, '-=.4');
    if (has('.phero__media img')) gsap.to('.phero__media img', { yPercent: 12, scale: 1.1, ease: 'none', scrollTrigger: { trigger: '.phero', start: 'top top', end: 'bottom top', scrub: true } });
  }

  // Section heads
  $$('.split > .rv:first-child, .loc > .rv:first-child, .rev > .rv:first-child, .shead').forEach((el) => {
    gsap.from(el.children, { y: 32, opacity: 0, duration: .95, stagger: .09, ease: 'power3.out', ...CLEAR, scrollTrigger: { trigger: el, start: 'top 85%' } });
  });

  // Items rise in batches
  const items = '.hcard, .rcard, .feat, .tile, .rcv, .qa details, .hlist li, .sight, .info, .spec tr, .gal figure, .doc section, .hrow, .contact';
  const all = $$(items);
  if (all.length) {
    gsap.set(all, { y: 44, opacity: 0 });
    ScrollTrigger.batch(all, {
      start: 'top 90%', end: 'max', once: true,
      onEnter: (b) => gsap.to(b, { y: 0, opacity: 1, duration: .9, stagger: .09, ease: 'power3.out', overwrite: true, clearProps: 'transform',
        onStart: () => b.forEach((el, i) => { const s = el.querySelector('.feat__ic svg, .info__ic svg, :scope > svg'); if (s) draw(s, .25 + i * .09); }) }),
    });
    const reveal = () => all.forEach((el) => {
      if (gsap.getProperty(el, 'opacity') < 1 && !gsap.isTweening(el) && el.getBoundingClientRect().top < innerHeight) gsap.to(el, { y: 0, opacity: 1, duration: .6, ease: 'power2.out', clearProps: 'transform' });
    });
    lenis.on('scroll', () => { clearTimeout(window.__rv); window.__rv = setTimeout(reveal, 180); });
  }
  $$('.feat, .tile, .info').forEach((el) => el.addEventListener('mouseenter', () => draw(el.querySelector('svg'))));

  if (has('.bf')) {
    gsap.from('.bf', { clipPath: 'inset(0 12% 0 12% round 20px)', opacity: 0, duration: 1.2, ease: 'power3.out', ...CLEAR, scrollTrigger: { trigger: '.bf', start: 'top 85%' } });
    gsap.fromTo('.bf__photo img', { yPercent: -6, scale: 1.12 }, { yPercent: 6, scale: 1.12, ease: 'none', scrollTrigger: { trigger: '.bf', start: 'top bottom', end: 'bottom top', scrub: true } });
    gsap.from('.bf__text > :not(.bf__tiles)', { x: 30, opacity: 0, duration: .9, stagger: .08, ease: 'power3.out', ...CLEAR, scrollTrigger: { trigger: '.bf', start: 'top 75%' } });
  }
  $$('.why__deco img, .svc__deco img, .faq__deco img, .terms__img img, .bf__tiles img').forEach((img) => {
    gsap.fromTo(img, { yPercent: -8, scale: 1.18 }, { yPercent: 8, scale: 1.18, ease: 'none', scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  $$('.map').forEach((m) => gsap.from(m, { y: 40, opacity: 0, scale: .97, duration: 1, ease: 'power3.out', ...CLEAR, scrollTrigger: { trigger: m, start: 'top 88%', onEnter: () => {
    $$('.leaflet-marker-icon.drop', m).forEach((p, i) => { p.style.setProperty('--d', `${.3 + i * .12}s`); p.classList.remove('drop'); void p.offsetWidth; p.classList.add('drop'); });
  } } }));
  if (has('.terms')) gsap.from('.terms', { y: 50, opacity: 0, duration: 1, ease: 'power3.out', ...CLEAR, scrollTrigger: { trigger: '.terms', start: 'top 88%', onEnter: () => draw($('.terms__ic svg'), .3) } });
  gsap.from('.foot__top > *', { y: 24, opacity: 0, duration: .8, stagger: .08, ease: 'power3.out', ...CLEAR, scrollTrigger: { trigger: '.foot', start: 'top 92%' } });
  addEventListener('load', () => ScrollTrigger.refresh());
})();
