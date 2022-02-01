var interval = null;
var counter = null;

function submitCode(submitUrl, checkUrl, code, input, language, csrfToken, displayElement, doneCallback){
    displayElement.val("Processing...");
    $.ajax({
        headers: { "X-CSRFToken": csrfToken },
        url: submitUrl,
        data: {"code": code, "language": language, "input": input},
        type: "POST"
    }).done(function(response) {
        var token = response;
        counter = 0;
        interval = setInterval(function() {
            checkSubmission(checkUrl, token, displayElement, doneCallback)
        }, 1500);
    }).fail(function(jqXHR, textStatus){
        displayElement.val(textStatus + ": " + jqXHR["responseText"]);
    });
}

function checkSubmission(checkUrl, token, displayElement, doneCallback) {
    $.get(checkUrl, {
        "token": token
    }).done(function(response) {
         if (response["status"] == "done") {
             clearInterval(interval);
             displayElement.val(response["text"]);
             doneCallback(response["passed"]);
         }
         else if (response["status"] == "processing") {
             counter++;
             if (counter >= 30) {
                clearInterval(interval);
                displayElement.val("Failed to get a valid response");
             }
         }
     }).fail(function(jqXHR, textStatus){
         clearInterval(interval);
         displayElement.val(textStatus + ": " + jqXHR["responseText"]);
     });
}

function wrapCode(code) {
    var all = "import io\n";
    all += "import sys\n";
    all += "from contextlib import redirect_stdout\n";
    all += "def out(**kwargs):\n";
    all += "\tfio = io.StringIO()\n";
    all += "\twith redirect_stdout(fio):\n\t\tpass\n\t\t";
    all += code.replace(/\n/g, "\n\t\t") + "\n";
    all += "\toutput = fio.getvalue().strip()\n";
    all += "\treturn output";
    return all;
}