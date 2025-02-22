document.addEventListener("DOMContentLoaded", function () {
    function switchTab(tabName) {
        // Hide all tab content
        document.querySelectorAll(".tab-content").forEach(el => el.style.display = "none");

        // Show the selected tab content
        let activeTab = document.getElementById(tabName);
        if (activeTab) {
            activeTab.style.display = "block";
        }

        // Remove active class from all buttons
        document.querySelectorAll(".tab-button").forEach(el => el.classList.remove("uk-active"));

        // Add active class to the clicked tab
        let activeButton = document.querySelector(`[data-tab='${tabName}']`);
        if (activeButton) {
            activeButton.classList.add("uk-active");
        }
    }

    // Set default tab to "overview" when the page loads
    setTimeout(() => {
        switchTab("overview");
    }, 50);

    // Attach event listeners to all tab buttons
    document.querySelectorAll(".tab-button").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            switchTab(this.getAttribute("data-tab"));
        });
    });
});
