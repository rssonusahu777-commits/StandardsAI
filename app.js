document.addEventListener("DOMContentLoaded", function () {

  const button = document.getElementById("analyze-btn");

  button.addEventListener("click", async function () {

    const input = document.getElementById("product-input").value.trim();

    console.log("Clicked:", input);

    if (!input) {
      alert("Enter product description");
      return;
    }

    const grid = document.getElementById("standards-grid");
    const count = document.getElementById("results-count");
    const latency = document.getElementById("results-latency");

    grid.innerHTML = "<p>Loading...</p>";
    count.textContent = "Processing...";
    latency.textContent = "...";

    const start = Date.now();

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: input })
      });

      const data = await res.json();

      console.log("API response:", data);

      const time = ((Date.now() - start) / 1000).toFixed(2);

      if (!data.results || data.results.length === 0) {
        grid.innerHTML = "<p>No results found</p>";
        count.textContent = "0 standards found";
        latency.textContent = time + "s";
        return;
      }

      grid.innerHTML = "";

      data.results.forEach((item, i) => {
        const div = document.createElement("div");

        div.style.border = "1px solid #ccc";
        div.style.margin = "10px";
        div.style.padding = "10px";

        div.innerHTML = `
          <h3>#${i + 1} - ${item.standard}</h3>
          <p>${item.reason}</p>
          <small>${item.category} | Score: ${(item.score * 100).toFixed(0)}%</small>
        `;

        grid.appendChild(div);
      });

      count.textContent = data.results.length + " standards found";
      latency.textContent = time + "s";

    } catch (error) {
      console.error(error);
      grid.innerHTML = "<p style='color:red;'>Error connecting backend</p>";
    }

  });

});