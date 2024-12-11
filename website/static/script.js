

/* FOR CONFIRMING DELETION of ADMIN */
const deleteAdmin = document.querySelectorAll('.remove-form');
deleteAdmin.forEach(form => {
    form.addEventListener('submit', confirmDelete);
});

function confirmDelete(event) {
    event.preventDefault();

    const isConfirmed = confirm("Do you want to delete this admin?");

    if (isConfirmed) {
        event.target.submit(); 
    }
}

/* FOR REFRESH */
window.onbeforeunload = function() {
    sessionStorage.setItem('scroll_pos', window.scrollY);
};

window.onload = function() {
    const scroll_pos = sessionStorage.getItem('scroll_pos');
    
    if (scroll_pos)
    {
        window.scrollTo(0, scroll_pos);
    }
};

/* FOR PREVENTING SCROLLING */
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.update-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const boxId = this.dataset.boxId;
            const quantity = this.querySelector('input[name="quantity"]').value;

            fetch(`/update_box/${boxId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ quantity: quantity })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const boxQuantity = this.closest('.box-side-by-side-container').querySelector('.box-quantity');
                    boxQuantity.textContent = data.new_quantity;
                    const warning = this.closest('.box-side-by-side-container').querySelector('.warning');
                    const low_stock = parseInt(this.closest('.box-side-by-side-container').querySelector('.box-low-stock').textContent);
                    if (parseInt(boxQuantity.textContent) <= low_stock)
                    {
                        warning.textContent = "WARNING! LOW STOCK!";
                    }
                    else
                    {
                        warning.textContent = "";
                    }
                } else {
                    alert(data.message);
                }
            });
        });
    });

    document.querySelectorAll('.update-size-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const boxId = this.dataset.boxId;
            const size = this.querySelector('input[name="size"]').value;

            fetch(`/update_size/${boxId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ size: size })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const boxSize = this.closest('.box-side-by-side-container').querySelector('.box-size');
                    boxSize.textContent = data.new_size;
                } else {
                    alert(data.message);
                }
            });
        });
    });

    document.querySelectorAll('.update-link-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const boxId = this.dataset.boxId;
            const link = this.querySelector('input[name="link"]').value;

            fetch(`/update_link/${boxId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ link: link })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const boxLink = this.closest('.box-side-by-side-container').querySelector('.box-link');
                    boxLink.textContent = data.new_link;
                } else {
                    alert(data.message);
                }
            });
        });
    });

    document.querySelectorAll('.update-low-stock-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const boxId = this.dataset.boxId;
            const low_stock = this.querySelector('input[name="low-stock"]').value;

            fetch(`/update_low_stock/${boxId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ low_stock: low_stock })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const boxLowStock = this.closest('.box-side-by-side-container').querySelector('.box-low-stock');
                    boxLowStock.textContent = data.new_low_stock;
                } else {
                    alert(data.message);
                }
            });
        });
    });

    document.querySelectorAll('.update-barcode-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const boxId = this.dataset.boxId;
            const barcode = this.querySelector('input[name="barcode"]').value;

            fetch(`/update_barcode/${boxId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ barcode: barcode })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const boxBarcode = this.closest('.box-side-by-side-container').querySelector('.box-barcode');
                    boxBarcode.textContent = data.new_barcode;
                } else {
                    alert(data.message);
                }
            });
        });
    });

    document.querySelectorAll('.delete-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const boxId = this.dataset.boxId;

            fetch(`/delete_box/${boxId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.closest('.box-loop').remove();
                } else {
                    alert(data.message);
                }
            });
        });
    });
});

/* TO ALLOW USERS TO SEE PASSWORDS TYPED */
function togglePassword() {
    const show_button = document.querySelector('#show-password');
    const show_password_icon = show_button.querySelector('img');
    const password_input = document.querySelector('.password-input-text');


        show_button.addEventListener('click', function() {
        if (password_input.type === 'password') {
            password_input.type = 'text';
            show_password_icon.src = './static/images/eye-regular.svg';
        } else {
            password_input.type = 'password';
            show_password_icon.src = './static/images/eye-slash-regular.svg';
        }
    });

}
//togglePassword();

/* Barcode Scanner Integration */
function onScanSuccess(decodedText, decodedResult) {
    console.log(`Code scanned = ${decodedText}`, decodedResult);
    const searchBar = document.getElementById("barcode-text");
    searchBar.value = decodedText;
}
var html5QrcodeScanner = new Html5QrcodeScanner(
 "qr-reader", { fps: 10, qrbox: 250 });
html5QrcodeScanner.render(onScanSuccess);

