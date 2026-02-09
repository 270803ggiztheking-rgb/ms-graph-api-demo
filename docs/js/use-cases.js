// Use Cases Page Scripts

document.addEventListener('DOMContentLoaded', () => {
    initSectorNav();
    initHealthChart();
});

// 1. Sticky Navigation & Scroll Spy
function initSectorNav() {
    const navLinks = document.querySelectorAll('.sector-link');
    const sections = document.querySelectorAll('.case-section');

    // Click to scroll
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);
            
            // Offset for sticky header
            const offset = 100;
            const bodyRect = document.body.getBoundingClientRect().top;
            const elementRect = targetSection.getBoundingClientRect().top;
            const elementPosition = elementRect - bodyRect;
            const offsetPosition = elementPosition - offset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        });
    });

    // Scroll Spy (Highlight active link)
    const observerOptions = {
        root: null,
        rootMargin: '-20% 0px -60% 0px', // Trigger when section is in middle of viewport
        threshold: 0
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Remove active class from all
                navLinks.forEach(link => link.classList.remove('active'));
                
                // Add to current
                const id = entry.target.getAttribute('id');
                const activeLink = document.querySelector(`.sector-link[data-target="${id}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        observer.observe(section);
    });
}

// 2. Health Sector Chart (Chart.js)
function initHealthChart() {
    const ctx = document.getElementById('healthChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [
                {
                    label: 'Manual Bookings (Conflicts)',
                    data: [12, 15, 8, 10],
                    backgroundColor: 'rgba(216, 59, 1, 0.5)', // Warning color
                    borderColor: 'rgba(216, 59, 1, 1)',
                    borderWidth: 1
                },
                {
                    label: 'MediGraph Sync (Conflicts)',
                    data: [0, 0, 0, 0],
                    backgroundColor: 'rgba(16, 124, 16, 0.5)', // Success color
                    borderColor: 'rgba(16, 124, 16, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Scheduling Conflicts Reduction'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Conflicts'
                    }
                }
            }
        }
    });
}

// 3. Copy Code Function
window.copyCode = function(elementId) {
    const codeElement = document.getElementById(elementId);
    const text = codeElement.innerText;

    navigator.clipboard.writeText(text).then(() => {
        // Visual feedback
        const btn = codeElement.parentElement.parentElement.querySelector('.btn-copy');
        const originalHtml = btn.innerHTML;
        
        btn.innerHTML = '<i data-lucide="check"></i> Copied!';
        lucide.createIcons();
        
        setTimeout(() => {
            btn.innerHTML = originalHtml;
            lucide.createIcons();
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
};
