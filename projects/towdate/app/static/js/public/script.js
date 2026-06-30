

// Navigation scroll effect
const navbar = document.getElementById('navbar');
if (navbar) {
   window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
         navbar.classList.add('scrolled');
      } else {
         navbar.classList.remove('scrolled');
      }
   });
}

// Mobile Menu
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');
const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
const mobileMenuClose = document.getElementById('mobileMenuClose');
const mobileNavLinks = document.querySelectorAll('.mobile-nav-links a');

function openMobileMenu() {
   if (!mobileMenu || !mobileMenuOverlay || !mobileMenuBtn) return;
   mobileMenu.classList.add('open');
   mobileMenuOverlay.classList.add('open');
   mobileMenuBtn.classList.add('active');
   document.body.classList.add('menu-open');
}

function closeMobileMenu() {
   if (!mobileMenu || !mobileMenuOverlay || !mobileMenuBtn) return;
   mobileMenu.classList.remove('open');
   mobileMenuOverlay.classList.remove('open');
   mobileMenuBtn.classList.remove('active');
   document.body.classList.remove('menu-open');
}

if (mobileMenuBtn && mobileMenuClose && mobileMenuOverlay) {
   mobileMenuBtn.addEventListener('click', openMobileMenu);
   mobileMenuClose.addEventListener('click', closeMobileMenu);
   mobileMenuOverlay.addEventListener('click', closeMobileMenu);
}

// Close mobile menu when clicking a link
mobileNavLinks.forEach(link => {
   link.addEventListener('click', () => {
      closeMobileMenu();
   });
});

// Close mobile menu on escape key
document.addEventListener('keydown', (e) => {
   if (e.key === 'Escape') {
      closeMobileMenu();
   }
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
   anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (!href || href === '#') {
         return;
      }

      let target = null;
      try {
         target = document.querySelector(href);
      } catch (_) {
         target = null;
      }

      if (!target) {
         return;
      }

      e.preventDefault();
      if (target) {
         target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
         });
      }
   });
});

// Login password toggle
const loginPasswordInput = document.getElementById('loginPassword');
const loginPasswordToggle = document.getElementById('pwToggle');
const loginEyeIcon = document.getElementById('eyeIcon');

if (loginPasswordInput && loginPasswordToggle && loginEyeIcon) {
   const eyeOpen = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
   const eyeClosed = '<path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>';

   loginPasswordToggle.addEventListener('click', () => {
      const hidden = loginPasswordInput.type === 'password';
      loginPasswordInput.type = hidden ? 'text' : 'password';
      loginEyeIcon.innerHTML = hidden ? eyeClosed : eyeOpen;
   });
}

// Active menu highlighting on scroll
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-links a');

function highlightNavOnScroll() {
   const scrollPos = window.scrollY + 150;

   sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      const sectionId = section.getAttribute('id');

      if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
         // Desktop nav
         navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + sectionId) {
               link.classList.add('active');
            }
         });
         // Mobile nav
         mobileNavLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + sectionId) {
               link.classList.add('active');
            }
         });
      }
   });

   // Remove active if at top of page
   if (window.scrollY < 100) {
      navLinks.forEach(link => link.classList.remove('active'));
      mobileNavLinks.forEach(link => link.classList.remove('active'));
   }
}

window.addEventListener('scroll', highlightNavOnScroll);

// Product tabs
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.products-tab-content');
let currentProductTab = 0;
let productAutoPlay;

function showProductTab(index) {
   if (!tabBtns.length || !tabContents.length) return;

   const safeIndex = (index + tabBtns.length) % tabBtns.length;
   currentProductTab = safeIndex;

   tabBtns.forEach((btn, btnIndex) => {
      btn.classList.toggle('active', btnIndex === safeIndex);
   });

   tabContents.forEach((content, contentIndex) => {
      content.classList.toggle('active', contentIndex === safeIndex);
   });
}

function startProductAutoPlay() {
   if (!tabBtns.length || !tabContents.length) return;

   clearInterval(productAutoPlay);
   productAutoPlay = setInterval(() => {
      showProductTab(currentProductTab + 1);
   }, 6000);
}

tabBtns.forEach((btn, index) => {
   btn.addEventListener('click', () => {
      showProductTab(index);
      startProductAutoPlay();
   });
});

const productsSection = document.querySelector('.products');
if (productsSection) {
   productsSection.addEventListener('mouseenter', () => clearInterval(productAutoPlay));
   productsSection.addEventListener('mouseleave', () => startProductAutoPlay());
}

showProductTab(0);
startProductAutoPlay();

// Testimonial Slider
const testimonialsTrack = document.getElementById('testimonialsTrack');
const testimonialDots = document.querySelectorAll('#testimonialDots .dot');
const testimonialPrev = document.getElementById('testimonialPrev');
const testimonialNext = document.getElementById('testimonialNext');
const totalTestimonials = testimonialDots.length;
let currentTestimonial = 0;

function goToTestimonial(index) {
   if (index < 0) index = totalTestimonials - 1;
   if (index >= totalTestimonials) index = 0;

   currentTestimonial = index;
   if (!testimonialsTrack) return;

   testimonialsTrack.style.transform = `translateX(-${currentTestimonial * 100}%)`;

   testimonialDots.forEach((dot, i) => {
      dot.classList.toggle('active', i === currentTestimonial);
   });
}

if (testimonialsTrack && testimonialPrev && testimonialNext && totalTestimonials > 0) {
   testimonialDots.forEach((dot, index) => {
      dot.addEventListener('click', () => {
         goToTestimonial(index);
      });
   });

   testimonialPrev.addEventListener('click', () => {
      goToTestimonial(currentTestimonial - 1);
   });

   testimonialNext.addEventListener('click', () => {
      goToTestimonial(currentTestimonial + 1);
   });

   // Auto-advance testimonials every 6 seconds
   let testimonialAutoPlay = setInterval(() => {
      goToTestimonial(currentTestimonial + 1);
   }, 6000);

   // Pause auto-play on hover
   const testimonialsWrapper = document.querySelector('.testimonials-wrapper');
   if (testimonialsWrapper) {
      testimonialsWrapper.addEventListener('mouseenter', () => {
         clearInterval(testimonialAutoPlay);
      });

      testimonialsWrapper.addEventListener('mouseleave', () => {
         testimonialAutoPlay = setInterval(() => {
            goToTestimonial(currentTestimonial + 1);
         }, 6000);
      });
   }
}

// Simulate live price updates (for demo purposes)
function updatePrices() {
   const priceElement = document.querySelector('.price-value');
   const changeElement = document.querySelector('.price-change');

   // Random price fluctuation for demo
   const basePrice = 4285.50;
   const fluctuation = (Math.random() - 0.5) * 10;
   const newPrice = (basePrice + fluctuation).toFixed(2);

   // This is just for visual effect - in production, connect to real API
}

const hasPriceWidget = document.querySelector('.price-value') || document.querySelector('.price-change');

// Update prices every 30 seconds (demo)
if (hasPriceWidget) {
   setInterval(updatePrices, 30000);
}

