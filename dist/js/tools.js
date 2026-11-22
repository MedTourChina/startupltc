/* startupltc — browser tools: vehicle chooser, first-year cost, repatriation.
   Everything runs locally. No network calls, no storage, no analytics. */

(function () {
  "use strict";

  var money = function (n) {
    if (!isFinite(n)) return "\u2014";
    return "\u00a5" + Math.round(n).toLocaleString("en-US");
  };

  var range = function (lo, hi) {
    return money(lo) + "\u2013" + money(hi).replace("\u00a5", "");
  };

  var $ = function (root, sel) { return root.querySelector(sel); };
  var $$ = function (root, sel) {
    return Array.prototype.slice.call(root.querySelectorAll(sel));
  };

  var out = function (root, key) { return $('[data-out="' + key + '"]', root); };
  var setOut = function (root, key, text) {
    var el = out(root, key);
    if (el) el.textContent = text;
  };

  var readNum = function (root, key, fallback) {
    var el = $('[data-in="' + key + '"]', root);
    if (!el) return fallback;
    var v = parseFloat(el.value);
    return isFinite(v) && v >= 0 ? v : fallback;
  };

  var readVal = function (root, key) {
    var el = $('[data-in="' + key + '"]', root);
    return el ? el.value : "";
  };

  /* ---------------------------------------------------------- structure quiz */

  var structure = function (form) {
    var result = $("[data-quiz-result]", form);
    if (!result) return;

    var names = ["job", "access", "control", "exit", "staff", "when"];
    var answers = {};
    var missing = 0;

    names.forEach(function (name) {
      var picked = $('input[name="' + name + '"]:checked', form);
      if (picked) answers[name] = picked.value;
      else missing += 1;
    });

    if (missing) {
      result.hidden = false;
      result.className = "quiz-result verdict result-maybe";
      result.innerHTML =
        "<h2>Answer all six first</h2>" +
        "<p>There are still " + missing + " question" + (missing === 1 ? "" : "s") +
        " without an answer. Half an answer gives a misleading vehicle.</p>";
      return;
    }

    var kind = "maybe";
    var title = "No entity yet \u2014 and that may be correct";
    var lead = "";
    var points = [];
    var links = [];

    if (answers.access === "closed") {
      kind = "no";
      title = "This activity is closed to foreign investment";
      lead = "A Chinese company will not be licensed for it. The realistic routes are a licence from the Chinese holder, an import/distribution arrangement, or a different market.";
      points.push("The foreign investment negative list, 2024 edition, prohibits the activity outright.");
      points.push("A nominee or VIE structure does not change the licence position and creates a control risk you cannot enforce in a Chinese court.");
      links.push(["Read the negative list guide", "/guides/negative-list/"]);
    } else if (answers.job === "nothing") {
      kind = "yes";
      title = "Do not register anything yet";
      lead = "Selling before you incorporate is usually the cheaper sequence: test demand with an importer, a cross-border platform or a licensing deal, and register when one of the five entity-only jobs appears.";
      points.push("Register an entity when you need domestic fapiao, local payroll, a sector licence, a lease in a company name, or RMB receipts from Chinese customers.");
      points.push("A company that exists and does nothing still files, audits and pays for an address every year.");
      links.push(["Do you need an entity at all?", "/guides/do-you-need-a-china-entity/"]);
      links.push(["What year one costs", "/tools/setup-cost/"]);
    } else if (answers.job === "liaison") {
      if (answers.access === "restricted") {
        kind = "maybe";
        title = "Representative office \u2014 unless the licence says otherwise";
        lead = "A representative office cannot invoice or employ local staff directly, which usually fails the restricted-sector licence test. Check the sector rule before choosing it.";
        links.push(["WFOE / JV / RO compared", "/guides/wfoe-jv-roe-comparison/"]);
      } else {
        kind = "yes";
        title = "Representative office, or nothing at all";
        lead = "For coordination, quality control or market research, a representative office is the leanest registered presence. It cannot invoice Chinese customers, and it employs staff through a dispatch agency.";
        points.push("An RO has no registered capital and no profit distribution, but it does have an annual audit and a filing obligation.");
        points.push("If the parent already has a Chinese distributor, an RO is often unnecessary.");
        links.push(["WFOE / JV / RO compared", "/guides/wfoe-jv-roe-comparison/"]);
      }
    } else if (answers.access === "restricted") {
      kind = "maybe";
      title = "Joint venture \u2014 the partner is the licence";
      lead = "The activity requires Chinese ownership, a Chinese partner, or both. The structure follows the licence condition, not the other way round.";
      points.push("The joint venture agreement and the articles decide control: board seats, reserved matters, deadlock, and how a partner exits.");
      points.push("A minority position with strong reserved matters is often better than 51% with a partner who controls the licence and the bank.");
      if (answers.control === "full") points.push("You said you need 100% control. In a restricted sector that is usually not available \u2014 decide now whether shared control is acceptable.");
      links.push(["WFOE / JV / RO compared", "/guides/wfoe-jv-roe-comparison/"]);
      links.push(["Check your sector", "/sectors/"]);
    } else if (answers.job === "licence") {
      kind = "maybe";
      title = "WFOE \u2014 but the licence, not the company, is the gate";
      lead = "Register the company only after the sector regulator has confirmed in writing what it will license. A business licence without the sector licence is a company that cannot trade.";
      points.push("Licensed sectors add premises, staff qualifications and inspection timelines to the registration.");
      links.push(["Check your sector", "/sectors/"]);
      links.push(["Registered address guide", "/guides/registered-address-in-china/"]);
    } else {
      kind = "yes";
      title = "Wholly foreign-owned enterprise (WFOE)";
      lead = "The activity is open, you need to invoice or employ locally, and you want full control: a WFOE is the default vehicle. If you are unsure about the list, verify it before you file.";
      points.push("Registered capital is subscribed, not paid up front, but the five-year paid-in rule starts at incorporation.");
      links.push(["WFOE / JV / RO compared", "/guides/wfoe-jv-roe-comparison/"]);
      links.push(["Registered capital and the five-year rule", "/guides/registered-capital-five-year-rule/"]);
    }

    if (answers.exit === "yes" && kind !== "no") {
      points.push("You plan to raise or sell within five years: an offshore holding company above the WFOE is usually worth setting up before the first financing round, not after.");
      links.push(["Hong Kong holding company", "/guides/hong-kong-holding-company/"]);
    }

    if (answers.when === "now" && kind !== "no") {
      points.push("Three months is realistic for an open-sector WFOE in a tier-one city only if the address and the bank introduction are already lined up.");
    }

    if (answers.staff === "many" && kind !== "no") {
      points.push("With three or more local employees, payroll, social insurance and the employment contract process become a monthly obligation from the first hire.");
      links.push(["Hiring your first employee", "/guides/hiring-first-employee-china/"]);
    }

    var cls = kind === "yes" ? "result-yes" : kind === "no" ? "result-no" : "result-maybe";
    var html = "<h2>" + title + "</h2><p>" + lead + "</p>";
    if (points.length) {
      html += "<ul>" + points.map(function (p) { return "<li>" + p + "</li>"; }).join("") + "</ul>";
    }
    if (links.length) {
      html += '<p class="quiz-sub">Next: ' + links.map(function (l) {
        return '<a href="' + l[1] + '">' + l[0] + "</a>";
      }).join(" \u00b7 ") + "</p>";
    }
    html += '<p class="quiz-sub">This is a route, not a permission. The registry and the sector regulator decide.</p>';

    result.hidden = false;
    result.className = "quiz-result verdict " + cls;
    result.innerHTML = html;
    result.scrollIntoView({ behavior: "smooth", block: "nearest" });
  };

  /* ------------------------------------------------------------ setup cost */

  var setup = function (root) {
    var factor = 0.8;
    var citySel = $('[data-in="city"]', root);
    if (citySel && citySel.options[citySel.selectedIndex]) {
      var f = parseFloat(citySel.options[citySel.selectedIndex].getAttribute("data-factor"));
      if (isFinite(f) && f > 0) factor = f;
    }

    var address = readVal(root, "address");
    var staff = Math.round(readNum(root, "staff", 0));
    var salary = readNum(root, "salary", 0);
    var audit = readVal(root, "audit") === "yes";

    var addressBands = {
      virtual: [3500, 8000],
      serviced: [9000, 26000],
      office: [30000, 120000]
    };
    var band = addressBands[address] || addressBands.serviced;

    var addressLo = band[0] * factor;
    var addressHi = band[1] * factor;
    var setupLo = 7000;
    var setupHi = 15000;
    var booksLo = 3600 * factor;
    var booksHi = 12000 * factor;
    var auditLo = audit ? 6000 * factor : 0;
    var auditHi = audit ? 18000 * factor : 0;
    var payrollLo = staff * 1200 * factor;
    var payrollHi = staff * 3000 * factor;
    var socialLo = staff * salary * 0.25;
    var socialHi = staff * salary * 0.32;
    var salaryLo = salary * 12;
    var salaryHi = salary * 12;

    var annualLo = addressLo + booksLo + auditLo + payrollLo + socialLo + salaryLo;
    var annualHi = addressHi + booksHi + auditHi + payrollHi + socialHi + salaryHi;
    var bufferLo = annualLo * 0.25;
    var bufferHi = annualHi * 0.25;
    var totalLo = setupLo + annualLo + bufferLo;
    var totalHi = setupHi + annualHi + bufferHi;

    var totalEl = out(root, "total");
    if (totalEl) totalEl.textContent = range(totalLo, totalHi);
    setOut(root, "setup", range(setupLo, setupHi));
    setOut(root, "address", range(addressLo, addressHi));
    setOut(root, "books", range(booksLo, booksHi));
    setOut(root, "audit", audit ? range(auditLo, auditHi) : "\u2014");
    setOut(root, "payroll", staff ? range(payrollLo, payrollHi) : "\u2014");
    setOut(root, "social", staff ? range(socialLo, socialHi) : "\u2014");
    setOut(root, "salary", range(salaryLo, salaryHi));
    setOut(root, "buffer", range(bufferLo, bufferHi));

    var note = "A " + (factor >= 1 ? "tier-one" : factor >= 0.8 ? "second-tier" : "lower-cost") +
      " city (factor " + factor.toFixed(1) + "). Audit " + (audit ? "included" : "excluded") +
      ". Social insurance is charged on your salary for each local employee; actual bases are set by the city.";
    if (staff === 0) note += " With no local employees, payroll and employer social insurance are zero.";
    setOut(root, "note", note);
  };

  /* ---------------------------------------------------------- repatriation */

  var repat = function (root) {
    var profit = readNum(root, "profit", 0);
    var citRate = parseFloat(readVal(root, "cit")) / 100;
    var whtRate = parseFloat(readVal(root, "wht")) / 100;
    var reserve = readVal(root, "reserve") === "yes";
    var route = readVal(root, "route");

    var cit = profit * citRate;
    var afterCit = profit - cit;
    var reserveAmt = reserve ? afterCit * 0.10 : 0;
    var dist = afterCit - reserveAmt;

    var vat = 0;
    var whtBase = dist;
    if (route !== "dividend") {
      vat = dist * 0.06 * 1.12;      /* 6% VAT + 12% surcharges */
      whtBase = dist;
    }
    var wht = whtBase * whtRate;
    var net = dist - vat - wht;
    var effective = profit > 0 ? (profit - net) / profit : 0;

    var totalEl = out(root, "net");
    if (totalEl) totalEl.textContent = money(net);
    setOut(root, "cit", money(cit));
    setOut(root, "reserve", reserve ? money(reserveAmt) : "\u2014");
    setOut(root, "dist", money(dist));
    setOut(root, "wht", money(wht));
    setOut(root, "vat", vat > 0 ? money(vat) : "\u2014");
    setOut(root, "effective", (effective * 100).toFixed(1) + "%");

    var notes = {
      dividend: "A dividend is paid out of after-tax profit. The withholding tax applies to the distribution; treaty relief needs a residence certificate and, for the 5% Hong Kong rate, at least 25% ownership and substance in Hong Kong.",
      royalty: "A royalty is a deductible expense for the Chinese company, so the corporate tax picture differs from this model \u2014 the figure here treats the payment as a distribution of already-taxed profit, which overstates the tax if the royalty is at arm's length. Withholding tax and 6% VAT still apply.",
      service: "A service fee is deductible if it is at arm's length and documented. This model treats it as a distribution, which is the conservative case; VAT and withholding tax apply.",
      interest: "Interest on a shareholder loan is deductible within thin-capitalisation limits (generally 2:1 debt-to-equity for non-financial companies). This model treats it as a distribution; VAT and withholding tax apply."
    };

    setOut(root, "note", notes[route] || notes.dividend);
  };

  /* --------------------------------------------------------------- wiring */

  var init = function () {
    $$('[data-quiz="structure"]').forEach(function (form) {
      var run = $("[data-quiz-run]", form);
      if (run) run.addEventListener("click", function () { structure(form); });
    });

    $$('[data-calc="setup"]').forEach(function (root) {
      var update = function () { setup(root); };
      $$("input, select", root).forEach(function (el) {
        el.addEventListener("input", update);
        el.addEventListener("change", update);
      });
      update();
    });

    $$('[data-calc="repat"]').forEach(function (root) {
      var update = function () { repat(root); };
      $$("input, select", root).forEach(function (el) {
        el.addEventListener("input", update);
        el.addEventListener("change", update);
      });
      update();
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
