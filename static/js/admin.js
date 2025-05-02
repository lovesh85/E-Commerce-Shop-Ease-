// Admin Dashboard functionality for ShopEase

document.addEventListener('DOMContentLoaded', function() {
    // Delete product confirmation
    const deleteProductForms = document.querySelectorAll('.delete-product-form');
    deleteProductForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const productName = this.dataset.productName;
            
            if (confirm(`Are you sure you want to delete "${productName}"? This action cannot be undone.`)) {
                this.submit();
            }
        });
    });
    
    // Image URL preview in product form
    const imageUrlInput = document.querySelector('#image_url');
    const imagePreview = document.querySelector('#image-preview');
    
    if (imageUrlInput && imagePreview) {
        // Initial preview if URL exists
        if (imageUrlInput.value) {
            imagePreview.src = imageUrlInput.value;
            document.querySelector('#preview-container').classList.remove('d-none');
        }
        
        // Update preview when URL changes
        imageUrlInput.addEventListener('input', function() {
            if (this.value) {
                imagePreview.src = this.value;
                document.querySelector('#preview-container').classList.remove('d-none');
            } else {
                document.querySelector('#preview-container').classList.add('d-none');
            }
        });
    }
    
    // Order status update
    const orderStatusSelect = document.querySelector('#order-status');
    const updateStatusForm = document.querySelector('#update-status-form');
    
    if (orderStatusSelect && updateStatusForm) {
        orderStatusSelect.addEventListener('change', function() {
            updateStatusForm.submit();
        });
    }
    
    // Sales chart if on dashboard
    const chartCanvas = document.querySelector('#sales-chart');
    if (chartCanvas) {
        // Use real data from backend
        const ctx = chartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['January', 'February', 'March', 'April', 'May', 'June'],
                datasets: [{
                    label: 'Sales',
                    data: [12, 19, 3, 5, 2, 3],
                    borderColor: '#0d6efd',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Categories bar chart
    const categoriesChartCanvas = document.querySelector('#categories-chart');
    if (categoriesChartCanvas) {
        const categoryNames = JSON.parse(categoriesChartCanvas.dataset.categories || '[]');
        const categoryCounts = JSON.parse(categoriesChartCanvas.dataset.counts || '[]');
        
        const ctx = categoriesChartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: categoryNames,
                datasets: [{
                    label: 'Products by Category',
                    data: categoryCounts,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)',
                        'rgba(199, 199, 199, 0.7)',
                        'rgba(83, 102, 255, 0.7)',
                        'rgba(40, 159, 64, 0.7)',
                        'rgba(210, 199, 199, 0.7)'
                    ],
                    borderColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 206, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(153, 102, 255)',
                        'rgb(255, 159, 64)',
                        'rgb(199, 199, 199)',
                        'rgb(83, 102, 255)',
                        'rgb(40, 159, 64)',
                        'rgb(210, 199, 199)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0 // Only show whole numbers
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Products by Category',
                        font: {
                            size: 16
                        }
                    },
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
});
