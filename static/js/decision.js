/* startupltc — decision sheet.
   Twenty-five checks across five layers, plus fifteen global stop conditions.
   State lives in localStorage on this device only; there is no server. */

(function () {
  "use strict";

  var KEY = "ltc-startup-decision-v1";
  var MAX_LAYER = 5;

  var load = function () {
    try {
      var raw = window.localStorage.getItem(KEY);
      if (!raw) return { checks: [], stops: [] };
      var data = JSON.parse(raw);
      return {
        checks: Array.isArray(data.checks) ? data.checks : [],
        stops: Array.isArray(data.stops) ? data.stops : []
      };
    } catch (err) {
      return { checks: [], stops: [] };
    }
  };

  var save = function (state) {
    try {
      window.localStorage.setItem(KEY, JSON.stringify(state));
    } catch (err) {
      /* private mode or storage disabled: the sheet still works for this visit */
    }
  };

  var init = function () {
    var sheet = document.querySelector("[data-sheet]");
    if (!sheet) return;

    var layers = Array.prototype.slice.call(
      sheet.querySelectorAll(".sheet-layer[data-layer]")
    ).filter(function (el) {
      return el.getAttribute("data-layer") !== "6";
    });

    var checkBoxes = Array.prototype.slice.call(sheet.querySelectorAll("input[data-check]"));
    var stopBoxes = Array.prototype.slice.call(sheet.querySelectorAll("input[data-stop]"));
    var progress = sheet.querySelector("[data-progress]");
    var bar = sheet.querySelector("[data-bar]");
    var verdict = sheet.querySelector("[data-verdict]");
    var reset = sheet.querySelector("[data-sheet-reset]");

    var state = load();

    var checkedIds = function (boxes) {
      return boxes.filter(function (b) { return b.checked; }).map(function (b) {
        return b.getAttribute("data-check") || b.getAttribute("data-stop");
      });
    };

    var hydrate = function () {
      var lookup = {};
      state.checks.forEach(function (id) { lookup[id] = true; });
      var stopLookup = {};
      state.stops.forEach(function (id) { stopLookup[id] = true; });
      checkBoxes.forEach(function (b) {
        b.checked = !!lookup[b.getAttribute("data-check")];
      });
      stopBoxes.forEach(function (b) {
        b.checked = !!stopLookup[b.getAttribute("data-stop")];
      });
    };

    var persist = function () {
      state.checks = checkedIds(checkBoxes);
      state.stops = checkedIds(stopBoxes);
      save(state);
    };

    var render = function () {
      var cleared = layers.filter(function (layer) {
        var boxes = Array.prototype.slice.call(layer.querySelectorAll("input[data-check]"));
        return boxes.length > 0 && boxes.every(function (b) { return b.checked; });
      }).length;

      var stopsHit = checkedIds(stopBoxes).length;

      if (progress) {
        progress.textContent = cleared + " of " + MAX_LAYER + " layers cleared" +
          (stopsHit ? " \u00b7 " + stopsHit + " stop condition" + (stopsHit === 1 ? "" : "s") : "");
      }
      if (bar) bar.style.width = (cleared / MAX_LAYER) * 100 + "%";

      if (!verdict) return;
      verdict.hidden = false;

      if (stopsHit) {
        verdict.className = "sheet-verdict verdict result-no";
        verdict.innerHTML =
          "<h2>Stop here</h2>" +
          "<p>At least one stop condition is ticked. Under the framework this plan ends at that point, " +
          "whatever the other layers say \u2014 and finding that out now is cheaper than finding it out after " +
          "the capital is paid in.</p>" +
          '<p class="quiz-sub">Usually the fix is a different route, not a different structure: ' +
          '<a href="/guides/do-you-need-a-china-entity/">no entity</a>, ' +
          '<a href="/guides/negative-list/">a licensing or distribution arrangement</a>, or a different market.</p>';
        return;
      }

      if (cleared === MAX_LAYER) {
        verdict.className = "sheet-verdict verdict result-yes";
        verdict.innerHTML =
          "<h2>All five layers cleared on paper</h2>" +
          "<p>That is the point to spend money on advice \u2014 not to decide whether to start, but to have " +
          "a lawyer review the structure, the address and the sector licence before anything is filed.</p>" +
          '<p class="quiz-sub">Still open: <a href="/guides/opening-a-corporate-bank-account/">the bank</a>, ' +
          '<a href="/guides/annual-compliance-calendar/">the compliance calendar</a>, and ' +
          '<a href="/guides/repatriating-profits-from-china/">how the money leaves</a>.</p>';
        return;
      }

      verdict.className = "sheet-verdict verdict result-maybe";
      var next = layers[cleared] || layers[0];
      var nextName = next ? next.getAttribute("data-name") : "";
      var nextSlug = next ? next.getAttribute("data-slug") : "";
      verdict.innerHTML =
        "<h2>" + cleared + " of " + MAX_LAYER + " layers cleared</h2>" +
        "<p>The next layer to settle is <strong>" + (nextName || "the next one") + "</strong>. " +
        "Do not move on to it until the current layer is genuinely answered \u2014 a structure chosen on an " +
        "unchecked access rule is the most expensive mistake in this process.</p>" +
        (nextSlug
          ? '<p class="quiz-sub"><a href="/framework/' + nextSlug + '/">Read layer ' +
            next.getAttribute("data-layer") + "</a> \u00b7 " +
            '<a href="/framework/decision-sheet/">Clear the sheet</a></p>'
          : "");
    };

    hydrate();
    render();

    sheet.addEventListener("change", function (event) {
      var t = event.target;
      if (t && t.matches && t.matches("input[data-check], input[data-stop]")) {
        persist();
        render();
      }
    });

    if (reset) {
      reset.addEventListener("click", function () {
        state = { checks: [], stops: [] };
        try { window.localStorage.removeItem(KEY); } catch (err) { /* ignore */ }
        hydrate();
        render();
      });
    }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
