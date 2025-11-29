const MAX_INPUT_SIZE = 200

function onGenerateButtonClick(buttonElement) {
    
    let input = document.getElementById("maininput").value
    if (input.length > MAX_INPUT_SIZE) {
        inputTooLargeError()
    } else {
        fetchGeneratorOutput(buttonElement, input)
    }
    
}

function fetchGeneratorOutput(buttonElement, input) {
    const url = buttonElement.getAttribute('data-url');
    const outputText = document.getElementById("output");
    const csrftoken = Cookies.get('csrftoken')

    const max_width_selector = document.getElementById("max-width-selector")

    fetch(url, {
        method: 'POST',
        headers: {
            'max-diagram-width' : max_width_selector.value,
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

function inputTooLargeError() {
    const outputText = document.getElementById("output");
    outputText.textContent = "Error: Input too Large"
}