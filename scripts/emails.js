async function updateEmails() {
    const response = await fetch('/dashboard');
    const data = await response.json();

    document.getElementById('unread-emails').textContent = `You have ${data.unread_emails} unread emails.`;
}
