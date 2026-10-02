async function postJSON(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    return await response.json();
}


function showMessage(message, isError = false) {
    const element = document.getElementById("form-message");

    if (!element) {
        return;
    }

    element.textContent = message;
    element.style.color = isError ? "#c0392b" : "#27ae60";
}


const registerForm = document.getElementById("register-form");

if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const data = {
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        };

        try {
            const result = await postJSON("/api/register", data);

            if (!result.success) {
                showMessage(result.detail || result.message || "Registration failed.", true);
                return;
            }

            showMessage("Registration successful. Redirecting...");

            setTimeout(() => {
                window.location.href = "/dashboard";
            }, 700);

        } catch (error) {
            showMessage("Something went wrong. Please try again.", true);
        }
    });
}


const loginForm = document.getElementById("login-form");

if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const data = {
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        };

        try {
            const result = await postJSON("/api/login", data);

            if (!result.success) {
                showMessage(result.detail || result.message || "Login failed.", true);
                return;
            }

            showMessage("Login successful. Redirecting...");

            setTimeout(() => {
                window.location.href = "/dashboard";
            }, 700);

        } catch (error) {
            showMessage("Something went wrong. Please try again.", true);
        }
    });
}


async function generateRecommendation(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    return await response.json();
}


function displayRecommendation(result) {
    const container = document.getElementById("recommendation-result");

    if (!container) {
        return;
    }

    if (!result.success) {
        container.innerHTML = `
            <div class="result-card">
                <p>${result.message || "Unable to generate recommendation."}</p>
            </div>
        `;
        return;
    }

    const recommendation = result.recommendation || {};
    const items = recommendation.items || recommendation.recommendations || [];
    const tips = recommendation.tips || [];

    let html = `
        <div class="result-card">
            <h2>Recommendation</h2>
    `;

    if (recommendation.summary) {
        html += `<p>${recommendation.summary}</p>`;
    }

    if (recommendation.message) {
        html += `<p>${recommendation.message}</p>`;
    }

    if (items.length > 0) {
        html += "<h3>Suggestions</h3><ul>";

        items.forEach((item) => {
            html += `
                <li>
                    <strong>${item.name || "Recommendation"}</strong>
                    ${item.description ? ` — ${item.description}` : ""}
                    ${item.reason ? ` — ${item.reason}` : ""}
                    ${item.estimated_cost ? ` — ₹${item.estimated_cost}` : ""}
                    ${item.url ? ` <a href="${item.url}" target="_blank">View</a>` : ""}
                </li>
            `;
        });

        html += "</ul>";
    }

    if (tips.length > 0) {
        html += "<h3>Tips</h3><ul>";

        tips.forEach((tip) => {
            html += `<li>${tip}</li>`;
        });

        html += "</ul>";
    }

    html += "</div>";

    container.innerHTML = html;
}


const homeForm = document.getElementById("home-form");

if (homeForm) {
    homeForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const data = {
            budget: Number(document.getElementById("budget").value),
            room_type: document.getElementById("room_type").value,
            style: document.getElementById("style").value,
            location: document.getElementById("location").value
        };

        try {
            const result = await generateRecommendation(
                "/api/generate-home",
                data
            );

            displayRecommendation(result);

        } catch (error) {
            displayRecommendation({
                success: false,
                message: "Unable to generate recommendation."
            });
        }
    });
}


const partyForm = document.getElementById("party-form");

if (partyForm) {
    partyForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const data = {
            budget: Number(document.getElementById("budget").value),
            event_type: document.getElementById("event_type").value,
            guests: Number(document.getElementById("guests").value),
            location: document.getElementById("location").value
        };

        try {
            const result = await generateRecommendation(
                "/api/generate-party",
                data
            );

            displayRecommendation(result);

        } catch (error) {
            displayRecommendation({
                success: false,
                message: "Unable to generate recommendation."
            });
        }
    });
}


const jewelryForm = document.getElementById("jewelry-form");

if (jewelryForm) {
    jewelryForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(jewelryForm);

        try {
            const response = await fetch("/api/generate-jewelry", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            displayRecommendation(result);

        } catch (error) {
            displayRecommendation({
                success: false,
                message: "Unable to generate recommendation."
            });
        }
    });
}
const shoppingForm = document.getElementById("shopping-form");

if (shoppingForm) {
    shoppingForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const category = document.getElementById(
            "shopping-category"
        ).value;

        const budget = Number(
            document.getElementById("shopping-budget").value
        );

        const platform = document.getElementById(
            "shopping-platform"
        ).value;

        const params = new URLSearchParams({
            category: category,
            budget: budget,
            platform: platform
        });

        try {
           const response = await fetch(
                `/api/shopping?${params.toString()}`,
                {
                    method: "POST"
                }
            );

            const result = await response.json();

            const resultsContainer =
                document.getElementById("shopping-results");

            if (!result.success || result.items.length === 0) {
                resultsContainer.innerHTML = `
                    <div class="recommendation-card">
                        <h3>No products found</h3>
                        <p>Try a different category or increase your budget.</p>
                    </div>
                `;
                return;
            }

            resultsContainer.innerHTML = result.items.map(item => `
                <div class="recommendation-card">
                    <h3>${item.name}</h3>
                    <p>${item.description}</p>
                    <p><strong>Price:</strong> ₹${item.price.toLocaleString()}</p>
                    <p><strong>Platform:</strong> ${item.platform}</p>
                    <a href="${item.url}" target="_blank">
                        View Shopping Site
                    </a>
                </div>
            `).join("");

        } catch (error) {
            document.getElementById(
                "shopping-results"
            ).innerHTML = `
                <div class="recommendation-card">
                    <h3>Something went wrong</h3>
                    <p>Unable to load shopping recommendations.</p>
                </div>
            `;
        }
    });
}

async function loadHistory() {
    const container = document.getElementById("history-list");

    if (!container) {
        return;
    }

    try {
        const response = await fetch("/api/history");
        const result = await response.json();

        if (!result.success) {
            container.innerHTML = `
                <div class="history-item">
                    <p>${result.message || "Please login first."}</p>
                </div>
            `;
            return;
        }

        if (!result.items.length) {
            container.innerHTML = `
                <div class="history-item">
                    <p>No recommendations yet.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = result.items.map((item) => `
            <div class="history-item">
                <h3>${item.planner_type}</h3>
                <p>
                    ${new Date(item.created_at).toLocaleString()}
                </p>
                <pre>${JSON.stringify(item.result, null, 2)}</pre>
            </div>
        `).join("");

    } catch (error) {
        container.innerHTML = `
            <div class="history-item">
                <p>Unable to load history.</p>
            </div>
        `;
    }
}


loadHistory();