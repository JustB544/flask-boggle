const form = document.querySelector("form")
const input = document.querySelector("#guess")
const start = document.querySelector("#start")
const table = document.querySelector("table")
const timer = document.querySelector("#timer")
const resp = document.querySelector("#response")
const hScore = document.querySelector("#h_score span")
let _score;

let score = 0;

start.addEventListener("click", () => {
    form.classList.remove("hide");
    table.classList.remove("hide");
    timer.classList.remove("hide");
    start.outerHTML = "<h3 id='score'>Score: <span>0</span><h3>";
    _score = document.querySelector("#score span");
    const interval = setInterval(() => {
        timer.innerText -= 1;
        if (timer.innerText === '0') {
            endGame();
            clearInterval(interval);
        }
    }, 1000);
})

form.addEventListener("submit", async (evt) => {
    evt.preventDefault()
    const { data } = await axios.get("/check", { params: { word: input.value } });
    input.value = "";
    resp.innerText = data.result;
    if (data.result === "ok") {
        score++;
        _score.innerText = score;
    }
    if (resp.classList.contains("response-trans1")) {
        resp.classList.remove("response-trans1");
        resp.classList.add("response-trans2");
    }
    else if (resp.classList.contains("response-trans2")) {
        resp.classList.remove("response-trans2");
        resp.classList.add("response-trans1");
    }
    else {
        resp.classList.remove("hide");
        resp.classList.add("response-trans1");
    }
});

function endGame() {
    hScore.innerText = score;
    console.log(_score.innerText);
    axios.post(`/gameover?score=${score}`);
    form.classList.add("hide");
    table.classList.add("hide");
    timer.classList.add("hide");
}