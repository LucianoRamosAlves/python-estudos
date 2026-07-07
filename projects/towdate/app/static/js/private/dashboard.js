// Minimal interactions for dashboard
document.addEventListener('DOMContentLoaded', function(){
  // small fade-in for panels
  document.querySelectorAll('.panel').forEach((el,i)=>{ el.style.opacity=0; setTimeout(()=>{ el.style.transition='opacity 360ms'; el.style.opacity=1 }, 80+i*40)});
});
