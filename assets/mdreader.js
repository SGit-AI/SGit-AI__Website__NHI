/* nhi.sgit.ai — in-page markdown reader.
   Renders the raw markdown file named by #mdread[data-src] into the page using
   marked (loaded from CDN before this script). The raw file stays the source of
   truth; this is presentation only. Any failure falls back to a link to the raw
   file, so the document is always reachable. */
(function () {
  var el = document.getElementById('mdread');
  if (!el) return;
  var src = el.getAttribute('data-src');
  function fail() {
    el.innerHTML = '<p class="dim">Could not render the document in-page — ' +
      '<a href="' + src + '">open the raw markdown</a> instead.</p>';
  }
  el.innerHTML = '<p class="dim">Loading the document…</p>';
  fetch(src).then(function (r) {
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.text();
  }).then(function (t) {
    if (!window.marked) return fail();
    el.innerHTML = marked.parse(t);
  }).catch(fail);
})();
