// タイピングゲームの基本設定
const words = ["apple", "banana", "cherry", "date", "elderberry"];
let currentWord = "";
let score = 0;

// HTML要素の取得
const wordDisplay = document.getElementById("word-display");
const inputField = document.getElementById("input-field");
const scoreDisplay = document.getElementById("score-display");

// ランダムな単語を選択
function getRandomWord() {
    const randomIndex = Math.floor(Math.random() * words.length);
    return words[randomIndex];
}

// ゲームの初期化
function initGame() {
    currentWord = getRandomWord();
    wordDisplay.textContent = currentWord;
    inputField.value = "";
    inputField.focus();
}

// 入力が正しいかチェック
function checkInput() {
    if (inputField.value === currentWord) {
        score++;
        scoreDisplay.textContent = `Score: ${score}`;
        initGame();
    }
}

// イベントリスナーの設定
inputField.addEventListener("input", checkInput);

// ゲームの開始
initGame();
