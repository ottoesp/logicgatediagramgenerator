const MAX_INPUT_SIZE = 200

function onGenerateButtonClick(buttonElement) {
    
    let input = document.getElementById("maininput").value
    if (input.length > MAX_INPUT_SIZE) {
        inputTooLargeError()
    } else {
        fetchGeneratorOutput(buttonElement, input)
    }
    
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function disableGeneratorButton(buttonElement) {
    const spinner = document.getElementById('generate-spinner')
    const buttonText = document.getElementById('generate-text')
    buttonElement.disabled = true

    spinner.classList.remove("d-none");
    buttonText.classList.add("d-none");
}

async function enableGeneratorButton(buttonElement) {
    await new Promise(r => setTimeout(r, 1000));
    const spinner = document.getElementById('generate-spinner')
    const buttonText = document.getElementById('generate-text')

    buttonElement.disabled = false

    spinner.classList.add("d-none");
    buttonText.classList.remove("d-none");
}

async function setTemporaryOutputBorder(temp_border_class) {
    const outputBox = document.getElementById('output-div')
    outputBox.classList.add(temp_border_class);

    await new Promise(r => setTimeout(r, 1000));

    outputBox.classList.remove(temp_border_class);
}

function fetchGeneratorOutput(buttonElement, input) {
    const url = buttonElement.getAttribute('data-url');
    const outputText = document.getElementById("output");
    const csrftoken = Cookies.get('csrftoken')

    const max_width_selector = document.getElementById("max-width-selector")

    disableGeneratorButton(buttonElement)

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
                if (data.ok) {
                    outputText.textContent = data.output;
                    setTemporaryOutputBorder('border-success')
                } else {
                    outputText.textContent = data.reasons;
                    setTemporaryOutputBorder('border-danger')
                }
            })
            .catch(error => {
                console.error('Error:', error);
            })
            .finally(
                enableGeneratorButton(buttonElement)
            );
}

function inputTooLargeError() {
    const outputText = document.getElementById("output");
    outputText.textContent = "Error: Input too Large"
}