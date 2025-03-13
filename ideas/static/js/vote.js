document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".vote-btn").forEach(button => {
        button.addEventListener("click", function () {
            let ideaId = this.getAttribute("data-id");
            let voteCountElement = document.getElementById(`votes-${ideaId}`);
            let voteButton = this;
            let ideaCard = this.closest(".idea-card");

            // Show loading state
            voteButton.disabled = true;
            voteButton.textContent = "Voting...";

            fetch(`/vote/${ideaId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "X-Requested-With": "XMLHttpRequest"
                },
                credentials: "same-origin"
            })
            .then(response => response.json())
            .then(data => {
                if (data.votes !== undefined) {
                    voteCountElement.textContent = data.votes; // Update votes instantly
                    reorderIdeas(); // Call function to reorder ideas
                    voteButton.textContent = "Voted ✅"; // Show success
                    voteButton.classList.replace("btn-primary", "btn-success"); // Change color
                } else {
                    showError(voteButton, data.error);
                }
            })
            .catch(error => {
                console.error("Error:", error);
                showError(voteButton, "Something went wrong! Try again.");
            })
            .finally(() => {
                voteButton.disabled = false; // Re-enable button after response
            });
        });
    });

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }

    function reorderIdeas() {
        let ideaContainer = document.querySelector(".idea-container");
        let ideas = Array.from(ideaContainer.getElementsByClassName("idea-card"));

        // Sort ideas based on votes in descending order
        ideas.sort((a, b) => {
            let votesA = parseInt(a.querySelector(".vote-count").textContent);
            let votesB = parseInt(b.querySelector(".vote-count").textContent);
            return votesB - votesA; // Higher votes come first
        });

        // Reattach sorted ideas to the container
        ideas.forEach(idea => ideaContainer.appendChild(idea));
    }

    function showError(button, message) {
        let errorDiv = document.createElement("div");
        errorDiv.className = "alert alert-danger mt-2 fade-in";
        errorDiv.textContent = message;

        let parent = button.parentNode;
        parent.appendChild(errorDiv);

        setTimeout(() => errorDiv.remove(), 3000); // Remove after 3 seconds
    }
});
