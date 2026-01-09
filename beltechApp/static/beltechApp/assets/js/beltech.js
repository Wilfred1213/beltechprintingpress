document.addEventListener("DOMContentLoaded", function() {
    // 1. Elements
    const consentBar = document.getElementById('cookie-consent-bar');
    const acceptBtn = document.getElementById('accept-cookies');
    const modalElement = document.getElementById('testimonialPopUp');
    const form = document.getElementById('pop-up-testimonial-form');
    const formContainer = document.getElementById('testimonial-form-container');
    const successMessage = document.getElementById('testimonial-success-message');
    
    // Initialize Bootstrap Modal once
    const testimonialModal = new bootstrap.Modal(modalElement);

    // 2. Logic State
    const hasAcceptedCookies = localStorage.getItem('cookiesAccepted');
    const hasSubmittedForm = localStorage.getItem('testimonialSubmitted');

    // --- STEP 1: COOKIE BAR CONTROL ---
    if (!hasAcceptedCookies) {
        // Show bar after 1 second if not accepted
        setTimeout(() => { if(consentBar) consentBar.classList.add('show'); }, 1000);
    } else if (!hasSubmittedForm) {
        // If already accepted but form not done, start timer
        startLogicTimer();
    }

    // --- STEP 2: ACCEPT BUTTON CLICK ---
    if (acceptBtn) {
        acceptBtn.addEventListener('click', function() {
            localStorage.setItem('cookiesAccepted', 'true');
            consentBar.classList.remove('show');
            startLogicTimer(); 
        });
    }

    // --- STEP 3: THE 60-SECOND TIMER ---
    function startLogicTimer() {
        setInterval(function() {
            const alreadyDone = localStorage.getItem('testimonialSubmitted');
            const isOpen = modalElement.classList.contains('show');
            
            if (!alreadyDone && !isOpen) {
                testimonialModal.show();
            }
        }, 60000); // 1 minute
    }

    // --- STEP 4: AJAX FORM SUBMISSION ---
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
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => {
                if (response.ok) {
                    // Success: Never show again
                    localStorage.setItem('testimonialSubmitted', 'true');

                    // Show Success UI
                    formContainer.classList.add('d-none');
                    successMessage.classList.remove('d-none');

                    // Auto-close after 3 seconds
                    setTimeout(() => {
                        testimonialModal.hide();
                    }, 3000);
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

    // --- STEP 5: BACKDROP CLEANUP (The "Transparency" Fix) ---
    modalElement.addEventListener('hidden.bs.modal', function () {
        const backdrop = document.querySelector('.modal-backdrop');
        if (backdrop) backdrop.remove();
        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';
        
        // Reset form if they closed without submitting (so it shows again in 1 min)
        if (localStorage.getItem('testimonialSubmitted') !== 'true') {
            formContainer.classList.remove('d-none');
            successMessage.classList.add('d-none');
        }
    });
});

// // pop up modal 
// document.addEventListener("DOMContentLoaded", function() {
//     const testimonialModal = new bootstrap.Modal(document.getElementById('testimonialPopUp'));
    
//     // Function to get a cookie by name
//     function getCookie(name) {
//         let value = "; " + document.cookie;
//         let parts = value.split("; " + name + "=");
//         if (parts.length == 2) return parts.pop().split(";").shift();
//     }

//     // Function to set a cookie
//     setTestimonialCookie = function() {
//         let date = new Date();
//         date.setTime(date.getTime() + (365 * 24 * 60 * 60 * 1000)); // 1 year
//         document.cookie = "testimonial_submitted=true; expires=" + date.toUTCString() + "; path=/";
//     };

//     // Main Logic
//     if (getCookie("testimonial_submitted") !== "true") {
//         // Trigger every 60,000 milliseconds (1 minute)
//         setInterval(function() {
//             // Only show if it's not already open
//             if (!document.getElementById('testimonialPopUp').classList.contains('show')) {
//                 testimonialModal.show();
//             }
//         }, 60000); 
//     }

//     // Handle form submission success
//     const form = document.getElementById('pop-up-testimonial-form');
//     form.addEventListener('submit', function() {
//         // We assume success here, or you can use AJAX to confirm
//         setTestimonialCookie();
//     });
// });