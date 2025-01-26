document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('surveyForm');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Show loading alert
            Swal.fire({
                title: 'Submitting...',
                text: 'Please wait while we save your data.',
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            try {
                const formData = new FormData(form);
                const response = await fetch('/submit', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();

                if (result.success) {
                    Swal.fire({
                        title: 'Success',
                        text: result.message,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        form.reset(); // Reset the form
                        window.location.href = '/responses'; // Redirect to the responses page
                    });
                } else {
                    Swal.fire({
                        title: 'Error',
                        text: result.message,
                        icon: 'error',
                        confirmButtonText: 'Try Again'
                    });
                }
            } catch (error) {
                Swal.fire({
                    title: 'Error',
                    text: 'An unexpected error occurred.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
    } else {
        console.error('The surveyForm element does not exist in the DOM.');
    }

    // Toggle navbar menu
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('show');
            navToggle.classList.toggle('active');
        });

        navLinks.addEventListener('click', () => {
            navLinks.classList.remove('show');
            navToggle.classList.remove('active');
        });
    } else {
        console.error('Navbar toggle elements are missing in the DOM.');
    }
});
