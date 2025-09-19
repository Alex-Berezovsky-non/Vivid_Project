// static/core/js/gallery.js
document.addEventListener('DOMContentLoaded', function() {
    const slider = document.querySelector('.gallery-slider');
    const prevBtn = document.querySelector('.gallery-prev');
    const nextBtn = document.querySelector('.gallery-next');
    
    if (!slider) return;
    
    const scrollAmount = 330; // Шаг прокрутки (width + gap)
    
    prevBtn.addEventListener('click', () => {
        slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });
    
    nextBtn.addEventListener('click', () => {
        slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
    
    // Автопрокрутка (опционально)
    let autoScroll = setInterval(() => {
        slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        
        // Если достигнут конец - вернуться в начало
        if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth - 50) {
            setTimeout(() => {
                slider.scrollTo({ left: 0, behavior: 'smooth' });
            }, 1000);
        }
    }, 4000);
    
    // Остановить автопрокрутку при наведении
    slider.addEventListener('mouseenter', () => {
        clearInterval(autoScroll);
    });
    
    slider.addEventListener('mouseleave', () => {
        autoScroll = setInterval(() => {
            slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        }, 4000);
    });
});