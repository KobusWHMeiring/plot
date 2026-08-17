(function () {
  const carousel = document.querySelector('.carousel');
  if (!carousel) return;

  const track = carousel.querySelector('.carousel__track');
  const slides = Array.from(carousel.querySelectorAll('.carousel__slide'));
  const prev = carousel.querySelector('.carousel__arrow--prev');
  const next = carousel.querySelector('.carousel__arrow--next');
  const dotsBox = carousel.querySelector('.carousel__dots');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (reduceMotion) track.classList.add('carousel__track--reduced');

  // Build dots to match slide count
  slides.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.className = 'carousel__dot';
    dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
    dot.addEventListener('click', () => goTo(i));
    dotsBox.appendChild(dot);
  });
  const dots = Array.from(dotsBox.querySelectorAll('.carousel__dot'));

  let current = 0;

  function goTo(index) {
    current = (index + slides.length) % slides.length;
    track.style.transform = `translateX(-${current * 100}%)`;
    slides.forEach((slide, i) => {
      slide.classList.toggle('carousel__slide--active', i === current);
      slide.setAttribute('aria-hidden', i === current ? 'false' : 'true');
    });
    dots.forEach((dot, i) => {
      dot.classList.toggle('carousel__dot--active', i === current);
      dot.setAttribute('aria-current', i === current ? 'true' : 'false');
    });
  }

  prev.addEventListener('click', () => goTo(current - 1));
  next.addEventListener('click', () => goTo(current + 1));

  carousel.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(current - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); goTo(current + 1); }
  });

  goTo(0);
})();
