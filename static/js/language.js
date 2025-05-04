document.addEventListener('DOMContentLoaded', function() {
    // Handle language toggle
    const languageToggle = document.querySelectorAll('.language-toggle');
    
    languageToggle.forEach(function(element) {
        element.addEventListener('click', function(event) {
            event.preventDefault();
            const language = this.getAttribute('data-language');
            
            // Redirect to set language route
            window.location.href = `/set-language/${language}`;
        });
    });
});
