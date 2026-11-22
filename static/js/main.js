/* Site chrome: sticky header state, mobile navigation, table of contents
   highlighting. There are no forms on this site, so there is no submission
   logic here. */
(function () {
  'use strict';

  var header = document.querySelector('[data-header]');
  var toggle = document.querySelector('.nav-toggle');

  // Header gains a border once the page has scrolled.
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Mobile navigation
  if (header && toggle) {
    var setOpen = function (open) {
      header.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      var openIcon = toggle.querySelector('[data-icon-open]');
      var closeIcon = toggle.querySelector('[data-icon-close]');
      if (openIcon) openIcon.hidden = open;
      if (closeIcon) closeIcon.hidden = !open;
    };

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });

    document.addEventListener('click', function (e) {
      if (!header.classList.contains('is-open')) return;
      if (!header.contains(e.target)) setOpen(false);
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 860) setOpen(false);
    });
  }

  // Table of contents: highlight the section currently in view.
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  if (tocLinks.length) {
    var targets = tocLinks
      .map(function (link) {
        var id = link.getAttribute('href').slice(1);
        var el = document.getElementById(id);
        return el ? { link: link, el: el } : null;
      })
      .filter(Boolean);

    if (targets.length && 'IntersectionObserver' in window) {
      var visible = new Set();

      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) visible.add(entry.target.id);
            else visible.delete(entry.target.id);
          });

          var active = targets.find(function (t) {
            return visible.has(t.el.id);
          });

          tocLinks.forEach(function (l) {
            l.classList.remove('is-active');
          });
          if (active) active.link.classList.add('is-active');
        },
        { rootMargin: '-96px 0px -65% 0px', threshold: 0 }
      );

      targets.forEach(function (t) {
        observer.observe(t.el);
      });
    }
  }
})();
