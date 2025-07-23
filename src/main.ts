const form = document.querySelector("form");

form?.addEventListener("submit", (e) => {
  e.preventDefault();

  const visitorName = document.querySelector<HTMLInputElement>("#name")!;
  const email = document.querySelector<HTMLInputElement>("#email")!;
  const message = document.querySelector<HTMLTextAreaElement>("#message")!;

  const errors: string[] = [];

  if (!visitorName.value.trim()) {
    errors.push("Enter your name.");
  }

  if (!email.value.trim()) {
    errors.push("Enter your e-mail address.");
  }

  if (!message.value.trim()) {
    errors.push("Type a message.");
  }

  if (errors.length > 0) {
    alert("Looks like you forgot something:\n\n" + errors.join("\n"));
    return;
  }

  alert("TypeScript:\nForm has been successfully submitted.");
  form.reset();
});
