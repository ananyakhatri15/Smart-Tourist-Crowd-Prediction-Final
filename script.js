const predictionReason = document.querySelector("#prediction-reason");
const button = document.querySelector("button");
const selects = document.querySelectorAll("select");
const destinationInput = document.querySelector("#destination");

const resultHeading = document.querySelector(".result h1");
const resultText = document.querySelector(".result p");

const scoreNumber = document.querySelector("#score-number");
const scoreFill = document.querySelector("#score-fill");

button.addEventListener("click", async function () {

    const destination = destinationInput.value.trim();
    const day = selects[0].value;
    const weather = selects[1].value;
    const holiday = selects[2].value;
    const festival = selects[3].value;

    if (destination === "") {
        resultHeading.innerText = "Enter a destination";
        resultText.innerText = "Please enter a place before predicting.";

        scoreNumber.innerText = "-- / 100";
        scoreFill.style.width = "0%";
        predictionReason.innerHTML = "";
        return;
    }

    resultHeading.innerText = "Predicting...";
    resultText.innerText = "Please wait...";
    scoreNumber.innerText = "-- / 100";
    scoreFill.style.width = "0%";
    predictionReason.innerHTML = "";

    try {

        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                destination: destination,
                day: day,
                weather: weather,
                holiday: holiday,
                festival: festival
            })
        });

        if (!response.ok) {
            throw new Error("Server error: " + response.status);
        }

        const data = await response.json();

        if (!data.destination_found) {
            resultHeading.innerText = "Destination not found";
            resultText.innerText =
                "We don't have tourism data for " + destination + ".";

            scoreNumber.innerText = "-- / 100";
            scoreFill.style.width = "0%";

            return;
        }

        const crowd = data.prediction;

        resultHeading.innerText = crowd;

        resultText.innerText =
            destination + " may have a " +
            crowd.toLowerCase() +
            " crowd on " + day + ".";
            let reasons = [];

if (day === "Saturday" || day === "Sunday") {
    reasons.push("Weekend travel can increase visitor activity.");
}

if (holiday === "Yes") {
    reasons.push("A holiday can increase tourist activity.");
}

if (festival === "Yes") {
    reasons.push("A festival or event can increase visitor activity.");
}

if (weather === "Rainy") {
    reasons.push("Rainy weather may reduce outdoor tourist activity.");
}

if (reasons.length === 0) {
    reasons.push("The prediction is based on the selected destination and travel conditions.");
}

predictionReason.innerHTML =
    "<strong>Why this prediction?</strong><br>" +
    reasons.map(reason => "• " + reason).join("<br>");

        if (data.crowd_score !== null) {

            const score = Number(data.crowd_score);

            scoreNumber.innerText = score + " / 100";
            scoreFill.style.width = score + "%";
        }

        if (crowd.toUpperCase() === "HIGH") {

            resultHeading.style.color = "red";

        } else if (crowd.toUpperCase() === "MEDIUM") {

            resultHeading.style.color = "#d4a500";

        } else {

            resultHeading.style.color = "green";
        }

    } catch (error) {

        console.error(error);

        resultHeading.innerText = "Error";

        resultText.innerText =
            "Could not connect to the prediction server.";

        scoreNumber.innerText = "-- / 100";
        scoreFill.style.width = "0%";
    }
});