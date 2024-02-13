document.addEventListener('DOMContentLoaded', function() {
    const themeToggleBtn = document.getElementById('themeToggleBtn');

    // reading the selected theme and switch state from localStorage
    const theme = localStorage.getItem('theme');

    // set the current theme
    if (theme) {
        document.body.classList.add(theme + '-theme');
    } else {
        localStorage.setItem('theme', 'light');
        document.body.classList.add('light-theme');
    }

    // set the current switch state
    if (theme === 'dark') {
        themeToggleBtn.checked = true;
    } else {
        themeToggleBtn.checked = false;
    }

    // handling of switch state change events
    themeToggleBtn.addEventListener('change', function() {
        const body = document.body;
        if (this.checked) {
            body.classList.remove('light-theme');
            body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark'); // save selected theme to localStorage
        } else {
            body.classList.remove('dark-theme');
            body.classList.add('light-theme');
            localStorage.setItem('theme', 'light');
        }
    });
});

