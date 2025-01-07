document.getElementById('emailForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const senderEmail = document.getElementById('senderEmail').value;
    const senderPassword = document.getElementById('senderPassword').value;
    const emailFile = document.getElementById('emailFile').files[0];
    const emailSubject = document.getElementById('emailSubject').value;
    const emailBody = document.getElementById('emailBody').value;

    const formData = new FormData();
    formData.append('senderEmail', senderEmail);
    formData.append('senderPassword', senderPassword);
    formData.append('emailFile', emailFile);
    formData.append('emailSubject', emailSubject);
    formData.append('emailBody', emailBody);

    const response = await fetch('/send-emails', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    document.getElementById('message').innerText = result.message;
});
