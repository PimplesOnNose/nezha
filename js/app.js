/**
 * 哪吒闹海 — Nezha Conquers the Dragon King
 * Application Logic — Dark Silk / Gongbi Heavy-Colour UI
 */
(function () {
  'use strict';

  // ── State ──────────────────────────────────────────────
  const state = {
    lang: 'zh',
    started: false,
    heroDismissed: false,
    currentChapter: 0,
    totalChapters: STORY.chapters.length,
    isPlaying: false,
    autoPlay: false,
    currentAudioChapter: -1
  };

  // ── DOM refs ───────────────────────────────────────────
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

  const hero           = $('#hero');
  const beginBtn       = $('#begin-btn');
  const header         = $('#header');
  const chapterTray    = $('#chapterTray');
  const tideProgress   = $('#tideProgress');
  const tideBar        = $('#tideBar');
  const storyEl        = $('#story');
  const audioPlayer    = $('#audioPlayer');
  const prevBtn        = $('#prevBtn');
  const nextBtn        = $('#nextBtn');
  const langEn         = $('#langEn');
  const langZh         = $('#langZh');
  const autoplayBtn    = $('#autoplayBtn');
  const moondialLabelZh = $('#moondialLabelZh');
  const moondialLabelEn = $('#moondialLabelEn');
  const moondialPlay   = $('#moondialPlay');
  const moondialBand   = $('#moondialBand');
  const moondialFill   = $('#moondialFill');
  const moondialCursor = $('#moondialCursor');
  const moondialTime   = $('#moondialTime');
  const particlesLayer = $('#particlesLayer');

  // ── Helpers ────────────────────────────────────────────
  const CN_NUM = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九'];

  // ── Rising Embers + Falling Petals Particles ───────────
  function spawnEmber() {
    if (!particlesLayer) return;
    const el = document.createElement('div');
    const x = Math.random() * 100;
    const dur = 4 + Math.random() * 5;
    const size = 1.5 + Math.random() * 2.5;
    const drift = (Math.random() - 0.5) * 40;
    el.className = 'particle particle--ember';
    el.style.cssText = `
      left: ${x}%; bottom: -10px;
      width: ${size}px; height: ${size}px;
      transform: translateX(${drift}px);
      animation: emberRise ${dur}s ease-in forwards;
    `;
    particlesLayer.appendChild(el);
    setTimeout(() => el.remove(), dur * 1000);
  }

  function spawnPetal() {
    if (!particlesLayer) return;
    const el = document.createElement('div');
    const x = Math.random() * 100;
    const dur = 5 + Math.random() * 6;
    const size = 3 + Math.random() * 4;
    const drift = (Math.random() - 0.5) * 30;
    const rot = Math.random() * 360;
    el.className = 'particle particle--petal';
    el.style.cssText = `
      left: ${x}%; top: -10px;
      width: ${size}px; height: ${size * 0.6}px;
      transform: translateX(${drift}px) rotate(${rot}deg);
      animation: petalFall ${dur}s ease-in forwards;
    `;
    particlesLayer.appendChild(el);
    setTimeout(() => el.remove(), dur * 1000);
  }

  // inject particle keyframes once
  (function injectParticleKeyframes() {
    const style = document.createElement('style');
    style.textContent = `
      .particle--ember {
        position: absolute;
        background: var(--cinnabar);
        border-radius: 50%;
        opacity: 0;
        box-shadow: 0 0 4px var(--cinnabar-glow);
        pointer-events: none;
      }
      .particle--petal {
        position: absolute;
        background: var(--lotus-pink);
        border-radius: 50% 0 50% 0;
        opacity: 0;
        pointer-events: none;
      }
      @keyframes emberRise {
        0%   { opacity: 0; transform: translateY(0) scale(0); }
        15%  { opacity: 0.4; }
        50%  { opacity: 0.2; }
        85%  { opacity: 0.08; }
        100% { opacity: 0; transform: translateY(-100vh) scale(0.3); }
      }
      @keyframes petalFall {
        0%   { opacity: 0; transform: translateY(0) rotate(0deg) scale(0); }
        15%  { opacity: 0.25; }
        50%  { opacity: 0.15; }
        85%  { opacity: 0.06; }
        100% { opacity: 0; transform: translateY(100vh) rotate(360deg) scale(0.4); }
      }
    `;
    document.head.appendChild(style);
  })();

  let particleInterval;
  function startParticles() {
    spawnEmber();
    spawnPetal();
    particleInterval = setInterval(() => {
      spawnEmber();
      spawnPetal();
    }, 1600);
  }

  // ── Chapter rendering ─────────────────────────────────
  function renderChapters() {
    storyEl.innerHTML = '';

    STORY.chapters.forEach((ch, idx) => {
      const article = document.createElement('article');
      article.className = `story-chapter${idx === 0 ? ' active' : ''}`;
      article.dataset.chapter = ch.id;

      const numCN = CN_NUM[ch.id] || String(ch.id);

      article.innerHTML = `
        <div class="chapter-badge">
          <span class="chapter-num">Chapter ${ch.id} · 第${numCN}章</span>
        </div>

        <div class="illustration-frame">
          <img src="images/${ch.image}"
               alt="${ch.title.en} — ${ch.title.zh}"
               loading="${idx === 0 ? 'eager' : 'lazy'}"
               width="1024" height="768">
          <div class="illustration-vignette"></div>
          <div class="illustration-glow" data-glow></div>
        </div>

        <div class="chapter-titles">
          <h2 class="chapter-title-en">${ch.title.en}</h2>
          <h2 class="chapter-title-zh">${ch.title.zh}</h2>
          <p class="chapter-title-pinyin">${ch.title.pinyin}</p>
        </div>

        <div class="chapter-audio">
          <button class="audio-play-btn" data-chapter="${ch.id}" aria-label="Play chapter ${ch.id}">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
          </button>
          <div class="audio-progress" data-chapter="${ch.id}">
            <div class="audio-progress-fill" data-chapter="${ch.id}"></div>
          </div>
          <span class="audio-time" data-chapter="${ch.id}">0:00</span>
        </div>

        <div class="lotus-divider">
          <div class="lotus-divider__line"></div>
          <div class="lotus-divider__petal" data-petal>
            <svg viewBox="0 0 28 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M14 2 C16 6 20 10 14 18 C8 10 12 6 14 2Z"
                    fill="var(--cinnabar)" opacity="0.6"/>
              <path d="M14 4 C15.5 7 18 10 14 16 C10 10 12.5 7 14 4Z"
                    fill="var(--cinnabar-deep)" opacity="0.3"/>
            </svg>
          </div>
          <div class="lotus-divider__line"></div>
        </div>

        <div class="chapter-content">
          <div class="content-en">
            ${ch.content.en.split('\n\n').map(p => `<p>${p}</p>`).join('')}
          </div>
          <div class="content-zh-grid">
            <p class="zh-text">${ch.content.zh}</p>
            <p class="pinyin-line">${ch.content.pinyin}</p>
          </div>
        </div>
      `;

      storyEl.appendChild(article);
    });
  }

  // ── Chapter tray nav ──────────────────────────────────
  function renderChapterTray() {
    chapterTray.innerHTML = '';
    STORY.chapters.forEach((ch, idx) => {
      const chip = document.createElement('button');
      chip.className = `chapter-chip${idx === 0 ? ' active' : ''}`;
      chip.dataset.ch = ch.id;
      chip.setAttribute('aria-label', `Chapter ${ch.id}: ${ch.title.en}`);
      chip.addEventListener('click', () => goToChapter(idx));
      chapterTray.appendChild(chip);
    });
  }

  // ── Navigation ────────────────────────────────────────
  function goToChapter(idx) {
    if (idx < 0 || idx >= state.totalChapters) return;
    // Allow re-rendering the same chapter on first load
    if (idx === state.currentChapter && state.heroDismissed && state.started) return;

    state.currentChapter = idx;

    // stop any playing audio
    if (state.isPlaying) {
      audioPlayer.pause();
      state.isPlaying = false;
    }

    // show/hide chapters
    $$('.story-chapter').forEach((el, i) => {
      const isActive = i === idx;
      el.classList.toggle('active', isActive);
      el.style.display = isActive ? 'block' : 'none';
    });

    // chapter tray
    $$('.chapter-chip').forEach((chip, i) => {
      chip.classList.toggle('active', i === idx);
      chip.classList.toggle('visited', i < idx);
    });

    // prev/next buttons
    prevBtn.disabled = idx === 0;
    nextBtn.disabled = idx === state.totalChapters - 1;

    // update moondial labels
    const ch = STORY.chapters[idx];
    moondialLabelZh.textContent = `第${CN_NUM[ch.id]}章`;
    moondialLabelEn.textContent = `Ch ${ch.id}`;

    // reset audio progress displays
    $$('.audio-progress-fill').forEach(el => el.style.width = '0%');
    $$('.audio-time').forEach(el => el.textContent = '0:00');

    // update moondial level
    updateMoondial(0);

    // scroll to story top
    storyEl.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // trigger illustration glow + lotus petal animations
    setTimeout(() => triggerChapterAnimations(idx), 200);

    // update tide progress
    updateTideProgress();

    // auto-play
    if (state.autoPlay) {
      setTimeout(() => playChapter(idx), 600);
    }
  }

  // ── Chapter animations ────────────────────────────────
  function triggerChapterAnimations(idx) {
    const chapter = $$('.story-chapter')[idx];
    if (!chapter) return;

    // cinnabar glow bloom on illustration
    const glow = chapter.querySelector('[data-glow]');
    if (glow) {
      glow.classList.remove('bloom');
      void glow.offsetWidth; // reflow
      glow.classList.add('bloom');
    }

    // lotus petal stamp in divider
    const petal = chapter.querySelector('[data-petal]');
    if (petal) {
      petal.classList.remove('visible');
      void petal.offsetWidth;
      petal.classList.add('visible');
    }
  }

  // ── Tide progress ──────────────────────────────────────
  function updateTideProgress() {
    const pct = ((state.currentChapter + 1) / state.totalChapters) * 100;
    tideBar.style.setProperty('--pct', pct + '%');
    tideBar.style.width = pct + '%';
  }

  // ── Moondial (audio console) ──────────────────────────
  function updateMoondial(pct) {
    const p = Math.min(Math.max(pct, 0), 100);
    moondialFill.style.setProperty('--pct', p + '%');
    moondialCursor.style.setProperty('--pct', p + '%');
  }

  // ── Audio ─────────────────────────────────────────────
  function getAudioSrc(chapterId) {
    return `audio/${state.lang === 'zh' ? 'zh' : 'en'}/chapter-${chapterId}.mp3`;
  }

  function playChapter(idx) {
    const ch = STORY.chapters[idx];
    if (!ch) return;

    state.currentAudioChapter = idx;
    audioPlayer.src = getAudioSrc(ch.id);
    audioPlayer.currentTime = 0;

    audioPlayer.play().then(() => {
      state.isPlaying = true;
      updateAllPlayButtons();
    }).catch(err => {
      console.warn('Audio play failed:', err);
      state.isPlaying = false;
    });
  }

  function togglePlay(idx) {
    const ch = STORY.chapters[idx];
    if (!ch) return;

    if (state.isPlaying && state.currentAudioChapter === idx) {
      audioPlayer.pause();
      state.isPlaying = false;
    } else if (state.currentAudioChapter === idx) {
      audioPlayer.play().then(() => {
        state.isPlaying = true;
      }).catch(() => { state.isPlaying = false; });
    } else {
      playChapter(idx);
    }
    updateAllPlayButtons();
  }

  function updateAllPlayButtons() {
    // chapter-level buttons
    $$('.audio-play-btn').forEach(btn => {
      const cid = parseInt(btn.dataset.chapter);
      const isOn = cid === state.currentAudioChapter && state.isPlaying;
      btn.classList.toggle('playing', isOn);
      btn.innerHTML = isOn
        ? `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>`
        : `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>`;
      btn.setAttribute('aria-label', isOn ? 'Pause' : 'Play');
    });

    // moondial play/pause icons
    const playSvg = moondialPlay.querySelector('.icon-play');
    const pauseSvg = moondialPlay.querySelector('.icon-pause');
    if (state.isPlaying) {
      playSvg.style.display = 'none';
      pauseSvg.style.display = '';
      moondialPlay.classList.add('playing');
    } else {
      playSvg.style.display = '';
      pauseSvg.style.display = 'none';
      moondialPlay.classList.remove('playing');
    }
  }

  // ── Audio events ──────────────────────────────────────
  audioPlayer.addEventListener('timeupdate', () => {
    if (state.currentAudioChapter < 0 || !audioPlayer.duration) return;
    const ch = STORY.chapters[state.currentAudioChapter];
    if (!ch) return;

    const pct = audioPlayer.currentTime / audioPlayer.duration;

    // chapter-level progress
    const fill = $(`.audio-progress-fill[data-chapter="${ch.id}"]`);
    if (fill) fill.style.width = `${Math.min(pct * 100, 100)}%`;

    const timeEl = $(`.audio-time[data-chapter="${ch.id}"]`);
    if (timeEl) {
      const m = Math.floor(audioPlayer.currentTime / 60);
      const s = Math.floor(audioPlayer.currentTime % 60);
      timeEl.textContent = `${m}:${s.toString().padStart(2, '0')}`;
    }

    // moondial updates
    updateMoondial(pct * 100);
    const m = Math.floor(audioPlayer.currentTime / 60);
    const s = Math.floor(audioPlayer.currentTime % 60);
    moondialTime.textContent = `${m}:${s.toString().padStart(2, '0')}`;
  });

  audioPlayer.addEventListener('ended', () => {
    const chIdx = state.currentAudioChapter;
    state.isPlaying = false;
    updateAllPlayButtons();

    // reset progress
    const ch = STORY.chapters[chIdx];
    if (ch) {
      const fill = $(`.audio-progress-fill[data-chapter="${ch.id}"]`);
      if (fill) fill.style.width = '0%';
    }
    updateMoondial(0);
    moondialTime.textContent = '0:00';

    // auto-advance
    if (state.autoPlay && chIdx < state.totalChapters - 1) {
      setTimeout(() => goToChapter(chIdx + 1), 1200);
    }
  });

  audioPlayer.addEventListener('error', () => {
    state.isPlaying = false;
    updateAllPlayButtons();
  });

  // ── Click to seek (chapter-level progress bar) ────────
  document.addEventListener('click', (e) => {
    const bar = e.target.closest('.audio-progress');
    if (!bar) return;
    const cid = parseInt(bar.dataset.chapter);
    if (cid !== state.currentAudioChapter) return;
    if (!audioPlayer.duration) return;

    const rect = bar.getBoundingClientRect();
    const pct = (e.clientX - rect.left) / rect.width;
    audioPlayer.currentTime = pct * audioPlayer.duration;
  });

  // ── Click to seek (moondial band) ─────────────────────
  moondialBand.addEventListener('click', (e) => {
    if (!audioPlayer.duration) return;
    const rect = moondialBand.getBoundingClientRect();
    const pct = (e.clientX - rect.left) / rect.width;
    audioPlayer.currentTime = pct * audioPlayer.duration;
  });

  // ── Play button clicks (chapter-level) ────────────────
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.audio-play-btn');
    if (!btn) return;
    const cid = parseInt(btn.dataset.chapter);
    togglePlay(STORY.chapters.findIndex(c => c.id === cid));
  });

  // ── Moondial play button ──────────────────────────────
  moondialPlay.addEventListener('click', () => {
    if (state.isPlaying) {
      togglePlay(state.currentAudioChapter);
    } else if (state.currentAudioChapter >= 0) {
      togglePlay(state.currentAudioChapter);
    } else {
      playChapter(state.currentChapter);
    }
  });

  // ── Nav buttons ───────────────────────────────────────
  prevBtn.addEventListener('click', () => {
    if (state.currentChapter > 0) goToChapter(state.currentChapter - 1);
  });
  nextBtn.addEventListener('click', () => {
    if (state.currentChapter < state.totalChapters - 1) goToChapter(state.currentChapter + 1);
  });

  // ── Language toggle ───────────────────────────────────
  function setLang(lang) {
    state.lang = lang;
    document.documentElement.dataset.lang = lang;
    document.documentElement.lang = lang === 'en' ? 'en' : 'zh-Hans';

    langEn.classList.toggle('active', lang === 'en');
    langEn.setAttribute('aria-pressed', lang === 'en');
    langZh.classList.toggle('active', lang === 'zh');
    langZh.setAttribute('aria-pressed', lang === 'zh');

    // swap audio if playing
    if (state.isPlaying && state.currentAudioChapter >= 0) {
      const ch = STORY.chapters[state.currentAudioChapter];
      if (ch) {
        const src = getAudioSrc(ch.id);
        const ct = audioPlayer.currentTime;
        audioPlayer.src = src;
        audioPlayer.currentTime = ct;
        audioPlayer.play().catch(() => {});
      }
    }
  }

  langEn.addEventListener('click', () => setLang('en'));
  langZh.addEventListener('click', () => setLang('zh'));

  // ── Auto-play ─────────────────────────────────────────
  autoplayBtn.addEventListener('click', () => {
    state.autoPlay = !state.autoPlay;
    autoplayBtn.classList.toggle('active', state.autoPlay);

    if (state.autoPlay && !state.isPlaying) {
      playChapter(state.currentChapter);
    }
  });

  // ── Keyboard shortcuts ────────────────────────────────
  document.addEventListener('keydown', (e) => {
    if (!state.started) return;
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    switch (e.key) {
      case 'ArrowLeft':
        e.preventDefault();
        if (state.currentChapter > 0) goToChapter(state.currentChapter - 1);
        break;
      case 'ArrowRight':
        e.preventDefault();
        if (state.currentChapter < state.totalChapters - 1) goToChapter(state.currentChapter + 1);
        break;
      case ' ':
        e.preventDefault();
        if (state.isPlaying) {
          togglePlay(state.currentAudioChapter);
        } else if (state.currentAudioChapter >= 0) {
          togglePlay(state.currentAudioChapter);
        } else {
          playChapter(state.currentChapter);
        }
        break;
      case 'a': case 'A':
        if (!e.ctrlKey && !e.metaKey) {
          autoplayBtn.click();
        }
        break;
    }
  });

  // ── Hero → Story transition ───────────────────────────
  beginBtn.addEventListener('click', () => {
    state.started = true;
    hero.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    hero.style.opacity = '0';
    hero.style.transform = 'translateY(-20px)';
    setTimeout(() => {
      hero.style.display = 'none';
      state.heroDismissed = true;
      header.style.display = '';
      tideProgress.style.display = '';
      goToChapter(0);
      startParticles();
    }, 600);
  });

  // ── Init ──────────────────────────────────────────────
  function init() {
    renderChapters();
    renderChapterTray();

    // hide header + progress initially (hero visible)
    header.style.display = 'none';
    tideProgress.style.display = 'none';

    prevBtn.disabled = true;
    nextBtn.disabled = false;

    // set initial lang
    setLang('zh');
  }

  init();
})();
