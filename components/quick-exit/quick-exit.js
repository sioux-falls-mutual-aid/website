(function () {
  function leave() {
    var a = document.querySelector(".quick-exit-link");
    if (!a) { return; }
    try { window.location.replace(a.href); }
    catch (err) { window.location.href = a.href; }
  }

  var links = document.querySelectorAll(".quick-exit-link");
  for (var i = 0; i < links.length; i++) {
    links[i].addEventListener("click", function (e) {
      e.preventDefault();
      leave();
    });
  }

  var lastEsc = 0;
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") { return; }
    var t = e.target;
    if (t) {
      var tn = t.tagName;
      if (tn === "INPUT") { return; }
      if (tn === "TEXTAREA") { return; }
      if (tn === "SELECT") { return; }
      if (t.isContentEditable) { return; }
    }
    var now = Date.now();
    if (now - lastEsc < 1500) { lastEsc = 0; leave(); }
    else { lastEsc = now; }
  });
})();
