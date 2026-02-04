// ===== JPCS WEBSITE - JAVASCRIPT =====

// ===== NAVIGATION =====
const nav = document.querySelector('nav');
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navLinks = document.querySelector('.nav-links');

// Scroll effect for navigation
window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});

// Mobile menu toggle
if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        mobileMenuToggle.classList.toggle('active');
        navLinks.classList.toggle('active');
    });

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenuToggle.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });
}

// ===== SMOOTH SCROLLING =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== OFFICERS DATA =====
const officers = [
    {
        id: 1,
        name: "Maria Santos",
        position: "President",
        course: "BS Computer Science",
        year: "4th Year",
        icon: "👩‍💼",
        bio: "Passionate about technology and community building. Leading JPCS with a vision to empower every member.",
        email: "maria.santos@jpcs.org",
        skills: ["Leadership", "Public Speaking", "Project Management"]
    },
    {
        id: 2,
        name: "Juan Dela Cruz",
        position: "Vice President",
        course: "BS Information Technology",
        year: "4th Year",
        icon: "👨‍💼",
        bio: "Supporting the president in all initiatives and managing internal operations of the organization.",
        email: "juan.delacruz@jpcs.org",
        skills: ["Strategic Planning", "Team Coordination", "Event Management"]
    },
    {
        id: 3,
        name: "Ana Reyes",
        position: "Secretary",
        course: "BS Computer Science",
        year: "3rd Year",
        icon: "👩‍💻",
        bio: "Keeping all records organized and ensuring smooth communication within the organization.",
        email: "ana.reyes@jpcs.org",
        skills: ["Documentation", "Communication", "Organization"]
    },
    {
        id: 4,
        name: "Carlos Rodriguez",
        position: "Treasurer",
        course: "BS Information Technology",
        year: "3rd Year",
        icon: "👨‍💻",
        bio: "Managing the financial resources of JPCS and ensuring transparency in all transactions.",
        email: "carlos.rodriguez@jpcs.org",
        skills: ["Financial Management", "Budgeting", "Accounting"]
    },
    {
        id: 5,
        name: "Sofia Garcia",
        position: "Event Coordinator",
        course: "BS Computer Engineering",
        year: "3rd Year",
        icon: "🎯",
        bio: "Organizing amazing events that bring our community together and create lasting memories.",
        email: "sofia.garcia@jpcs.org",
        skills: ["Event Planning", "Logistics", "Creativity"]
    },
    {
        id: 6,
        name: "Miguel Torres",
        position: "Technical Lead",
        course: "BS Computer Science",
        year: "4th Year",
        icon: "⚡",
        bio: "Leading technical workshops and hackathons to enhance the coding skills of our members.",
        email: "miguel.torres@jpcs.org",
        skills: ["Web Development", "Programming", "Mentoring"]
    }
];

// ===== EVENTS DATA =====
const events = [
    {
        id: 1,
        title: "Web Development Workshop",
        description: "Learn the fundamentals of web development with HTML, CSS, and JavaScript. Perfect for beginners!",
        date: "2026-03-15",
        time: "2:00 PM - 5:00 PM",
        location: "Computer Lab 1",
        category: "workshop",
        icon: "🌐",
        speaker: "Prof. John Smith",
        slots: 30,
        registered: 23,
        details: "This comprehensive workshop will cover the basics of web development including HTML5, CSS3, and JavaScript ES6. Participants will build a complete responsive website from scratch."
    },
    {
        id: 2,
        title: "AI & Machine Learning Seminar",
        description: "Explore the exciting world of Artificial Intelligence and Machine Learning with industry experts.",
        date: "2026-02-20",
        time: "1:00 PM - 4:00 PM",
        location: "Auditorium",
        category: "seminar",
        icon: "🤖",
        speaker: "Dr. Sarah Johnson",
        slots: 100,
        registered: 87,
        details: "Discover the latest trends in AI and ML. Topics include neural networks, deep learning, and real-world applications in various industries."
    },
    {
        id: 3,
        title: "Annual Hackathon 2026",
        description: "48-hour coding marathon! Build innovative solutions and compete for amazing prizes.",
        date: "2026-04-10",
        time: "9:00 AM (Day 1)",
        location: "Innovation Hub",
        category: "hackathon",
        icon: "💻",
        speaker: "Multiple Mentors",
        slots: 50,
        registered: 45,
        details: "Join teams of 3-5 members to develop innovative tech solutions. Categories include Web Apps, Mobile Apps, and AI Solutions. Total prize pool: ₱50,000!"
    },
    {
        id: 4,
        title: "Cybersecurity Basics",
        description: "Learn how to protect yourself and your applications from cyber threats.",
        date: "2026-02-25",
        time: "3:00 PM - 6:00 PM",
        location: "Computer Lab 2",
        category: "workshop",
        icon: "🔒",
        speaker: "Alex Martinez",
        slots: 25,
        registered: 20,
        details: "Hands-on workshop covering password security, encryption, secure coding practices, and common vulnerabilities."
    },
    {
        id: 5,
        title: "Career in Tech: Panel Discussion",
        description: "Hear from successful IT professionals about their career journeys and get valuable advice.",
        date: "2026-03-05",
        time: "2:00 PM - 4:00 PM",
        location: "Conference Room",
        category: "seminar",
        icon: "💼",
        speaker: "Industry Professionals",
        slots: 60,
        registered: 52,
        details: "Panel discussion with tech professionals from leading companies. Q&A session and networking opportunity included."
    },
    {
        id: 6,
        title: "JPCS Year-End Party",
        description: "Celebrate a successful year with games, food, and fun activities!",
        date: "2025-12-15",
        time: "5:00 PM - 9:00 PM",
        location: "University Grounds",
        category: "social",
        icon: "🎉",
        speaker: "JPCS Officers",
        slots: 150,
        registered: 142,
        details: "Year-end celebration with awards ceremony, games, performances, and dinner. Don't miss this amazing night!"
    },
    {
        id: 7,
        title: "Mobile App Development",
        description: "Create your first mobile application using React Native.",
        date: "2026-03-20",
        time: "1:00 PM - 5:00 PM",
        location: "Computer Lab 3",
        category: "workshop",
        icon: "📱",
        speaker: "Lisa Chen",
        slots: 20,
        registered: 18,
        details: "Build a cross-platform mobile app from scratch. Learn React Native fundamentals and app deployment."
    },
    {
        id: 8,
        title: "Git & GitHub Masterclass",
        description: "Master version control and collaboration with Git and GitHub.",
        date: "2026-02-28",
        time: "10:00 AM - 12:00 PM",
        location: "Computer Lab 1",
        category: "workshop",
        icon: "📦",
        speaker: "Mark Wilson",
        slots: 35,
        registered: 31,
        details: "Learn Git commands, branching strategies, pull requests, and collaborative development workflows."
    }
];

// ===== RENDER OFFICERS =====
function renderOfficers() {
    const officersGrid = document.getElementById('officers-grid');
    if (!officersGrid) return;

    officersGrid.innerHTML = officers.map(officer => `
        <div class="officer-card" onclick="showOfficerModal(${officer.id})">
            <div class="officer-image">${officer.icon}</div>
            <div class="officer-info">
                <h3 class="officer-name">${officer.name}</h3>
                <p class="officer-position">${officer.position}</p>
                <p class="officer-course">${officer.course} - ${officer.year}</p>
                <p class="officer-bio">${officer.bio}</p>
            </div>
        </div>
    `).join('');
}

// ===== RENDER EVENTS =====
function renderEvents(filteredEvents = events) {
    const eventsGrid = document.getElementById('events-grid');
    if (!eventsGrid) return;

    if (filteredEvents.length === 0) {
        eventsGrid.innerHTML = '<p style="text-align: center; grid-column: 1/-1; padding: 40px; color: #64748b;">No events found matching your criteria.</p>';
        return;
    }

    eventsGrid.innerHTML = filteredEvents.map(event => {
        const eventDate = new Date(event.date);
        const formattedDate = eventDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        
        return `
            <div class="event-card" data-category="${event.category}" onclick="showEventModal(${event.id})">
                <div class="event-image">
                    ${event.icon}
                    <div class="event-badge">${event.category}</div>
                    <div class="event-date-badge">📅 ${formattedDate}</div>
                </div>
                <div class="event-info">
                    <h3 class="event-title">${event.title}</h3>
                    <p class="event-description">${event.description}</p>
                    <div class="event-meta">
                        <span>⏰ ${event.time}</span>
                        <span>📍 ${event.location}</span>
                        <span>👥 ${event.registered}/${event.slots}</span>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// ===== EVENT FILTERING BY CATEGORY =====
const filterButtons = document.querySelectorAll('.filter-btn');

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Update active state
        filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        const filter = button.getAttribute('data-filter');
        
        if (filter === 'all') {
            renderEvents(events);
        } else {
            const filtered = events.filter(event => event.category === filter);
            renderEvents(filtered);
        }
    });
});

// ===== EVENT FILTERING BY DATE =====
const dateSort = document.getElementById('date-sort');

if (dateSort) {
    dateSort.addEventListener('change', () => {
        const sortType = dateSort.value;
        let sortedEvents = [...events];
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        switch(sortType) {
            case 'upcoming':
                sortedEvents = events.filter(event => new Date(event.date) >= today)
                    .sort((a, b) => new Date(a.date) - new Date(b.date));
                break;
            case 'recent':
                sortedEvents = events.filter(event => new Date(event.date) < today)
                    .sort((a, b) => new Date(b.date) - new Date(a.date));
                break;
            case 'date-asc':
                sortedEvents = events.sort((a, b) => new Date(a.date) - new Date(b.date));
                break;
            case 'date-desc':
                sortedEvents = events.sort((a, b) => new Date(b.date) - new Date(a.date));
                break;
        }

        renderEvents(sortedEvents);
    });
}

// ===== MODAL FUNCTIONALITY (FIXED) =====
const eventModal = document.getElementById('event-modal');
const officerModal = document.getElementById('officer-modal');

// Show Event Modal
function showEventModal(eventId) {
    const event = events.find(e => e.id === eventId);
    if (!event) return;

    const eventDate = new Date(event.date);
    const formattedDate = eventDate.toLocaleDateString('en-US', { 
        weekday: 'long',
        month: 'long', 
        day: 'numeric', 
        year: 'numeric' 
    });

    const modalBody = document.getElementById('modal-body');
    if (modalBody) {
        modalBody.innerHTML = `
            <div class="modal-image">${event.icon}</div>
            <div class="modal-header">
                <h2 class="modal-title">${event.title}</h2>
                <p class="modal-subtitle">${event.category.toUpperCase()}</p>
            </div>
            <div class="modal-body">
                <div class="modal-section">
                    <h4>📅 Date & Time</h4>
                    <p>${formattedDate}<br>${event.time}</p>
                </div>
                <div class="modal-section">
                    <h4>📍 Location</h4>
                    <p>${event.location}</p>
                </div>
                <div class="modal-section">
                    <h4>👨‍🏫 Speaker/Facilitator</h4>
                    <p>${event.speaker}</p>
                </div>
                <div class="modal-section">
                    <h4>👥 Available Slots</h4>
                    <p>${event.registered} / ${event.slots} registered</p>
                </div>
                <div class="modal-section">
                    <h4>📝 Description</h4>
                    <p>${event.details}</p>
                </div>
            </div>
        `;
    }

    if (eventModal) {
        eventModal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

// Show Officer Modal
function showOfficerModal(officerId) {
    const officer = officers.find(o => o.id === officerId);
    if (!officer) return;

    const modalBody = document.getElementById('officer-modal-body');
    if (modalBody) {
        modalBody.innerHTML = `
            <div class="modal-image">${officer.icon}</div>
            <div class="modal-header">
                <h2 class="modal-title">${officer.name}</h2>
                <p class="modal-subtitle">${officer.position}</p>
            </div>
            <div class="modal-body">
                <div class="modal-section">
                    <h4>📚 Course & Year</h4>
                    <p>${officer.course} - ${officer.year}</p>
                </div>
                <div class="modal-section">
                    <h4>📧 Email</h4>
                    <p>${officer.email}</p>
                </div>
                <div class="modal-section">
                    <h4>💡 About</h4>
                    <p>${officer.bio}</p>
                </div>
                <div class="modal-section">
                    <h4>🎯 Skills</h4>
                    <p>${officer.skills.join(' • ')}</p>
                </div>
            </div>
        `;
    }

    if (officerModal) {
        officerModal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

// FIXED: Close Modal logic using Event Delegation
// This guarantees clicks on the Close Button or the background work
document.addEventListener('click', (e) => {
    // 1. Check if the clicked element is the Close Button (or inside it)
    if (e.target.closest('.modal-close')) {
        closeModal();
    }
    // 2. Check if the clicked element is the background overlay (outside the white box)
    if (e.target.classList.contains('modal')) {
        closeModal();
    }
});

function closeModal() {
    if (eventModal) eventModal.classList.remove('show');
    if (officerModal) officerModal.classList.remove('show');
    document.body.style.overflow = 'auto';
}

// ===== MEMBERSHIP FORM =====
const membershipForm = document.getElementById('membership-form');
const formSteps = document.querySelectorAll('.form-step');
const nextBtn = document.getElementById('next-btn');
const prevBtn = document.getElementById('prev-btn');
const submitBtn = document.getElementById('submit-btn');
const progressFill = document.getElementById('progress-fill');
const currentStepEl = document.getElementById('current-step');

let currentStep = 1;
const totalSteps = 3;

// Load saved form data from LocalStorage
function loadFormData() {
    const savedData = localStorage.getItem('jpcs-registration-form');
    if (savedData) {
        const formData = JSON.parse(savedData);
        Object.keys(formData).forEach(key => {
            const input = membershipForm.elements[key];
            if (input) {
                if (input.type === 'checkbox') {
                    if (Array.isArray(formData[key])) {
                        formData[key].forEach(value => {
                            const checkbox = membershipForm.querySelector(`input[name="${key}"][value="${value}"]`);
                            if (checkbox) checkbox.checked = true;
                        });
                    } else {
                        input.checked = formData[key];
                    }
                } else {
                    input.value = formData[key];
                }
            }
        });
    }
}

// Save form data to LocalStorage
function saveFormData() {
    const formData = {};
    const formElements = membershipForm.elements;
    
    for (let element of formElements) {
        if (element.name) {
            if (element.type === 'checkbox') {
                if (element.name === 'interests') {
                    if (!formData[element.name]) {
                        formData[element.name] = [];
                    }
                    if (element.checked) {
                        formData[element.name].push(element.value);
                    }
                } else {
                    formData[element.name] = element.checked;
                }
            } else if (element.type !== 'submit' && element.type !== 'button') {
                formData[element.name] = element.value;
            }
        }
    }
    
    localStorage.setItem('jpcs-registration-form', JSON.stringify(formData));
}

// Auto-save on input change
if (membershipForm) {
    membershipForm.addEventListener('input', saveFormData);
    loadFormData();
}

// Update progress bar
function updateProgress() {
    const progress = (currentStep / totalSteps) * 100;
    progressFill.style.width = progress + '%';
    currentStepEl.textContent = currentStep;
}

// Show specific step
function showStep(step) {
    formSteps.forEach((formStep, index) => {
        if (index + 1 === step) {
            formStep.classList.add('active');
        } else {
            formStep.classList.remove('active');
        }
    });

    // Update buttons visibility
    prevBtn.style.display = step === 1 ? 'none' : 'block';
    nextBtn.style.display = step === totalSteps ? 'none' : 'block';
    submitBtn.style.display = step === totalSteps ? 'block' : 'none';

    updateProgress();
}

// Validate current step
function validateStep(step) {
    const currentFormStep = document.querySelector(`.form-step[data-step="${step}"]`);
    if (!currentFormStep) return true; // Safety check

    const inputs = currentFormStep.querySelectorAll('input[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        const errorMsg = input.parentElement.querySelector('.error-message');
        
        if (!input.value.trim() && input.type !== 'checkbox') {
            isValid = false;
            input.classList.add('error');
            if (errorMsg) errorMsg.textContent = 'This field is required';
        } else if (input.type === 'email' && input.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value)) {
                isValid = false;
                input.classList.add('error');
                if (errorMsg) errorMsg.textContent = 'Please enter a valid email address';
            } else {
                input.classList.remove('error');
                if (errorMsg) errorMsg.textContent = '';
            }
        } else if (input.type === 'tel' && input.value) {
            const phoneRegex = /^[0-9+\-\s()]+$/;
            if (!phoneRegex.test(input.value) || input.value.length < 10) {
                isValid = false;
                input.classList.add('error');
                if (errorMsg) errorMsg.textContent = 'Please enter a valid phone number';
            } else {
                input.classList.remove('error');
                if (errorMsg) errorMsg.textContent = '';
            }
        } else if (input.type === 'checkbox' && input.required && !input.checked) {
            isValid = false;
            input.classList.add('error');
            if (errorMsg) errorMsg.textContent = 'You must agree to the terms';
        } else {
            input.classList.remove('error');
            if (errorMsg) errorMsg.textContent = '';
        }
    });

    return isValid;
}

// Clear error on input
if (membershipForm) {
    membershipForm.addEventListener('input', (e) => {
        if (e.target.classList.contains('error')) {
            e.target.classList.remove('error');
            const errorMsg = e.target.parentElement.querySelector('.error-message');
            if (errorMsg) errorMsg.textContent = '';
        }
    });
}

// Next button
if (nextBtn) {
    nextBtn.addEventListener('click', () => {
        if (validateStep(currentStep)) {
            currentStep++;
            showStep(currentStep);
            saveFormData();
        }
    });
}

// Previous button
if (prevBtn) {
    prevBtn.addEventListener('click', () => {
        currentStep--;
        showStep(currentStep);
    });
}

// Form submission
if (membershipForm) {
    membershipForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        if (validateStep(currentStep)) {
            // Get all form data
            const formData = new FormData(membershipForm);
            const data = {};
            
            for (let [key, value] of formData.entries()) {
                if (data[key]) {
                    if (Array.isArray(data[key])) {
                        data[key].push(value);
                    } else {
                        data[key] = [data[key], value];
                    }
                } else {
                    data[key] = value;
                }
            }
            
            // Save to LocalStorage as submitted
            localStorage.setItem('jpcs-submitted-registration', JSON.stringify(data));
            localStorage.setItem('jpcs-registration-date', new Date().toISOString());
            
            // Clear the form progress data
            localStorage.removeItem('jpcs-registration-form');
            
            // Show success message
            showSuccessMessage();
        }
    });
}

// Show success message
function showSuccessMessage() {
    const formContainer = document.querySelector('.registration-form-container');
    if (formContainer) {
        formContainer.innerHTML = `
            <div class="success-message">
                <div class="success-icon">🎉</div>
                <h3>Registration Successful!</h3>
                <p>Thank you for joining JPCS! We've received your registration.</p>
                <p>You will receive a confirmation email at the address you provided within 24 hours.</p>
                <p>Welcome to the JPCS family!</p>
                <br>
                <button class="btn-primary" onclick="location.reload()">Register Another Member</button>
            </div>
        `;
    }
}

// ===== SCROLL TO TOP BUTTON =====
const scrollTopBtn = document.createElement('button');
scrollTopBtn.className = 'scroll-top';
scrollTopBtn.innerHTML = '↑';
scrollTopBtn.setAttribute('aria-label', 'Scroll to top');
document.body.appendChild(scrollTopBtn);

window.addEventListener('scroll', () => {
    if (window.scrollY > 500) {
        scrollTopBtn.classList.add('show');
    } else {
        scrollTopBtn.classList.remove('show');
    }
});

scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// ===== INITIALIZE =====
document.addEventListener('DOMContentLoaded', () => {
    renderOfficers();
    renderEvents();
    if(typeof showStep === 'function') showStep(1);
    
    // Check if there's a saved registration
    const savedRegistration = localStorage.getItem('jpcs-submitted-registration');
    if (savedRegistration) {
        console.log('Previous registration found:', JSON.parse(savedRegistration));
    }
});

// ===== PREFERENCES STORAGE =====
// Store user preferences (example usage)
function saveUserPreference(key, value) {
    let preferences = JSON.parse(localStorage.getItem('jpcs-preferences') || '{}');
    preferences[key] = value;
    localStorage.setItem('jpcs-preferences', JSON.stringify(preferences));
}

function getUserPreference(key) {
    let preferences = JSON.parse(localStorage.getItem('jpcs-preferences') || '{}');
    return preferences[key];
}

console.log('JPCS Website Loaded Successfully! 🚀');