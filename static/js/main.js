document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Handle file input for upload form
    const fileInput = document.getElementById('report_file');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileName = this.files[0]?.name;
            if (fileName) {
                const label = document.querySelector('.custom-file-label');
                if (label) {
                    label.textContent = fileName;
                }
            }
        });
    }

    // Handle delete confirmation
    const deleteButtons = document.querySelectorAll('.delete-report-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const reportId = this.getAttribute('data-report-id');
            const reportTitle = this.getAttribute('data-report-title');
            
            // Set the report title in the modal
            const modalReportTitle = document.getElementById('deleteReportTitle');
            if (modalReportTitle) {
                modalReportTitle.textContent = reportTitle;
            }
            
            // Set the form action in the modal
            const deleteForm = document.getElementById('deleteReportForm');
            if (deleteForm) {
                deleteForm.action = `/reports/${reportId}/delete`;
            }
            
            // Show the modal
            const deleteModal = new bootstrap.Modal(document.getElementById('deleteReportModal'));
            deleteModal.show();
        });
    });

    // Handle RTL/LTR layout based on language
    const htmlElement = document.documentElement;
    const currentLanguage = document.body.getAttribute('data-language');
    
    if (currentLanguage === 'ar') {
        htmlElement.setAttribute('dir', 'rtl');
        document.body.classList.add('rtl');
    } else {
        htmlElement.setAttribute('dir', 'ltr');
        document.body.classList.remove('rtl');
    }
});
