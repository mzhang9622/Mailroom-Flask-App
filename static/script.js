document.addEventListener('DOMContentLoaded', function () {
    const delete_admins = document.querySelectorAll('.delete-admin');

    delete_admins.forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const user_id = form.getAttribute('data-user-id');
            const url = form.action;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                },
                body: JSON.stringify({
                    user_id: user_id
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    form.closest('.delete-border-container').remove();
                    alert('Admin deleted successfully');
                } else {
                    alert('Failed to delete the admin');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error deleting the admin');
            });
        });
    });
});