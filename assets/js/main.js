/**
* Template Name: Clinic
* Template URL: https://bootstrapmade.com/clinic-bootstrap-template/
* Updated: Jul 23 2025 with Bootstrap v5.3.7
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', mobileNavToogle);
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Set the active nav link based on the current page URL
   */
  function setActiveNavLink() {
    const navLinks = document.querySelectorAll('#navmenu a');
    if (!navLinks.length) return;

    const currentPage = window.location.pathname.split('/').pop().toLowerCase() || 'index.html';

    function getNavTarget(page) {
      if (page === '' || page === 'index.html') {
        return 'index.html';
      }
      if (page === 'privacy.html' || page === 'terms.html' || page === 'privacy-terms.html') {
        return 'privacy-terms.html';
      }
      if (page === 'department-details.html' || page.startsWith('department-')) {
        return 'departments.html';
      }
      if (page === 'service-details.html' || page.startsWith('service-')) {
        return 'services.html';
      }
      return page;
    }

    const targetHref = getNavTarget(currentPage);

    navLinks.forEach(navLink => {
      navLink.classList.remove('active');
      const href = navLink.getAttribute('href')?.split('/').pop().toLowerCase();
      if (href === targetHref) {
        navLink.classList.add('active');
      }
    });
  }

  setActiveNavLink();

  /**
   * Auto-append department query to appointment links on department/service pages
   */
  function fixAppointmentLinksForCurrentPage() {
    const pageName = window.location.pathname.split('/').pop().toLowerCase();
    const departmentPages = {
      'department-cardiology.html': 'cardiology',
      'department-dental.html': 'dental',
      'department-dermatology.html': 'dermatology',
      'department-details.html': 'general',
      'department-neurology.html': 'neurology',
      'department-oncology.html': 'oncology',
      'department-ophthalmology.html': 'ophthalmology',
      'department-orthopedics.html': 'orthopedics',
      'department-pediatrics.html': 'pediatrics'
    };
    const servicePages = {
      'service-details.html': 'general',
      'service-emergency-care.html': 'general',
      'service-laboratory-testing.html': 'general',
      'service-medical-imaging.html': 'general',
      'service-mental-health.html': 'psychiatry',
      'service-pharmacy-services.html': 'general',
      'service-physiotherapy.html': 'orthopedics',
      'service-telemedicine.html': 'general',
      'service-wellness-programs.html': 'general'
    };

    const targetDept = departmentPages[pageName] || servicePages[pageName];
    if (!targetDept) return;

    document.querySelectorAll('a[href^="appointment.html"]').forEach(link => {
      const href = link.getAttribute('href');
      if (!href) return;

      const [path, query = ''] = href.split('?');
      if (path !== 'appointment.html' && path !== './appointment.html') return;
      const params = new URLSearchParams(query);
      if (params.get('department')) return;

      params.set('department', targetDept);
      link.setAttribute('href', `appointment.html?${params.toString()}`);
    });
  }

  fixAppointmentLinksForCurrentPage();

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Frequently Asked Questions Toggle
   */
  document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle, .faq-item .faq-header').forEach((faqItem) => {
    faqItem.addEventListener('click', () => {
      faqItem.parentNode.classList.toggle('faq-active');
    });
  });

})();