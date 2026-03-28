/**

*/

(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function(e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  
  

  /**
   * Initiate Datatables
   */
  const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable, {
      perPageSelect: [5, 10, 15, 25, 50, 75, 100, ["All", -1]],
      columns: [
        {
          select: 2,
          sortSequence: ["desc", "asc"],
        },
        {
          select: 3,
          sortSequence: ["desc", "asc"],
        },
        {
          select: 4,
          cellClass: "green",
          headerClass: "red",
        },
      ],
    });
  })

  (function () {
  "use strict";

  // ── Mobile nav toggle ──────────────────────────────────────────
  var navBtn   = document.querySelector('.nav-button-wrap');
  var mainMenu = document.querySelector('.main-menu');

  if (navBtn && mainMenu) {
    navBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      mainMenu.classList.toggle('vismobmenu');
      navBtn.classList.toggle('menu-open');
    });
  }

  // Close when clicking outside
  document.addEventListener('click', function (e) {
    if (mainMenu && !mainMenu.contains(e.target) && navBtn && !navBtn.contains(e.target)) {
      mainMenu.classList.remove('vismobmenu');
      navBtn.classList.remove('menu-open');
    }
  });

  // ── Mobile dropdown (ಜಿಲ್ಲಾ submenu) ─────────────────────────
  var dropdownLinks = document.querySelectorAll('.menusb li.dropdown > a');
  dropdownLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      if (window.innerWidth <= 1064) {
        e.preventDefault();
        var parentLi = this.parentElement;
        var sub = parentLi.querySelector('ul');
        var isOpen = parentLi.classList.contains('open-sub');

        // Close all other open submenus
        document.querySelectorAll('.menusb li.dropdown.open-sub').forEach(function (el) {
          el.classList.remove('open-sub');
          var s = el.querySelector('ul');
          if (s) s.style.maxHeight = null;
        });

        if (!isOpen && sub) {
          parentLi.classList.add('open-sub');
          sub.style.maxHeight = sub.scrollHeight + 'px';
        }
      }
    });
  });

  // ── Desktop nav hover (already handled by CSS, but ensure active link) ──
  var currentPath = window.location.pathname + window.location.search;
  document.querySelectorAll('.nav-holder nav li a, .menusb li a').forEach(function (a) {
    if (a.getAttribute('href') === currentPath) {
      a.classList.add('act-link');
    }
  });

  // ── Progress bar on scroll ──────────────────────────────────────
  window.addEventListener('scroll', function () {
    var scrollTop  = document.documentElement.scrollTop || document.body.scrollTop;
    var scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var progress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
    var bar = document.querySelector('.progress-bar');
    if (bar) bar.style.width = progress + '%';
  });

  // ── Search toggle ───────────────────────────────────────────────
  var searchBtn  = document.querySelector('.show_search-btn');
  var searchWrap = document.querySelector('.header-search-wrap');
  if (searchBtn && searchWrap) {
    searchBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      searchWrap.classList.toggle('vis-search');
      searchBtn.classList.toggle('scwllink2');
    });
    document.addEventListener('click', function (e) {
      if (!searchWrap.contains(e.target) && !searchBtn.contains(e.target)) {
        searchWrap.classList.remove('vis-search');
        searchBtn.classList.remove('scwllink2');
      }
    });
  }

  // ── Date/time display ───────────────────────────────────────────
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var now = new Date();
  var numEl   = document.querySelector('.date_num');
  var monEl   = document.querySelector('.date_mounth');
  var yearEl  = document.querySelector('.date_year');
  var timeEl  = document.getElementById('time');
  if (numEl)  numEl.textContent  = now.getDate();
  if (monEl)  monEl.textContent  = months[now.getMonth()];
  if (yearEl) yearEl.textContent = now.getFullYear();
  function updateTime() {
    var t = new Date();
    var h = String(t.getHours()).padStart(2,'0');
    var m = String(t.getMinutes()).padStart(2,'0');
    if (timeEl) timeEl.textContent = h + ':' + m;
  }
  updateTime();
  setInterval(updateTime, 60000);

})();
  


