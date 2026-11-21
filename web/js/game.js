/*
 * Paper Launch — web edition.
 *
 * A browser port of Adam W. Cooper's 2012 CMU 15-112 term project
 * (originally Python + pygame). The game logic, physics constants and screen
 * layouts follow the original PaperLaunch.py closely; the simulation runs at
 * the original fixed 30 ticks per second regardless of display refresh rate.
 *
 * Added for the web: mouse/touch controls, localStorage saves, responsive
 * scaling and fullscreen.
 */
(() => {
  'use strict';

  // ---------------------------------------------------------------------------
  // Constants
  // ---------------------------------------------------------------------------
  const W = 1000;
  const H = 600;
  const TICK_MS = 1000 / 30;
  const SAVE_KEY = 'paperLaunch.save.v1';
  const GROUND = 100;
  const PAD = 0.2;

  const ASSETS = {
    // sprites
    airplane: 'png', airplane1: 'png', bear: 'png', bearSwipe: 'png', bigcannon: 'png',
    boom: 'png', car1: 'png', car12: 'png', carpeDiem: 'png', carpeDiemMachine: 'png',
    kosbie: 'jpg', money: 'png', nyanCat: 'png', nyanCat1: 'png', nyanCat2: 'png',
    nyanCat3: 'png', selfFalling: 'png', selfFalling2: 'png', selfFalling3: 'png',
    selfHurt: 'png', selfair: 'png', shark: 'png', slingshot: 'png',
    slingshotSwoosh: 'png', sunMachine: 'png', tank: 'png', trogdor: 'png',
    trogdorEvent: 'png',
    // how-to-play
    htp1: 'png', htp2: 'png', htp3: 'png', htp4: 'png', htp5: 'png', htp6: 'png',
    htp7: 'png', htp8: 'png', htpBg: 'png',
    // icons
    areYouSure: 'png', extrasButton: 'jpg', hermesBoot: 'png', moonBoot: 'png',
    musicNote: 'png', oldBoot: 'png', optionsButton: 'jpg', playButton: 'jpg',
    saveFileNo: 'png', saveFileYes: 'png', saveIcon: 'png', sketchBookIcon: 'png',
    storeButton: 'jpg',
    // backgrounds
    gameOverScreen: 'jpg', mainMenu: 'png', paperSlice: 'jpg', sketchbookBg: 'png',
    store: 'png', tealPaperBg: 'jpg',
  };

  const COSTS = [
    [300, 600, 2500, 7500, 15000], // agility
    [300, 600, 2500, 7500, 17000], // fortitude
    [100, 700, 1200, 5400, 10000], // iterance
    [300, 600, 2500, 7500, 20000], // serendipity
    [300, 800, 5000, 7500, 17000], // resistance
    [0, 7500, 20000],              // boots
    [0, 1000, 7500, 15000, 30000], // cannons
  ];
  const STAT_KEYS = ['agility', 'fortitude', 'iterance', 'serendipity', 'resistance'];
  const STAT_INFO = [
    'Agility: Increase your maximum speed',
    'Fortitude: Lose less speed when you hit the ground',
    'Iterance: Increase the number of times you can boost',
    'Serendipity: Increase your chances of seeing money and helpful doodles',
    'Resistance: Lose less speed when hitting enemies',
  ];

  const CANNONS = ['slingshot', 'cannon', 'tank', 'sunMachine', 'carpeDiemMachine'];
  const CANNON_SPRITE = {
    slingshot: 'slingshot', cannon: 'bigcannon', tank: 'tank',
    sunMachine: 'sunMachine', carpeDiemMachine: 'carpeDiem',
  };
  const CANNON_POWER = { slingshot: 20, cannon: 40, tank: 80, sunMachine: 140, carpeDiemMachine: 300 };
  const CANNON_INFO = [
    'Slingshot: Good for propelling you forward.',
    'Cannon: Perfect for recreational launching.',
    "Tank: If the military comes asking for Top Secret schematics, we don't know nothin'.",
    'Sun Machine: For launching with a bit more elegance.',
    'Carpe Diem Machine: Seize the day, soar to the heavens.',
  ];

  const BOOTS = ['oldBoots', 'moonBoots', 'hermesBoots'];
  const BOOT_SPRITE = ['oldBoot', 'moonBoot', 'hermesBoot'];
  const BOOT_FORCE = { oldBoots: 8, moonBoots: 15, hermesBoots: 28 };
  const BOOT_INFO = [
    'Old Boots: Old yet reliable.',
    'Moon Boots: Get to the moon and back.',
    'Hermes Boots: The boots of the gods.',
  ];

  // Fortitude level -> [xFriction, yFriction] applied on each bounce.
  const FORTITUDE = [[1.7, -1.85], [1.5, -1.7], [1.4, -1.6], [1.3, -1.5], [1.15, -1.4], [1.1, -1.2]];

  const MENU_BUTTONS = ['playButton', 'storeButton', 'extrasButton', 'optionsButton'];
  const MENU_SCREENS = ['store', 'extras', 'options', 'game']; // indexed by buttonSelect

  const OPTIONS = ['autoSave', 'save', 'erase'];

  // ---------------------------------------------------------------------------
  // Setup
  // ---------------------------------------------------------------------------
  const canvas = document.getElementById('game');
  const ctx = canvas.getContext('2d');
  const sprites = {};
  const S = {}; // all mutable game state (the original's `data` struct)

  const rand = Math.random;
  const choice = (arr) => arr[Math.floor(rand() * arr.length)];
  const randInt = (a, b) => {
    a = Math.trunc(a); b = Math.trunc(b);
    if (b < a) [a, b] = [b, a];
    return a + Math.floor(rand() * (b - a + 1));
  };
  const size = (name) => [sprites[name].width, sprites[name].height];

  function loadImages() {
    return Promise.all(Object.entries(ASSETS).map(([name, ext]) => new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => { sprites[name] = img; resolve(); };
      img.onerror = () => reject(new Error('Could not load ' + name));
      img.src = `assets/${name}.${ext}`;
    })));
  }

  // ---------------------------------------------------------------------------
  // Saving (localStorage instead of a pickle file)
  // ---------------------------------------------------------------------------
  function emptySave() {
    return {
      agility: 0, fortitude: 0, iterance: 0, serendipity: 0, resistance: 0,
      bank: 500, maxHeight: 0, bestDistance: 0,
      unlockedBoots: 1, currentBoot: 'oldBoots',
      unlockedCannons: 1, currentCannon: 'slingshot',
      sketchbook: ['self'], autoSave: true,
    };
  }

  function storageAvailable() {
    try {
      localStorage.setItem('__pl_test', '1');
      localStorage.removeItem('__pl_test');
      return true;
    } catch (e) { return false; }
  }

  function loadSave() {
    S.canSave = storageAvailable();
    let raw = null;
    try { raw = S.canSave ? localStorage.getItem(SAVE_KEY) : null; } catch (e) { raw = null; }
    if (raw) {
      try {
        S.save = Object.assign(emptySave(), JSON.parse(raw));
        S.firstTime = false;
        return;
      } catch (e) { /* corrupt save: fall through to a fresh one */ }
    }
    S.save = emptySave();
    S.firstTime = 'saveMessage';
    if (S.canSave) writeSave(S.save);
  }

  function writeSave(obj) {
    try { localStorage.setItem(SAVE_KEY, JSON.stringify(obj)); return true; } catch (e) { return false; }
  }

  function save() {
    const ok = writeSave({
      agility: S.levels[0], fortitude: S.levels[1], iterance: S.levels[2],
      serendipity: S.levels[3], resistance: S.levels[4],
      bank: S.bank, maxHeight: S.bestHeight, bestDistance: S.bestDistance,
      unlockedBoots: S.unlockedBoots, currentBoot: S.currentBoot,
      unlockedCannons: S.unlockedCannons, currentCannon: S.currentCannon,
      sketchbook: S.sketchbook.slice(), autoSave: S.autoSave,
    });
    if (ok) S.icons.save.killTime = 40;
  }

  // ---------------------------------------------------------------------------
  // Init
  // ---------------------------------------------------------------------------
  function init() {
    S.currentScreen = 'mainMenu';
    S.buttonSelect = 3;
    S.gameOverButtonSelect = 0;
    S.storeButtonSelect = 0;
    S.cannonButtonSelect = 0;
    S.bootButtonSelect = 0;
    S.optionsSelect = 0;
    S.areYouSure = false;
    S.instructions = false;
    S.htpi = 0;
    S.debugMode = false;
    S.playerSprite = 'selfair';
    S.changeAni = 'up';
    S.icons = { save: new Icon('saveIcon'), sketchbook: new Icon('sketchBookIcon') };
    S.bgWidth = sprites.paperSlice.width;
    S.bgHeight = sprites.paperSlice.height;
    [S.selfW, S.selfH] = size('selfair');
    S.radius = S.selfH;
    S.onScreen = [];
    S.launch = 'launchBar';
    initStats();
    S.sketchbookSelect = 0;
  }

  function initStats() {
    const s = S.save;
    S.bank = s.bank;
    S.levels = STAT_KEYS.map((k) => Math.max(0, Math.min(5, s[k] | 0)));
    S.unlockedCannons = s.unlockedCannons;
    S.currentCannon = CANNONS.includes(s.currentCannon) ? s.currentCannon : 'slingshot';
    S.unlockedBoots = s.unlockedBoots;
    S.currentBoot = BOOTS.includes(s.currentBoot) ? s.currentBoot : 'oldBoots';
    S.autoSave = s.autoSave;
    S.sketchbook = s.sketchbook.slice();
    S.bestHeight = s.maxHeight || 0;
    S.bestDistance = s.bestDistance || 0;
  }

  const agility = () => S.levels[0];
  const fortitude = () => S.levels[1];
  const iterance = () => S.levels[2];
  const serendipity = () => S.levels[3];
  const resistance = () => S.levels[4];

  function initGame() {
    if (S.firstTime) S.instructions = true;
    S.gameOver = false;
    S.runCash = 0;
    S.maxHeight = 0;
    S.newBest = false;
    // physics
    S.bgx = 0;
    S.bgy = 0;
    S.distance = 0;
    S.launchBarLength = 0;
    [S.xFriction, S.yFriction] = FORTITUDE[fortitude()];
    S.selfHeight = 0;
    S.theta = Math.PI / 32;
    S.dTheta = Math.PI / 32;
    S.yVelocity = 0;
    S.xSpeed = 0;
    S.maxBoost = 5 + iterance();
    S.boostCount = S.maxBoost;
    S.selfHitbox = {
      x: 100, y: H - Math.trunc(S.selfH * PAD),
      w: Math.trunc(S.selfW * (1 - PAD * 2)), h: Math.trunc(S.selfH * (1 - PAD * 2)),
    };
    S.onScreen = [new Cannon()];
    S.launch = 'launchBar';
    S.playerSprite = 'selfair';
    S.changeAni = 'up';
  }

  // ---------------------------------------------------------------------------
  // Game objects
  // ---------------------------------------------------------------------------
  const overlap = (a, b) => a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
  const groundY = (h) => H - GROUND - h + S.bgy - 2;
  const skyY = (h) => randInt(H - S.bgHeight + h + S.bgy, H - Math.floor(S.bgHeight / 2) + h + S.bgy);

  function cameraAbsorbsVelocity() {
    // When true the background scrolls instead of the player moving.
    return !(S.selfHeight < H / 2 ||
      (S.yVelocity < 0 && S.bgy === 0) ||
      (S.yVelocity > 0 && S.bgy === S.bgHeight - H) ||
      (S.selfHeight + GROUND > H * 0.8));
  }

  function discover(name) {
    if (!S.sketchbook.includes(name)) {
      S.sketchbook.push(name);
      S.icons.sketchbook.killTime = 40;
    }
  }

  class PhysicalObject {
    constructor(image, x, y, resistance = 0) {
      this.setImage(image);
      this.location = [x, y];
      this.resistance = resistance;
      this.encounter = false;
      this.updateHitbox();
    }
    get name() { return this.constructor.key; }
    setImage(image) {
      this.image = image;
      [this.width, this.height] = size(image);
    }
    updateHitbox() {
      this.hitbox = {
        x: Math.trunc(this.location[0] + this.width * PAD),
        y: Math.trunc(this.location[1] + this.height * PAD),
        w: Math.trunc(this.width * (1 - PAD * 2)),
        h: Math.trunc(this.height * (1 - PAD * 2)),
      };
    }
    remove() {
      const i = S.onScreen.indexOf(this);
      if (i >= 0) S.onScreen.splice(i, 1);
    }
    move() {
      if (this.location[0] < -W / 2 || this.location[0] > W * 1.5) { this.remove(); return; }
      this.location[0] -= S.xSpeed / 3 + this.resistance;
      if (cameraAbsorbsVelocity()) this.location[1] += S.yVelocity;
      this.updateHitbox();
      if (overlap(this.hitbox, S.selfHitbox)) this.event();
    }
    animate() {}
    event() { discover(this.name); }
    draw() {
      ctx.drawImage(sprites[this.image], Math.round(this.location[0]), Math.round(this.location[1]));
      if (S.debugMode) strokeRect(this.hitbox, '#f00', 4);
    }
  }

  class Cannon extends PhysicalObject {
    static key = 'cannon';
    constructor() {
      const img = CANNON_SPRITE[S.currentCannon];
      super(img, 100, 0);
      this.location[1] = groundY(this.height);
      this.updateHitbox();
    }
    event() {
      if (S.currentCannon === 'slingshot') this.image = 'slingshotSwoosh';
      discover(S.currentCannon);
    }
  }

  class Bear extends PhysicalObject {
    static key = 'bear';
    constructor() {
      super('bear', 0, 0);
      this.location = [W + this.width, groundY(this.height)];
    }
    event() {
      if (!this.encounter) { // swats you into the ground and slows you down
        this.encounter = true;
        this.setImage('bearSwipe');
        S.xSpeed = Math.trunc(S.xSpeed * (0.78 + resistance() * 0.03));
        S.yVelocity = -Math.trunc(Math.abs(S.yVelocity) - 15);
      }
      super.event();
    }
  }

  class Shark extends PhysicalObject {
    static key = 'shark';
    constructor() {
      super('shark', 0, 0, 10);
      this.location = [W + this.width, skyY(this.height)];
    }
    event() {
      if (!this.encounter) { // knocks you down fast and slows you down
        this.encounter = true;
        S.xSpeed = Math.trunc(S.xSpeed * (0.4 + resistance() * 0.1));
        S.yVelocity = -Math.trunc(Math.abs(S.yVelocity)) - 12;
      }
      super.event();
    }
  }

  class Car extends PhysicalObject {
    static key = 'car';
    constructor() {
      super('car1', 0, 0, 20);
      this.counter = 0;
      this.location = [W + this.width, groundY(this.height)];
    }
    animate() {
      this.counter = (this.counter + 1) % 10;
      this.image = this.counter % 9 < 5 ? 'car1' : 'car12';
    }
    event() {
      if (!this.encounter) { // pops you up but slows you down
        S.xSpeed = Math.trunc(S.xSpeed / (2 - resistance() * 0.15));
        S.yVelocity = 10 + Math.abs(S.yVelocity);
        this.encounter = true;
      }
      super.event();
    }
  }

  class NyanCat extends PhysicalObject {
    static key = 'nyanCat';
    constructor() {
      super('nyanCat', 0, 0, -20);
      this.counter = 0;
      this.location = [W + this.width, skyY(this.height)];
    }
    animate() {
      this.counter = (this.counter + 1) % 12;
      this.image = ['nyanCat', 'nyanCat1', 'nyanCat2', 'nyanCat3'][Math.floor(this.counter / 3) % 4];
    }
    event() {
      if (S.boostCount < S.maxBoost && !this.encounter) { // refills a boost
        S.boostCount += 1;
        this.encounter = true;
      }
      super.event();
    }
  }

  class Money extends PhysicalObject {
    static key = 'money';
    constructor() {
      super('money', 0, 0);
      this.location = [W + this.width, randInt(H - S.bgHeight + this.height + S.bgy, groundY(this.height))];
    }
    event() {
      this.remove();
      S.runCash += 100;
      S.bank += 100;
      super.event();
    }
  }

  class Airplane extends PhysicalObject {
    static key = 'airplane';
    constructor() {
      super('airplane', 0, 0, -23);
      this.flip = true;
      this.location = [W + this.width, skyY(this.height)];
    }
    animate() {
      this.flip = !this.flip;
      if (!this.encounter) this.image = this.flip ? 'airplane1' : 'airplane';
    }
    event() {
      if (!this.encounter) { // big boost up and forward
        this.setImage('boom');
        this.encounter = true;
        this.resistance = 0;
        S.yVelocity = Math.abs(S.yVelocity) + 20;
        S.xSpeed += 70;
      }
      super.event();
    }
  }

  class Trogdor extends PhysicalObject {
    static key = 'trogdor';
    constructor() {
      super('trogdor', 0, 0);
      this.location = [W + this.width, groundY(this.height)];
    }
    event() {
      if (!this.encounter) { // like the airplane, but smaller
        this.setImage('trogdorEvent');
        this.encounter = true;
        S.yVelocity = Math.abs(S.yVelocity) + 17;
        S.xSpeed += 50;
      }
      super.event();
    }
  }

  class Icon {
    constructor(image) { this.image = image; this.killTime = 0; }
    animate() { if (this.killTime > 0) this.killTime -= 1; }
    draw() {
      if (this.killTime !== 0) ctx.drawImage(sprites[this.image], W - sprites[this.image].width, 0);
    }
  }

  // ---------------------------------------------------------------------------
  // Simulation (one call = one 1/30 s tick)
  // ---------------------------------------------------------------------------
  function gamePlay() {
    if (S.instructions || S.gameOver) return;
    if (S.launch === 'launchBar') {
      S.launchBarLength = S.launchBarLength > 100 ? 0 : S.launchBarLength + 5;
    } else if (S.launch === 'angle') {
      if (!(S.theta > 0 && S.theta < Math.PI / 2)) S.dTheta *= -1; // meter bounces at the bounds
      S.theta += S.dTheta;
    }
    movement();
    const height = S.selfHeight - GROUND + S.bgy;
    if (height > S.maxHeight) S.maxHeight = height;
    if (S.xSpeed > 0) monsterFactory();
  }

  function monsterFactory() {
    const r = rand();
    if (S.onScreen.length >= 13) return;
    if (r > 0.99) S.onScreen.push(new (choice([Car, Bear, Shark]))());
    if (r > 0.5 && r < 0.5 + serendipity() * 0.005 + 0.01) S.onScreen.push(new (choice([Trogdor, Airplane, NyanCat]))());
    if (r < 0.05 + serendipity() * 0.03) S.onScreen.push(new Money());
  }

  function movement() {
    if (S.yVelocity > 180) S.yVelocity = 180;
    const cap = 50 * (agility() + 1);
    if (S.xSpeed > cap) S.xSpeed = cap;

    if (S.xSpeed === 0 && S.launch === false && !S.gameOver) {
      S.gameOver = true;
      endRun();
    }
    S.bgx += S.xSpeed / 3;
    S.distance += S.xSpeed;
    S.yVelocity -= 1; // gravity
    for (const item of S.onScreen.slice()) item.move();
    if (cameraAbsorbsVelocity()) S.bgy += S.yVelocity;
    else S.selfHeight += S.yVelocity;
    if (S.selfHeight < 0) bounce();
  }

  function bounce() {
    S.selfHeight = 0;
    S.bgy = 0;
    if (S.xSpeed > 0) S.yVelocity = Math.trunc(S.yVelocity / S.yFriction);
    if (S.xSpeed === 0) S.yVelocity = 0;
    S.xSpeed = Math.trunc(S.xSpeed / S.xFriction);
  }

  function endRun() {
    S.bank += Math.floor(S.distance / 100);
    S.endTime = performance.now();
    const dist = Math.floor(S.distance / 100);
    if (dist > S.bestDistance) { S.bestDistance = dist; S.newBest = true; }
    S.bestHeight = Math.max(S.bestHeight, Math.round(S.maxHeight));
    S.gameOverButtonSelect = 0;
    if (S.autoSave) save();
  }

  function launch() {
    const power = CANNON_POWER[S.currentCannon];
    S.xSpeed = Math.trunc(Math.cos(S.theta) * (S.launchBarLength / 100) * power) + 20;
    S.yVelocity = Math.trunc(Math.sin(S.theta) * (S.launchBarLength / 100) * power) + 20;
    S.launch = false;
    S.startTime = performance.now();
  }

  function boost() {
    S.xSpeed = Math.abs(S.xSpeed) + BOOT_FORCE[S.currentBoot];
    S.yVelocity = Math.floor(Math.abs(S.yVelocity) / 2) + BOOT_FORCE[S.currentBoot];
    S.boostCount -= 1;
  }

  // ---------------------------------------------------------------------------
  // Drawing helpers
  // ---------------------------------------------------------------------------
  function font(px) { return `${Math.round(px * 0.8)}px "Times New Roman", Times, Georgia, serif`; }

  function text(str, x, y, px = 20, color = '#0a0c0a', align = 'left') {
    ctx.font = font(px);
    ctx.fillStyle = color;
    ctx.textAlign = align;
    ctx.textBaseline = 'top';
    ctx.fillText(str, x, y);
    return ctx.measureText(str).width;
  }

  function textHeight(px) { return Math.round(px * 0.8 * 1.2); }

  function strokeRect(r, color, width) {
    ctx.lineWidth = width;
    ctx.strokeStyle = color;
    ctx.strokeRect(r.x + width / 2, r.y + width / 2, r.w - width, r.h - width);
  }

  function fillRect(x, y, w, h, color) { ctx.fillStyle = color; ctx.fillRect(x, y, w, h); }

  function blit(name, x, y, w, h) {
    const img = sprites[name];
    if (w === undefined) ctx.drawImage(img, x, y);
    else ctx.drawImage(img, x, y, w, h);
  }

  // ---------------------------------------------------------------------------
  // Screens
  // ---------------------------------------------------------------------------
  function redrawAll() {
    fillRect(0, 0, W, H, '#000');
    switch (S.currentScreen) {
      case 'mainMenu': drawMainMenu(); break;
      case 'store': drawStore(); break;
      case 'options': drawOptions(); break;
      case 'extras': drawSketchbook(); break;
      case 'game': drawGame(); break;
    }
    S.icons.save.draw();
    S.icons.sketchbook.draw();
    if (S.instructions) drawInstructions();
    if (S.firstTime === 'saveMessage') drawSaveMessage();
  }

  function menuLayout() {
    const [bw, bh] = size('playButton');
    const scale = 1.4;
    const down = 120;
    const sideY = H / 2 - bh + down;
    return [
      { x: W / 2 - bw / 2 - bw - 60, y: sideY, w: bw, h: bh },
      { x: W / 2 - (bw * scale) / 2, y: H / 2 - bh * scale + down, w: bw * scale, h: bh * scale },
      { x: W / 2 + bw / 2 + 60, y: sideY, w: bw, h: bh },
    ];
  }

  function drawMainMenu() {
    blit('mainMenu', 0, 0, W, H);
    menuLayout().forEach((r, i) => {
      blit(MENU_BUTTONS[(i + S.buttonSelect) % 4], r.x, r.y, r.w, r.h);
    });
    if (S.bestDistance > 0) {
      text(`Best distance: ${S.bestDistance}m   ·   Money: $${S.bank}`, W / 2, H - 40, 26, '#355', 'center');
    }
  }

  function drawGame() {
    drawBackground();
    if (S.launch === false) drawSelf();
    for (const item of S.onScreen) item.draw();
    drawInfo();
    drawBoosts();
    // A little in-joke from the original for the most powerful launcher.
    if (S.onScreen.length && S.launch === false && S.onScreen[0] instanceof Cannon &&
        S.currentCannon === 'carpeDiemMachine' && S.xSpeed > 70) {
      blit('kosbie', 0, 0);
    }
    if (S.launch !== false) {
      drawLaunchBar();
      if (S.launch === 'angle') drawAngle();
    }
    if (S.gameOver) drawGameOver();
    if (S.debugMode) drawDebug();
  }

  function drawBackground() {
    if (S.bgy > S.bgHeight - H) S.bgy = S.bgHeight - H;
    if (S.bgy < 0) S.bgy = 0;
    if (S.bgx > S.bgWidth) S.bgx %= S.bgWidth;
    const tiles = Math.ceil(W / S.bgWidth) + 1;
    for (let t = 0; t < tiles; t++) {
      blit('paperSlice', Math.round(t * S.bgWidth - S.bgx), Math.round(H - S.bgHeight + S.bgy));
    }
  }

  function drawSelf() {
    const changeSprite = (S.changeAni === 'up' && S.yVelocity <= 0) || (S.changeAni === 'down' && S.yVelocity > 0);
    if (changeSprite) {
      if (S.yVelocity > 0) { S.playerSprite = 'selfair'; S.changeAni = 'up'; } else {
        S.playerSprite = choice(['selfFalling', 'selfFalling2', 'selfFalling3']);
        S.changeAni = 'down';
      }
    }
    S.selfHitbox = {
      x: 100 + 100 * PAD,
      y: Math.trunc(H - S.selfHeight + S.selfH * PAD - S.radius) - GROUND,
      w: Math.trunc(S.selfW * (1 - PAD * 2)),
      h: Math.trunc(S.selfH * (1 - PAD * 2)),
    };
    blit(S.playerSprite, 100, Math.round(H - S.radius - GROUND - S.selfHeight));
    if (S.debugMode) strokeRect(S.selfHitbox, '#f00', 4);
  }

  function drawInfo() {
    fillRect(4, H - 34, W - 6, 30, '#fff');
    blit('musicNote', W - 34, H - 34);
    if (S.selfHeight + GROUND > H) {
      // Off the top of the screen: show how high you are.
      fillRect(440, 4, 120, 35, '#f00');
      strokeRect({ x: 440, y: 4, w: 120, h: 35 }, '#000', 2);
      text(`↑ ${Math.round(S.selfHeight - GROUND + S.bgy)}m`, 500, 12, 22, '#0a0c0a', 'center');
    }
    text(`Distance: ${Math.floor(S.distance / 100)}m`, W / 2 - 80, H - 28, 22);
    strokeRect({ x: 4, y: H - 36, w: W - 6, h: 32 }, '#000', 2);
  }

  function drawBoosts() {
    for (let b = 0; b < S.maxBoost; b++) fillRect(6 + 25 * b, H - 34, 23, 28, '#000');
    for (let b = 0; b < S.boostCount; b++) fillRect(6 + 25 * b, H - 34, 23, 28, '#00f');
  }

  function drawLaunchBar() {
    fillRect(75, H - GROUND - 100, 20, 100, '#000');
    fillRect(75, H - GROUND - S.launchBarLength, 20, S.launchBarLength, S.launchBarLength > 95 ? '#e1e100' : '#f00');
  }

  function drawAngle() {
    const bottom = H - GROUND - 10;
    ctx.lineWidth = 5;
    ctx.strokeStyle = '#f00';
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(110, bottom);
    ctx.lineTo(110 + 100 * Math.cos(S.theta), bottom - 100 * Math.sin(S.theta));
    ctx.stroke();
  }

  const GAME_OVER_BUTTONS = [
    { x: 572, y: 175, w: 212, h: 136 }, // retry
    { x: 572, y: 327, w: 212, h: 136 }, // store
  ];

  function drawGameOver() {
    blit('gameOverScreen', W * 0.1, H * 0.1, W * 0.8, H * 0.8);
    const runTime = ((S.endTime - S.startTime) / 1000).toFixed(1) + 's';
    text(String(Math.floor(S.distance / 100)) + 'm', 466, 172, 24);
    if (S.newBest) text('New best distance!', 150, 360, 30, '#c00');
    text(`${Math.round(S.maxHeight)}cm`, 403, 200, 24);
    text(runTime, 368, 228, 24);
    text(String(S.runCash), 397, 282, 24);
    text(String(S.bank), 392, 311, 24);
    strokeRect(GAME_OVER_BUTTONS[S.gameOverButtonSelect], '#f00', 4);
  }

  function drawDebug() {
    text(S.onScreen.map((o) => o.name).join(', '), 4, 4, 20);
    text(`xSpeed = ${S.xSpeed}`, 4, 24, 20);
    text(`yVelocity = ${S.yVelocity}`, 4, 44, 20);
  }

  function drawInstructions() {
    blit('htpBg', 0, 0);
    blit('htp' + (S.htpi + 1), 50, 50);
    fillRect(W / 2 - 230, H - 50, 460, 32, 'rgba(255,255,255,.9)');
    text(`${S.htpi + 1} / 8 — press any key or tap to continue`, W / 2, H - 44, 24, '#222', 'center');
  }

  function drawSaveMessage() {
    blit('htpBg', 0, 0);
    blit(S.canSave ? 'saveFileYes' : 'saveFileNo', 300, 220);
  }

  // --- Store -----------------------------------------------------------------
  const STAT_ROW = (i) => ({ x: 139, y: i * 36 + 135, w: 125, h: 31 });
  const BOOT_ICON = (i) => ({ x: 323 + 150 * i, y: H - 265, w: 100, h: 80 });
  const CANNON_ICON = (i) => ({ x: 230 + 150 * i, y: H - 170, w: 100, h: 80 });
  const STORE_BACK = { x: 60, y: 35, w: 200, h: 60 };
  const STORE_PLAY = { x: 720, y: 35, w: 170, h: 60 };

  function drawStore() {
    blit('store', 0, 0);
    // level bars (aligned with the row labels)
    for (let i = 0; i < 5; i++) {
      const row = STAT_ROW(i);
      fillRect(284, row.y, 95 * S.levels[i], row.h, 'rgba(230, 30, 30, .85)');
    }
    // boots
    for (let b = 0; b < 3; b++) {
      const r = BOOT_ICON(b);
      if (b >= S.unlockedBoots + 1) { fillRect(r.x, r.y, r.w, r.h, '#000'); continue; } // hidden
      ctx.globalAlpha = b < S.unlockedBoots ? 1 : 0.4;
      blit(BOOT_SPRITE[b], r.x, r.y, r.w, r.h);
      ctx.globalAlpha = 1;
    }
    strokeRect(BOOT_ICON(BOOTS.indexOf(S.currentBoot)), '#000', 4);
    if (S.storeButtonSelect === 5) strokeRect(BOOT_ICON(S.bootButtonSelect), '#f00', 6);
    // cannons
    for (let c = 0; c < 5; c++) {
      const r = CANNON_ICON(c);
      if (c >= S.unlockedCannons + 1) { fillRect(r.x, r.y, r.w, r.h, '#000'); continue; }
      ctx.globalAlpha = c < S.unlockedCannons ? 1 : 0.4;
      blit(CANNON_SPRITE[CANNONS[c]], r.x, r.y, r.w, r.h);
      ctx.globalAlpha = 1;
    }
    strokeRect(CANNON_ICON(CANNONS.indexOf(S.currentCannon)), '#000', 4);
    if (S.storeButtonSelect === 6) strokeRect(CANNON_ICON(S.cannonButtonSelect), '#f00', 6);
    if (S.storeButtonSelect < 5) strokeRect(STAT_ROW(S.storeButtonSelect), '#f00', 2);

    // info line + money + cost
    const sel = S.storeButtonSelect;
    let info = '';
    let cost = null;
    if (sel < 5) {
      const lvl = S.levels[sel];
      info = lvl >= 5 ? 'Maxed!!!' : STAT_INFO[sel].replace(':', ` lv${lvl + 1}:`);
      if (lvl < 5) cost = COSTS[sel][lvl];
    } else if (sel === 5) {
      info = BOOT_INFO[S.bootButtonSelect];
      if (S.bootButtonSelect === S.unlockedBoots) cost = COSTS[5][S.unlockedBoots];
      else if (BOOTS[S.bootButtonSelect] === S.currentBoot) info += '  (equipped)';
    } else {
      info = CANNON_INFO[S.cannonButtonSelect];
      if (S.cannonButtonSelect === S.unlockedCannons) cost = COSTS[6][S.unlockedCannons];
      else if (CANNONS[S.cannonButtonSelect] === S.currentCannon) info += '  (equipped)';
    }
    text(info, 150, 541, 22);
    text(`Money: $${S.bank}`, 10, H - 28, 22);
    if (cost !== null && cost > 0) {
      const color = cost <= S.bank ? '#0a0c0a' : '#b00';
      text(`Cost: $${cost}${cost > S.bank ? ' (not enough money)' : ''}`, 200, H - 28, 22, color);
    }
    if (S.storeFlash > 0) {
      S.storeFlash -= 1;
      text('Purchased!', 880, H - 28, 22, '#070', 'center');
    }
  }

  function storeUp() { S.storeButtonSelect = (S.storeButtonSelect + 6) % 7; }
  function storeDown() { S.storeButtonSelect = (S.storeButtonSelect + 1) % 7; }

  function storeLeftRight(dir) {
    if (S.storeButtonSelect === 5) {
      const n = Math.min(S.unlockedBoots + 1, 3);
      S.bootButtonSelect = (S.bootButtonSelect + dir + n) % n;
    } else if (S.storeButtonSelect === 6) {
      const n = Math.min(S.unlockedCannons + 1, 5);
      S.cannonButtonSelect = (S.cannonButtonSelect + dir + n) % n;
    }
  }

  function storeEnter() {
    const sel = S.storeButtonSelect;
    let bought = false;
    if (sel === 5) {
      const b = S.bootButtonSelect;
      if (b < S.unlockedBoots) S.currentBoot = BOOTS[b];
      else if (b === S.unlockedBoots && S.bank >= COSTS[5][b]) {
        S.bank -= COSTS[5][b];
        S.unlockedBoots += 1;
        S.currentBoot = BOOTS[b];
        discover(BOOTS[b]);
        bought = true;
      }
    } else if (sel === 6) {
      const c = S.cannonButtonSelect;
      if (c < S.unlockedCannons) S.currentCannon = CANNONS[c];
      else if (c === S.unlockedCannons && S.unlockedCannons < 5 && S.bank >= COSTS[6][c]) {
        S.bank -= COSTS[6][c];
        S.unlockedCannons += 1;
        S.currentCannon = CANNONS[c];
        bought = true;
      }
    } else if (S.levels[sel] < 5 && S.bank >= COSTS[sel][S.levels[sel]]) {
      S.bank -= COSTS[sel][S.levels[sel]];
      S.levels[sel] += 1;
      bought = true;
    }
    if (bought) S.storeFlash = 30;
    if (S.autoSave) save();
  }

  // --- Options ---------------------------------------------------------------
  function optionRows() {
    const h = textHeight(36);
    return OPTIONS.map((_, i) => ({ x: 96, y: 150 + h * i, w: 260, h }));
  }

  function drawOptions() {
    blit('tealPaperBg', 0, 0);
    const labels = [`AutoSave: ${S.autoSave ? 'ON' : 'OFF'}`, 'Save Game', 'Delete File'];
    const rows = optionRows();
    labels.forEach((l, i) => text(l, 100, rows[i].y + 4, 36));
    strokeRect(rows[S.optionsSelect], '#e10000', 2);
    text('Esc or ← Back to return', 100, 150 + textHeight(36) * 3 + 30, 22, '#444');
    if (S.areYouSure) {
      blit('htpBg', 0, 0);
      blit('areYouSure', 300, 220);
      text('Tap the message to confirm, anywhere else to cancel', W / 2, 380, 20, '#444', 'center');
    }
  }

  function optionsEnter() {
    const opt = OPTIONS[S.optionsSelect];
    if (opt === 'autoSave') { S.autoSave = !S.autoSave; save(); } else if (opt === 'save') save();
    else if (opt === 'erase') {
      if (S.areYouSure) {
        S.save = emptySave();
        initStats();
        S.sketchbookSelect = 0;
        S.firstTime = true;
        save();
        S.areYouSure = false;
        S.currentScreen = 'mainMenu';
      } else S.areYouSure = true;
    }
  }

  // --- Sketchbook (credits / collection) ---------------------------------------
  function sketchbookEntries() {
    const sb = S.sketchbook;
    const list = [['selfair', 'Adam Cooper'], ['selfHurt', 'Adam Cooper'], ['oldBoot', 'Adam Cooper'],
      ['selfFalling', 'Adam Cooper'], ['selfFalling2', 'Adam Cooper'], ['selfFalling3', 'Adam Cooper']];
    const add = (key, items) => { if (sb.includes(key)) list.push(...items); };
    add('trogdor', [['trogdor', 'Internet'], ['trogdorEvent', 'Internet']]);
    add('nyanCat', [['nyanCat1', 'Audrey Wu'], ['nyanCat', 'Audrey Wu'], ['nyanCat3', 'Audrey Wu'], ['nyanCat2', 'Audrey Wu']]);
    add('airplane', [['airplane', 'Connie Dai'], ['airplane1', 'Connie Dai'], ['boom', 'Connie Dai']]);
    add('shark', [['shark', 'Dan Cushman']]);
    add('bear', [['bear', 'Faith Quist'], ['bearSwipe', 'Faith Quist']]);
    add('car', [['car1', 'Hira Ahmad'], ['car12', 'Hira Ahmad']]);
    add('carpeDiemMachine', [['carpeDiemMachine', 'Adam Cooper'], ['carpeDiem', 'Internet']]);
    add('money', [['money', 'Hira Ahmad']]);
    add('tank', [['tank', 'Internet']]);
    add('cannon', [['bigcannon', 'Internet']]);
    add('sunMachine', [['sunMachine', 'Internet']]);
    add('slingshot', [['slingshot', 'Adam Cooper'], ['slingshotSwoosh', 'Adam Cooper']]);
    if (S.unlockedBoots >= 2) list.push(['moonBoot', 'Adam Cooper']);
    if (S.unlockedBoots >= 3) list.push(['hermesBoot', 'Faith Quist']);
    return list;
  }

  function drawSketchbook() {
    blit('sketchbookBg', 0, 0);
    const entries = sketchbookEntries();
    S.sketchbookSelect = ((S.sketchbookSelect % entries.length) + entries.length) % entries.length;
    const [name, artist] = entries[S.sketchbookSelect];
    let [w, h] = size(name);
    const k = Math.min(1, 420 / h, 800 / w);
    w *= k; h *= k;
    blit(name, W / 2 - w / 2, H / 2 - h / 2, w, h);
    text(artist, W / 2, H - 70, 44, '#0a0c0a', 'center');
    text(`${S.sketchbookSelect + 1} / ${entries.length}   ◀ ▶`, W / 2, H - 28, 20, '#555', 'center');
  }

  // ---------------------------------------------------------------------------
  // Input
  // ---------------------------------------------------------------------------
  const inputQueue = [];

  const KEYMAP = {
    ArrowLeft: 'left', ArrowRight: 'right', ArrowUp: 'up', ArrowDown: 'down',
    Enter: 'enter', ' ': 'space', Escape: 'esc', Backspace: 'esc',
  };

  window.addEventListener('keydown', (e) => {
    if (e.repeat || e.metaKey || e.ctrlKey || e.altKey) return;
    const key = KEYMAP[e.key] || (e.key.length === 1 ? e.key.toLowerCase() : null);
    if (!key) return;
    if (['left', 'right', 'up', 'down', 'space', 'esc'].includes(key)) e.preventDefault();
    inputQueue.push({ type: 'key', key });
  });

  function canvasPoint(e) {
    const rect = canvas.getBoundingClientRect();
    return { x: (e.clientX - rect.left) * (W / rect.width), y: (e.clientY - rect.top) * (H / rect.height) };
  }

  canvas.addEventListener('pointerdown', (e) => {
    e.preventDefault();
    canvas.focus();
    inputQueue.push({ type: 'tap', ...canvasPoint(e) });
  });

  const inside = (p, r) => p.x >= r.x && p.x <= r.x + r.w && p.y >= r.y && p.y <= r.y + r.h;

  /** Keyboard handling — mirrors keyPressed() from the original. */
  function handleKey(key) {
    if (S.firstTime === 'saveMessage') { S.firstTime = true; return; }
    if (key === 'esc') { goBack(); return; }
    if (S.instructions) { nextInstruction(); return; }
    if (key === 'i') { S.instructions = true; S.htpi = 0; return; }
    switch (S.currentScreen) {
      case 'game': gameKey(key); break;
      case 'mainMenu':
        if (key === 'left') S.buttonSelect = (S.buttonSelect + 3) % 4;
        else if (key === 'right') S.buttonSelect = (S.buttonSelect + 1) % 4;
        else if (key === 'enter' || key === 'space') openFromMenu();
        break;
      case 'store':
        if (key === 'p') startGame();
        else if (key === 'up') storeUp();
        else if (key === 'down') storeDown();
        else if (key === 'left') storeLeftRight(-1);
        else if (key === 'right') storeLeftRight(1);
        else if (key === 'enter' || key === 'space') storeEnter();
        break;
      case 'extras':
        if (key === 'right') S.sketchbookSelect += 1;
        else if (key === 'left') S.sketchbookSelect -= 1;
        break;
      case 'options':
        if (key === 'enter' || key === 'space') optionsEnter();
        else if (S.areYouSure) S.areYouSure = false;
        else if (key === 'up') S.optionsSelect = Math.max(0, S.optionsSelect - 1);
        else if (key === 'down') S.optionsSelect = Math.min(OPTIONS.length - 1, S.optionsSelect + 1);
        break;
    }
  }

  function gameKey(key) {
    if (key === 'd') { S.debugMode = !S.debugMode; return; }
    if (S.gameOver) {
      if (key === 'up' || key === 'down') S.gameOverButtonSelect = 1 - S.gameOverButtonSelect;
      else if (key === 'enter' || key === 'space') gameOverChoose(S.gameOverButtonSelect);
      return;
    }
    if (S.launch === 'launchBar') { S.launch = 'angle'; return; }
    if (S.launch === 'angle') { launch(); return; }
    if (key === 'space' && S.boostCount > 0) { boost(); return; }
    if (S.debugMode) {
      const spawn = { c: Car, b: Bear, t: Trogdor, n: NyanCat, m: Money, s: Shark, a: Airplane }[key];
      if (spawn) S.onScreen.push(new spawn());
      if (key === 'enter') { boost(); S.boostCount += 1; }
    }
  }

  /** Mouse / touch handling — maps taps onto the same actions. */
  function handleTap(p) {
    if (S.firstTime === 'saveMessage') { S.firstTime = true; return; }
    if (S.instructions) { nextInstruction(); return; }
    switch (S.currentScreen) {
      case 'mainMenu': {
        const [left, centre, right] = menuLayout();
        if (inside(p, centre)) openFromMenu();
        else if (inside(p, left) || p.x < 150) S.buttonSelect = (S.buttonSelect + 3) % 4;
        else if (inside(p, right) || p.x > W - 150) S.buttonSelect = (S.buttonSelect + 1) % 4;
        break;
      }
      case 'game':
        if (S.gameOver) {
          const i = GAME_OVER_BUTTONS.findIndex((r) => inside(p, r));
          if (i >= 0) gameOverChoose(i);
        } else gameKey('space');
        break;
      case 'store': {
        if (inside(p, STORE_BACK)) { goBack(); break; }
        if (inside(p, STORE_PLAY)) { startGame(); break; }
        // Tap once to select, tap the selected item again to buy/equip.
        const select = (group, idx) => {
          const already = S.storeButtonSelect === group &&
            (group < 5 || (group === 5 ? S.bootButtonSelect : S.cannonButtonSelect) === idx);
          S.storeButtonSelect = group;
          if (group === 5) S.bootButtonSelect = idx;
          if (group === 6) S.cannonButtonSelect = idx;
          if (already) storeEnter();
        };
        for (let i = 0; i < 5; i++) {
          const row = STAT_ROW(i);
          if (inside(p, { x: row.x, y: row.y, w: 620, h: row.h + 4 })) return select(i, 0);
        }
        for (let b = 0; b <= Math.min(S.unlockedBoots, 2); b++) if (inside(p, BOOT_ICON(b))) return select(5, b);
        for (let c = 0; c <= Math.min(S.unlockedCannons, 4); c++) if (inside(p, CANNON_ICON(c))) return select(6, c);
        break;
      }
      case 'extras':
        S.sketchbookSelect += p.x < W / 2 ? -1 : 1;
        break;
      case 'options': {
        if (S.areYouSure) {
          if (inside(p, { x: 300, y: 220, w: 400, h: 140 })) optionsEnter();
          else S.areYouSure = false;
          break;
        }
        const i = optionRows().findIndex((r) => inside(p, r));
        if (i >= 0) {
          if (S.optionsSelect === i) optionsEnter();
          else S.optionsSelect = i;
        }
        break;
      }
    }
  }

  function nextInstruction() {
    if (S.htpi === 7) {
      S.instructions = false;
      S.firstTime = false;
      S.htpi = 0;
    } else S.htpi += 1;
  }

  function openFromMenu() {
    const screen = MENU_SCREENS[S.buttonSelect];
    if (screen === 'game') startGame();
    else S.currentScreen = screen;
  }

  function startGame() {
    S.currentScreen = 'game';
    initGame();
  }

  function gameOverChoose(i) {
    if (i === 1) S.currentScreen = 'store';
    else initGame();
  }

  function goBack() {
    S.areYouSure = false;
    if (S.instructions) { S.instructions = false; S.htpi = 0; return; }
    if (S.currentScreen === 'game' && !S.gameOver && S.launch === false && S.autoSave) save();
    if (S.currentScreen !== 'mainMenu') S.currentScreen = 'mainMenu';
  }

  function processInput() {
    while (inputQueue.length) {
      const ev = inputQueue.shift();
      if (ev.type === 'key') handleKey(ev.key);
      else if (ev.type === 'tap') handleTap(ev);
      else if (ev.type === 'back') goBack();
      else if (ev.type === 'help') {
        if (S.firstTime === 'saveMessage') S.firstTime = true;
        S.instructions = true;
        S.htpi = 0;
      }
    }
  }

  // HTML overlay buttons (handy on touch screens)
  const touchbar = document.getElementById('touchbar');
  document.getElementById('btn-back').addEventListener('click', () => inputQueue.push({ type: 'back' }));
  document.getElementById('btn-help').addEventListener('click', () => inputQueue.push({ type: 'help' }));
  document.getElementById('btn-full').addEventListener('click', () => {
    const stage = document.getElementById('stage');
    if (document.fullscreenElement) document.exitFullscreen?.();
    else (stage.requestFullscreen || stage.webkitRequestFullscreen)?.call(stage);
  });
  if (!document.fullscreenEnabled && !document.webkitFullscreenEnabled) {
    document.getElementById('btn-full').hidden = true;
  }

  window.addEventListener('pagehide', () => { if (S.autoSave && S.levels) save(); });

  // ---------------------------------------------------------------------------
  // Main loop: fixed 30 Hz simulation, matching the original clock.tick(30)
  // ---------------------------------------------------------------------------
  function tick() {
    if (S.currentScreen === 'game') gamePlay();
    S.icons.save.animate();
    S.icons.sketchbook.animate();
    processInput();
    // Per-tick sprite animation (the original advanced these while drawing).
    if (S.currentScreen === 'game' && !S.instructions && !S.gameOver) {
      for (const item of S.onScreen) item.animate();
    }
    redrawAll();
    touchbar.dataset.screen = S.currentScreen;
  }

  let last = 0;
  let acc = 0;
  function frame(now) {
    if (!last) last = now;
    acc += Math.min(now - last, 250);
    last = now;
    let steps = 0;
    while (acc >= TICK_MS && steps < 5) { tick(); acc -= TICK_MS; steps++; }
    if (steps === 5) acc = 0;
    requestAnimationFrame(frame);
  }

  // Exposed for automated tests / tinkering in the console.
  window.PaperLaunch = { state: S, tick, sprites };

  loadImages().then(() => {
    loadSave();
    init();
    document.getElementById('loading').remove();
    canvas.focus();
    requestAnimationFrame(frame);
  }).catch((err) => {
    document.getElementById('loading').textContent = 'Failed to load: ' + err.message;
  });
})();
