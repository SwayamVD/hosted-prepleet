let allQuestions = [];

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("searchInput");
  const searchButton = document.getElementById("searchButton");
  const questionsContainer = document.getElementById("questions-container");

  // Fetch initial data for company and question sets
  fetch("/questions")
    .then((res) => res.json())
    .then((data) => {
      allQuestions = data;
      // Your existing code to populate company buttons goes here
      const companies = [...new Set(data.map((q) => q.Company))];
      const companyList = document.getElementById("company-list");
      companies.forEach((company) => {
        const btn = document.createElement("button");
        btn.className = "btn btn-dark border btn-sm rounded";
        btn.innerText = company;
        btn.onclick = () => {
          document
            .querySelectorAll("#company-list .btn, #ques-sets .btn")
            .forEach((b) => b.classList.remove("active"));
          btn.classList.add("active");
          showQuestions(company);
        };
        companyList.appendChild(btn);
      });
    });

  // Event listener for the search button
  searchButton.addEventListener("click", () => {
    const query = searchInput.value.trim();
    if (query) {
      fetchAndDisplayQuestions(query);
    } else {
      // Optional: Clear results if search bar is empty
      questionsContainer.innerHTML = "<h4>Please enter a search query.</h4>";
    }
  });

  // Event listener for the search input (on 'Enter' key press)
  searchInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      searchButton.click(); // Trigger button click
    }
  });
});

// New function to fetch questions based on search query
function fetchAndDisplayQuestions(searchQuery) {
  const container = document.getElementById("questions-container");
  container.innerHTML = "<h4>Searching...</h4>"; // Show loading message

  // Remove 'active' class from all other buttons
  document
    .querySelectorAll("#company-list .btn, #ques-sets .btn")
    .forEach((b) => b.classList.remove("active"));

  // Construct the URL with the search query parameter
  const url = `/search?search=${encodeURIComponent(searchQuery)}`;

  fetch(url)
    .then((res) => {
      if (!res.ok) {
        throw new Error("Network response was not ok");
      }
      return res.json();
    })
    .then((data) => {
      container.innerHTML = `<h4>Search results for "${searchQuery}"</h4>`;
      if (data.length === 0) {
        container.innerHTML += `<p>No questions found.</p>`;
        return;
      }

      const listGroup = document.createElement("div");
      listGroup.className = "list-group questionlistcss";

      data.forEach((q, index) => {
        const item = document.createElement("a");
        item.className =
          "list-group-item list-group-item-action d-flex justify-content-between align-items-center";
        item.href = `/solve?title=${q.titleSlug}`;
        item.style.textDecoration = "none";

        item.innerHTML = `
                    <div class="question-title">${q.id}. ${q.title}</div>
                    <span class="badge badge-dark-${q.difficulty}">${q.difficulty}</span>
                `;
        listGroup.appendChild(item);
      });
      container.appendChild(listGroup);
    })
    .catch((error) => {
      console.error("Error fetching search results:", error);
      container.innerHTML = "<h4>Error loading search results.</h4>";
    });
}

// Your existing showQuestions and listquesset functions remain unchanged
function showQuestions(company) {
  const container = document.getElementById("questions-container");
  container.innerHTML = `<h4 class="mb-3">${company} Questions</h4>`;
  const questions = allQuestions.filter((q) => q.Company === company);
  // ... (rest of your showQuestions logic)
  if (questions.length === 0) {
    container.innerHTML += `<p>No questions found for ${company}.</p>`;
    return;
  }
  const listGroup = document.createElement("div");
  listGroup.className = "list-group questionlistcss";
  questions.forEach((q, index) => {
    const item = document.createElement("a");
    item.className =
      "list-group-item list-group-item-action d-flex justify-content-between align-items-center";
    item.href = `/solve?title=${q.Slug}`;
    item.style.textDecoration = "none";
    item.innerHTML = `
            <div class="question-title">${index + 1}. ${q.Title}</div>
            <span class="badge badge-dark-${q.Difficulty}">${
      q.Difficulty
    }</span>
        `;
    listGroup.appendChild(item);
  });
  container.appendChild(listGroup);
}

// faviourate list retrival
function listquesset(name, fname) {
  fetch(`/getquestionset/${name}`)
    .then((res) => res.json())
    .then((data) => {
      setq = data;
      document
        .querySelectorAll("#company-list .btn")
        .forEach((b) => b.classList.remove("active"));
      const actbtn = document.getElementById("eeudwo2i");
      actbtn.classList.add("active");
      const container = document.getElementById("questions-container");
      container.innerHTML = `<h4 class="mb-3">${fname} Question Set</h4>`;
      if (setq.length === 0) {
        container.innerHTML += `<p>No questions found for ${fname}.</p>`;
        return;
      }
      const listGroup = document.createElement("div");
      listGroup.className = "list-group questionlistcss";
      setq.forEach((q, index) => {
        const item = document.createElement("a");
        item.className =
          "list-group-item list-group-item-action d-flex justify-content-between align-items-center";
        item.href = `/solve?title=${q.titleSlug}`;
        item.style.textDecoration = "none";
        item.innerHTML = `
                    <div class="question-title">${q.id}. ${q.title}</div>
                    <span class="badge badge-dark-${q.difficulty}">${q.difficulty}</span>
                `;
        listGroup.appendChild(item);
      });
      container.appendChild(listGroup);
    })
    .catch((error) => console.error("Error:", error));
}
