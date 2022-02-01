function Codetester(element, options) {

    let widgetUrl = options.widgetUrl;
    let testResultCallback = options.testResultCallback;
    let resultsElement = null;
    let codeElement = null;
    let submitUrl = null;
    let checkSubmissionUrl = null;
    let counter = null;
    let interval = null;
    let submitButton = null;

    let loading = `
        <div class="codetester-widget">
            <textarea class='codetester-results-textarea-loading' disabled>Loading...</textarea>
        </div>
    `

    let codetesterWidget = `
<div class="codetester-widget">
    <div class="codetester-title-div">
    </div>
    <div class="codetester-instructions-div">
    </div>
    <div class="codetester-ide-div">
    </div>
    <div class="codetester-results-div">
        <textarea class='codetester-results-textarea' disabled></textarea>
    </div>
    <div class="codetester-submit-div">
        <button class="codetester-submit-btn">Submit</button>
        <div class="codetester-powered-by">Powered By <a href="https://codetester.io/widget">CodeTester Widget</a></div>
    </div>
</div>
`;

    element.innerHTML = loading;
    resultsElement = element.getElementsByClassName("codetester-results-textarea-loading")[0];

    fetch(widgetUrl)
     .then(response => {
         if (!response.ok)
             throw response;

        return response.json();
     })
     .then(data => {
        submitUrl = data.submit_url;
        checkSubmissionUrl = data.check_submission_url;

        element.innerHTML = codetesterWidget;
        element.getElementsByClassName("codetester-instructions-div")[0].innerHTML = data.instructions;
        element.getElementsByClassName("codetester-title-div")[0].innerHTML = "<h4>" + data.title + "</h4>";

        resultsElement = element.getElementsByClassName("codetester-results-textarea")[0];
        submitButton = element.getElementsByClassName("codetester-submit-btn")[0];

        submitButton.onclick = submit;

        codeElement = CodeMirror(element.getElementsByClassName("codetester-ide-div")[0], {
            mode: data.codemirror_language,
            lineNumbers: true,
            indentUnit: 4,
            matchBrackets: true,
            value: data.starting_code
        });
     })
     .catch(error => {
         errorHandler(error);
     });


    function submit() {
        resultsElement.value = "Processing...";
        submitButton.disabled = true;
        fetch(submitUrl, {
            body: JSON.stringify({"code": codeElement.getValue() }),
            mode: "cors",
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            }
         })
         .then(response => {
            if (!response.ok)
                throw response;

            return response.text();
        }).then(token => {
            counter = 0;
            interval = setInterval(function() {
                checkSubmission(token, resultsElement)
            }, 1500);
        }).catch(error => {
            errorHandler(error);
        });
    }

    function checkSubmission(token) {
        fetch(checkSubmissionUrl + "?token=" + token)
         .then(response => {
            if (!response.ok)
                throw response;

            return response.json();
        }).then(data => {
            if (data.status == "done") {
                clearInterval(interval);
                resultsElement.value = data.text;
                testResultCallback(data.passed);
                submitButton.disabled = false;
            }
            else if (data.status == "processing") {
                counter++;
                 if (counter >= 30) {
                    clearInterval(interval);
                    resultsElement.value = "Timed out";
                    submitButton.disabled = false;
                 }
            }
        }).catch(error => {
            errorHandler(error);
        });
    }

    function errorHandler(error) {
        if (error.text == undefined) {
            resultsElement.value = error;
            submitButton.disabled = false;
        }
        else {
            error.text().then(errorMessage => {
                resultsElement.value = "Error: " + error.statusText + "\n" + errorMessage;
                if (submitButton != null)
                    submitButton.disabled = false;
            });
        }
    }

}