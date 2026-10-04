// Runs the shipped inline script with deterministic clocks, DOM, and audio inputs.
// Device microphone quality and browser audio policies still need phone testing.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8').match(/<script>([\s\S]*?)<\/script>/)[1];

function setup() {
  let now = 1000, sequence = 0;
  const elements = new Map(), events = {}, frames = new Map(), timers = new Map(), storage = new Map();
  function element(id) {
    const classes = new Set();
    return {
      offsetWidth: 130, textContent: '', hidden: false, disabled: false, lang: '',
      style: { display: ['scene', 'errorScreen', 'endScreen'].includes(id) ? 'none' : 'flex', setProperty() {}, removeProperty() {} },
      classList: { add: (...items) => items.forEach(x => classes.add(x)), remove: (...items) => items.forEach(x => classes.delete(x)), contains: x => classes.has(x) },
      addEventListener(type, handler) { this[type] = handler; },
      querySelector: () => element(), querySelectorAll: () => [],
      getBoundingClientRect: () => ({ left: 250, width: 116 }),
      focus() {}, appendChild() {}, setAttribute() {}, remove() {}
    };
  }
  const context = {
    console, Float32Array, URLSearchParams, location: { search: '' },
    performance: { now: () => now },
    document: { hidden: false, getElementById(id) { if (!elements.has(id)) elements.set(id, element(id)); return elements.get(id); }, addEventListener: (type, handler) => events[type] = handler, createElement: () => element() },
    window: { innerWidth: 390, addEventListener: (type, handler) => events[type] = handler },
    navigator: { userAgent: 'Test' },
    localStorage: { getItem: key => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, value) },
    requestAnimationFrame: handler => { frames.set(++sequence, handler); return sequence; },
    cancelAnimationFrame: id => frames.delete(id),
    setTimeout: (handler, delay) => { timers.set(++sequence, { handler, at: now + delay }); return sequence; },
    clearTimeout: id => timers.delete(id), matchMedia: () => ({ matches: false })
  };
  vm.createContext(context);
  vm.runInContext(source, context);
  const run = code => vm.runInContext(code, context);
  return { context, run, elements, events, storage, time: value => now = value,
    tick(value) { now = value; const pending = [...frames.values()]; frames.clear(); pending.forEach(handler => handler(value)); },
    timers(value) { now = value; for (const [id, timer] of timers) if (timer.at <= now) { timers.delete(id); timer.handler(); } }
  };
}
function audio(h, options = {}) {
  const tracks = [{ stopped: false, stop() { this.stopped = true; }, addEventListener(type, handler) { this[type] = handler; } }];
  const stream = { getTracks: () => tracks };
  const contexts = [];
  h.context.window.AudioContext = class {
    constructor() { this.state = 'running'; this.sampleRate = 48000; contexts.push(this); }
    async resume() { this.state = 'running'; this.statechange?.(); }
    async close() { this.state = 'closed'; this.statechange?.(); }
    addEventListener(type, handler) { this[type] = handler; }
    createMediaStreamSource() { if (options.failSource) throw new Error('Source failed'); return { connect() {} }; }
    createAnalyser() { return { fftSize: 2048, getFloatTimeDomainData: data => {
      if (options.failRead) throw new Error('Read failed');
      data.fill(0);
    } }; }
  };
  h.context.navigator.mediaDevices = { getUserMedia: options.getUserMedia || (async () => stream) };
  return { stream, tracks, contexts };
}
const flush = () => new Promise(setImmediate);
async function start(h) { const pending = h.run('startAudio()'); await flush(); h.tick(2100); await pending; }
function meow(h, at, duration, glide = false) {
  h.time(at); h.run(`updateMeowTracking('meow', 300, ${at})`);
  h.time(at + duration / 2); h.run(`updateMeowTracking('meow', ${glide ? 340 : 300}, ${at + duration / 2})`);
  h.time(at + duration); h.run(`updateMeowTracking('silence', -1, ${at + duration})`);
  h.time(at + duration + 100); h.run(`updateMeowTracking('silence', -1, ${at + duration + 100})`);
}
const tests = [
  ['short pitch gap retains one valid meow', h => {
    h.run('startGame(); updateMeowTracking("meow",300,1000); updateMeowTracking("talk",-1,1250); updateMeowTracking("meow",310,1267); updateMeowTracking("silence",-1,1550); updateMeowTracking("silence",-1,1650)');
    assert.equal(h.run('meowCountForScore'), 1); assert.equal(h.run('catPos'), 58);
  }],
  ['separate meows remain separate; cooldown and duration limits hold', h => {
    h.run('startGame()'); meow(h,1000,900); meow(h,2200,900); assert.equal(h.run('meowCountForScore'),2);
    meow(h,3300,100); meow(h,4000,1600); assert.equal(h.run('meowCountForScore'),2);
    meow(h,6000,300); meow(h,6400,300); assert.equal(h.run('meowCountForScore'),3);
  }],
  ['loudness chatter is one scare and sustained quiet rearms', h => {
    h.run('startGame(); minVol=.0015; scareVol=.004');
    for (const [i,v] of [.0041,.0039,.0041,.0039,.0041,.0039,.0041].entries()) h.run(`updateScream(${v},${1000+i*16})`);
    assert.equal(h.run('catPos'),35); h.run('updateScream(.002,1300);updateScream(.002,1600);updateScream(.005,1700)');
    assert.equal(h.run('catPos'),20);
  }],
  ['scream-ending candidate never earns reward or wins', h => {
    h.run('startGame(); minVol=.0015; scareVol=.004; catPos=96; updateMeowTracking("meow",300,1000);updateMeowTracking("meow",310,1400);updateScream(.005,1500);updateMeowTracking("scream",300,1500)');
    assert.equal(h.run('catPos'),81); assert.equal(h.run('meowCountForScore'),0); assert.equal(h.run('gameState'),'playing');
  }],
  ['frame loop enforces deadline before finishing candidate', h => {
    h.run('startGame(); catPos=96; minVol=.0015; scareVol=.004; audioCtx={state:"running",sampleRate:48000,close:async()=>{}}; timeData=new Float32Array(2048); analyser={getFloatTimeDomainData:b=>b.fill(0)}; updateMeowTracking("meow",300,60500);updateMeowTracking("silence",-1,60900)');
    h.time(61000); h.run('frameLoop()'); assert.equal(h.run('gameState'),'lost'); assert.equal(h.run('meowCountForScore'),0);
  }],
  ['completion before deadline still wins', h => {
    h.run('startGame();catPos=96'); meow(h,59500,900); assert.equal(h.run('gameState'),'won'); assert.ok(h.run('finalCompletionTime') < 60);
  }],
  ['win, rank, persistence, language, and audio cleanup', async h => {
    const a=audio(h); await start(h); let at=2200;
    for(let i=0;i<5;i++,at+=1200) meow(h,at,900,true);
    assert.equal(h.run('gameState'),'won'); assert.ok(a.tracks[0].stopped); h.timers(at+1000);
    assert.equal(h.elements.get('endTitle').textContent,'You win! Rank S'); assert.equal(h.elements.get('endMsg').lang,'th');
    assert.ok(h.storage.has('meowme_best_time')); h.run('totalQuality=0;showEndScreen("won",6)');
    assert.equal(h.elements.get('endMsg').lang,'en'); assert.ok(!h.elements.get('rankTip').hidden);
    assert.equal(h.run('rankForScore(CONFIG.rankA)'),'A'); assert.equal(h.run('rankForScore(CONFIG.rankB)'),'B');
    h.storage.set('meowme_best_time','Infinity'); assert.ok(Number.isNaN(h.run('readBestTime()')));
  }],
  ['loss reason distinguishes scares from wandering', h => {
    h.run('startGame();for(let i=0;i<4;i++)applyScream()'); assert.match(h.elements.get('endStats').textContent,/Too loud/);
    h.time(2000);h.run('startGame()');h.time(23000);h.run('gameTick(performance.now())');assert.match(h.elements.get('endStats').textContent,/wandered/);
  }],
  ['background callbacks cannot grant progress; paused timer stays fixed', h => {
    h.run('startGame();audioCtx={state:"running"}');h.time(7000);h.context.document.hidden=true;h.events.visibilitychange();
    h.time(8000);h.run('gameTick(performance.now());renderScene(0)');assert.equal(h.elements.get('timeLeftDisplay').textContent,'54s');
    h.time(9000);h.context.document.hidden=false;h.events.visibilitychange();h.run('gameTick(performance.now())');
    assert.equal(h.run('catPos'),50);assert.equal(h.run('lastTickAt'),9000);
  }],
  ['retry resets cooldown and cancels old animation', h => {
    h.run('startGame()');meow(h,1000,900);h.time(2000);h.run('startGame()');meow(h,2000,300);
    assert.equal(h.run('meowCountForScore'),1);assert.equal(h.run('catPos'),58);
  }],
  ['cat stays within screen at finish and offscreen at loss', h => {
    h.run('catPos=100;positionCat()'); assert.equal(h.elements.get('catWrap').style.left,'243px');
    h.run('catPos=0;positionCat()');assert.equal(h.elements.get('catWrap').style.left,'-130px');
  }],
  ['periodic tones accepted; uncorrelated noise rejected', h => {
    h.run('minVol=.0015;scareVol=.004');
    for(const hz of [155,220,300,590]) {
      h.run(`testTone=Float32Array.from({length:2048},(_,i)=>.003*Math.sin(2*Math.PI*${hz}*i/48000));testPitch=detectPitch(testTone,48000)`);
      assert.ok(Math.abs(h.run('testPitch')-hz)<3); assert.equal(h.run('classify(rms(testTone),testPitch)'),'meow');
    }
    const hits=h.run('seed=12345678;hits=0;for(let j=0;j<100;j++){const b=Float32Array.from({length:2048},()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return ((seed/4294967296)*2-1)*.003});if(classify(rms(b),detectPitch(b,48000))==="meow")hits++}hits');
    assert.equal(hits,0);
  }],
  ['scream frames skip pitch computation', h => {
    h.run('startGame();minVol=.0015;scareVol=.004;audioCtx={state:"running",sampleRate:48000};timeData=new Float32Array(2048);analyser={getFloatTimeDomainData:b=>b.fill(.005)};detectPitch=()=>{throw Error("Unexpected pitch work")};frameLoop()');
    assert.equal(h.run('catPos'),35);
  }],
  ['pending retry remains visible and late permission is cleaned up', async h => {
    let resolve;const a=audio(h,{getUserMedia:()=>new Promise(r=>resolve=r)});
    h.run('startGame();endRound("lost")'); const pending=h.run('startAudio()');await flush();
    assert.equal(h.elements.get('scene').style.display,'block');assert.match(h.elements.get('gameStatus').textContent,/Starting/);
    h.elements.get('restartBtn').click();resolve(a.stream);await pending;
    assert.ok(a.tracks[0].stopped);assert.equal(h.run('gameState'),'landing');assert.equal(h.run('isStarting'),false);
  }],
  ['cancelling calibration permits clean restart', async h => {
    audio(h);const pending=h.run('startAudio()');await flush();assert.equal(h.run('gameState'),'calibrating');
    h.elements.get('restartBtn').click();await pending;await start(h);assert.equal(h.run('gameState'),'playing');
  }],
  ['stale permission cannot overwrite a newer attempt', async h => {
    let resolve;const old=audio(h,{getUserMedia:()=>new Promise(r=>resolve=r)});
    const pending=h.run('startAudio()');await flush();h.elements.get('restartBtn').click();audio(h);await start(h);
    resolve(old.stream);await pending;assert.ok(old.tracks[0].stopped);assert.equal(h.run('gameState'),'playing');assert.equal(h.run('isStarting'),false);
  }],
  ['source and calibration failures show recoverable errors', async h => {
    audio(h,{failSource:true});await h.run('startAudio()');assert.equal(h.elements.get('errorTitle').textContent,'Mic trouble');assert.equal(h.run('isStarting'),false);
    h.elements.get('retryBtn').click();audio(h,{failRead:true});await h.run('startAudio()');assert.equal(h.run('gameState'),'error');assert.equal(h.run('isStarting'),false);
    h.elements.get('retryBtn').click();audio(h);await start(h);assert.equal(h.run('gameState'),'playing');
  }],
  ['denied, missing, busy, and unsupported mic have distinct guidance', async h => {
    for(const [name,title] of [['NotAllowedError','Mic access denied'],['NotFoundError','No microphone found'],['NotReadableError','Mic unavailable']]) {
      audio(h,{getUserMedia:async()=>{throw Object.assign(Error(name),{name});}});await h.run('startAudio()');assert.equal(h.elements.get('errorTitle').textContent,title);h.elements.get('retryBtn').click();
    }
    h.context.navigator.mediaDevices=undefined;await h.run('startAudio()');assert.equal(h.elements.get('errorTitle').textContent,'No mic support');assert.equal(h.elements.get('copyLinkBtn').style.display,'inline-block');
  }],
  ['track loss stops round instead of penalizing silence', async h => {
    const a=audio(h);await start(h);a.tracks[0].ended();assert.equal(h.run('gameState'),'error');assert.equal(h.elements.get('errorTitle').textContent,'Mic disconnected');assert.ok(a.tracks[0].stopped);
  }],
  ['suspended mic pauses, user gesture resumes without time penalty', async h => {
    const a=audio(h);await start(h);h.time(3100);a.contexts[0].state='suspended';a.contexts[0].statechange();
    assert.equal(h.elements.get('resumeBtn').hidden,false);h.time(7100);h.run('gameTick(performance.now())');
    await h.elements.get('resumeBtn').click();assert.equal(h.run('pauseStartedAt'),0);assert.equal(h.run('roundStartAt'),6100);assert.equal(h.run('catPos'),50);
  }],
  ['calibration interrupted by backgrounding recovers', async h => {
    audio(h);const pending=h.run('startAudio()');await flush();h.context.document.hidden=true;h.events.visibilitychange();await pending;
    assert.equal(h.run('gameState'),'error');assert.equal(h.run('isStarting'),false);
  }]
];
(async()=>{for(const [name,test] of tests){await test(setup());console.log(`PASS ${name}`);}console.log(`${tests.length} regression checks passed.`);})().catch(error=>{console.error(error);process.exitCode=1;});
