function onCopyButtonClick() {

}

function onGenerateButtonClick(buttonElement) {
    const url = buttonElement.getAttribute('data-url');
    const outputText = document.getElementById("output");
    fetch(url)
            .then(response => {
                // Check if the request was successful
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json(); // If expecting a JSON response
            })
            .then(data => {
                console.log('Success:', data);
                outputText.textContent = data.output;
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle any errors
            });
}