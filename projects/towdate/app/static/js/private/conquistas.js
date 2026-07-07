// Minimal UI touches for achievements page
document.addEventListener('DOMContentLoaded', function(){
  const cards = document.querySelectorAll('.achievement-card');
  cards.forEach((c, i)=>{
    c.style.opacity = 0;
    setTimeout(()=>{ c.style.transition='opacity 360ms ease-out, transform 360ms'; c.style.opacity=1; c.style.transform='translateY(0)'; }, 40 + i*60);
    c.style.transform='translateY(6px)';
  });
});
