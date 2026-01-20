document.addEventListener("DOMContentLoaded", function() {
    // 1. Elements
    const consentBar = document.getElementById('cookie-consent-bar');
    const acceptBtn = document.getElementById('accept-cookies');
    const modalElement = document.getElementById('testimonialPopUp');
    const form = document.getElementById('pop-up-testimonial-form');
    const formContainer = document.getElementById('testimonial-form-container');
    const successMessage = document.getElementById('testimonial-success-message');
    const stickyBtn = document.querySelector('.btn-sticky-rate');
    
    // Initialize Bootstrap Modal
    const testimonialModal = new bootstrap.Modal(modalElement);

    // 2. Logic State
    const hasAcceptedCookies = localStorage.getItem('cookiesAccepted');

    // --- STEP 1: COOKIE BAR CONTROL ---
    if (!hasAcceptedCookies) {
        // Slide up after 1 second
        setTimeout(() => { 
            if(consentBar) consentBar.classList.add('show'); 
        }, 1000);
    } else {
        // If already accepted, ensure it stays gone
        if(consentBar) consentBar.style.display = 'none';
        startLogicTimer();
    }

    if (acceptBtn) {
        acceptBtn.addEventListener('click', function() {
            localStorage.setItem('cookiesAccepted', 'true');
            
            // Trigger the slide-down animation
            consentBar.classList.add('cookie-hidden');
            
            // After animation (400ms), remove from layout entirely
            setTimeout(() => {
                consentBar.style.display = 'none';
            }, 400);

            startLogicTimer(); 
        });
    }

    // --- STEP 2: THE INTELLIGENT TIMER (Once a Day) ---
    function startLogicTimer() {
        const alreadyDone = localStorage.getItem('testimonialSubmitted');
        const lastDismissed = localStorage.getItem('testimonialDismissedAt');
        const now = new Date().getTime();
        const oneDay = 24 * 60 * 60 * 1000;

        // Hide sticky button immediately if already rated
        if (alreadyDone && stickyBtn) {
            stickyBtn.style.display = 'none';
            return; 
        }

        // Auto-popup logic
        if (!alreadyDone) {
            if (!lastDismissed || (now - lastDismissed > oneDay)) {
                setTimeout(function() {
                    if (modalElement && !modalElement.classList.contains('show')) {
                        testimonialModal.show();
                    }
                }, 120000); // 2 Minutes
            }
        }
    }

    // --- STEP 3: AJAX FORM SUBMISSION ---
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const submitBtn = document.getElementById('submit-btn');
            if (submitBtn) {
                submitBtn.innerHTML = "Sending...";
                submitBtn.disabled = true;
            }

            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => {
                if (response.ok) {
                    localStorage.setItem('testimonialSubmitted', 'true');
                    formContainer.classList.add('d-none');
                    successMessage.classList.remove('d-none');
                    if(stickyBtn) stickyBtn.style.display = 'none';

                    setTimeout(() => { testimonialModal.hide(); }, 3000);
                } else {
                    alert("Submission failed. Please check the form.");
                    if (submitBtn) {
                        submitBtn.innerHTML = "Submit Review";
                        submitBtn.disabled = false;
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (submitBtn) {
                    submitBtn.innerHTML = "Error! Try Again";
                    submitBtn.disabled = false;
                }
            });
        });
    }

    // --- STEP 4: MODAL CLEANUP ---
    if (modalElement) {
        modalElement.addEventListener('hidden.bs.modal', function () {
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) backdrop.remove();
            document.body.classList.remove('modal-open');
            document.body.style.overflow = '';
            
            if (localStorage.getItem('testimonialSubmitted') !== 'true') {
                localStorage.setItem('testimonialDismissedAt', new Date().getTime());
                formContainer.classList.remove('d-none');
                successMessage.classList.add('d-none');
            }
        });
    }
});


// document.addEventListener("DOMContentLoaded", function() {
//     // 1. Elements
//     const consentBar = document.getElementById('cookie-consent-bar');
//     const acceptBtn = document.getElementById('accept-cookies');
//     const modalElement = document.getElementById('testimonialPopUp');
//     const form = document.getElementById('pop-up-testimonial-form');
//     const formContainer = document.getElementById('testimonial-form-container');
//     const successMessage = document.getElementById('testimonial-success-message');
//     const stickyBtn = document.querySelector('.btn-sticky-rate');
    
//     // Initialize Bootstrap Modal
//     const testimonialModal = new bootstrap.Modal(modalElement);

//     // 2. Logic State
//     const hasAcceptedCookies = localStorage.getItem('cookiesAccepted');
//     const hasSubmittedForm = localStorage.getItem('testimonialSubmitted');

//     // --- STEP 1: COOKIE BAR CONTROL ---
//     if (!hasAcceptedCookies) {
//         setTimeout(() => { if(consentBar) consentBar.classList.add('show'); }, 1000);
//     } else {
//         startLogicTimer();
//     }

//     if (acceptBtn) {
//         acceptBtn.addEventListener('click', function() {
//             localStorage.setItem('cookiesAccepted', 'true');
//             consentBar.classList.remove('show');
//             startLogicTimer(); 
//         });
//     }

//     // --- STEP 2: THE INTELLIGENT TIMER (Once a Day) ---
//     function startLogicTimer() {
//         const alreadyDone = localStorage.getItem('testimonialSubmitted');
//         const lastDismissed = localStorage.getItem('testimonialDismissedAt');
//         const now = new Date().getTime();
//         const oneDay = 24 * 60 * 60 * 1000;

//         // Hide sticky button immediately if already rated
//         if (alreadyDone && stickyBtn) {
//             stickyBtn.style.display = 'none';
//             return; 
//         }

//         // Auto-popup logic
//         if (!alreadyDone) {
//             if (!lastDismissed || (now - lastDismissed > oneDay)) {
//                 setTimeout(function() {
//                     if (!modalElement.classList.contains('show')) {
//                         testimonialModal.show();
//                     }
//                 }, 120000); // 2 Minutes
//             }
//         }
//     }

//     // --- STEP 3: AJAX FORM SUBMISSION ---
//     if (form) {
//         form.addEventListener('submit', function(e) {
//             e.preventDefault();
//             const submitBtn = document.getElementById('submit-btn');
//             if (submitBtn) {
//                 submitBtn.innerHTML = "Sending...";
//                 submitBtn.disabled = true;
//             }

//             const formData = new FormData(this);
//             fetch(this.action, {
//                 method: 'POST',
//                 body: formData,
//                 headers: { 'X-Requested-With': 'XMLHttpRequest' }
//             })
//             .then(response => {
//                 if (response.ok) {
//                     localStorage.setItem('testimonialSubmitted', 'true');
//                     formContainer.classList.add('d-none');
//                     successMessage.classList.remove('d-none');
//                     if(stickyBtn) stickyBtn.style.display = 'none'; // Hide sticky button

//                     setTimeout(() => { testimonialModal.hide(); }, 3000);
//                 } else {
//                     alert("Submission failed. Please check the form.");
//                     if (submitBtn) {
//                         submitBtn.innerHTML = "Submit Review";
//                         submitBtn.disabled = false;
//                     }
//                 }
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//                 if (submitBtn) {
//                     submitBtn.innerHTML = "Error! Try Again";
//                     submitBtn.disabled = false;
//                 }
//             });
//         });
//     }

//     // --- STEP 4: MODAL CLEANUP & DISMISSAL LOGIC ---
//     modalElement.addEventListener('hidden.bs.modal', function () {
//         // Transparency/Backdrop Fix
//         const backdrop = document.querySelector('.modal-backdrop');
//         if (backdrop) backdrop.remove();
//         document.body.classList.remove('modal-open');
//         document.body.style.overflow = '';
//         document.body.style.paddingRight = '';
        
//         // If they closed without submitting, save dismissal time
//         if (localStorage.getItem('testimonialSubmitted') !== 'true') {
//             localStorage.setItem('testimonialDismissedAt', new Date().getTime());
//             formContainer.classList.remove('d-none');
//             successMessage.classList.add('d-none');
//         }
//     });
// });








