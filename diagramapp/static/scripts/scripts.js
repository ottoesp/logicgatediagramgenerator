function onGenerateButtonClick(buttonElement) {
    const url = buttonElement.getAttribute('data-url');
    const outputText = document.getElementById("output");
    const csrftoken = Cookies.get('csrftoken')

    let input = document.getElementById("maininput").value

    fetch(url, {
        method: 'POST',
        headers: {
            'max-diagram-width' : 5,
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        body: input
    })
            .then(response => {
                // Check if the request was successful
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json(); // If expecting a JSON response
            })
            .then(data => {
                
                outputText.textContent = data.output;
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle any errors
            });
}