document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const submitButton = document.querySelector('input[type="submit"]');
    const maxAllowed = 3;

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const checkedCount = document.querySelectorAll('input[type="checkbox"]:checked').length;
            if (checkedCount > maxAllowed) {
                this.checked = false;
            }
        });
    });

    submitButton.addEventListener('click', function (event) {
        const checkedCount = document.querySelectorAll('input[type="checkbox"]:checked').length;
        if (checkedCount !== maxAllowed) {
            event.preventDefault();
            alert(`Пожалуйста, выберите ровно ${maxAllowed} опции.`);
        }
    });
});