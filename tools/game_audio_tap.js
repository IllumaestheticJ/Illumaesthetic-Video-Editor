// Init script for tools/game_driver.js (--init): mirrors whatever a page plays into a MediaStream so the
// recorder can capture game audio. Every AudioContext gets a MediaStreamAudioDestinationNode, and any node
// connected to the context's speakers is connected to that node as well.
(() => {
  const taps = (window.__audioTaps = []);
  const tapFor = (ctx) => {
    let t = taps.find((x) => x.ctx === ctx);
    if (!t) { t = { ctx, dest: ctx.createMediaStreamDestination() }; taps.push(t); }
    return t;
  };
  const connect = AudioNode.prototype.connect;
  AudioNode.prototype.connect = function (target, ...rest) {
    const r = connect.call(this, target, ...rest);
    try {
      if (target && target === this.context.destination && typeof this.context.createMediaStreamDestination === 'function') {
        connect.call(this, tapFor(this.context).dest);
      }
    } catch (e) { /* offline contexts have no stream destination */ }
    return r;
  };
})();
