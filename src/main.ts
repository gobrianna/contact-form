const form = document.getElementById("contactForm") as HTMLFormElement;

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);
  const data = {
    name: formData.get("name"),
    email: formData.get("email"),
    message: formData.get("message"),
  };

  try {
    const response = await fetch(
      "https://hiw4wtnkqg.execute-api.us-east-1.amazonaws.com/submit",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    );

    const result = await response.json();

    if (response.ok) {
      alert("Message sent.");
    } else {
      alert(`Error: ${result.error}`);
    }
  } catch (error) {
    console.error("Request failed", error);
    alert("Something went wrong. Please try again later.");
  }
});
