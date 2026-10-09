// voice.js - Handles Speech Recognition and Synthesis

let recognition;
let isListening = false;

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
} else {
    alert("Speech Recognition API not supported in this browser. Please use Chrome.");
}

function speak(text, lang='ta-IN') {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    synth.speak(utterance);
}

document.addEventListener('DOMContentLoaded', () => {
    const micBtn = document.getElementById('mic-btn');
    const statusText = document.getElementById('status-text');
    const recognizedText = document.getElementById('recognized-text');

    if(micBtn) {
        micBtn.addEventListener('click', () => {
            if(!recognition) return;

            if(isListening) {
                recognition.stop();
                return;
            }

            const lang = document.querySelector('input[name="lang"]:checked').value;
            recognition.lang = lang;
            
            recognition.start();
            isListening = true;
            micBtn.classList.add('listening');
            statusText.innerText = 'Listening...';
            recognizedText.innerText = '';
        });

        recognition.onresult = async (event) => {
            const transcript = event.results[0][0].transcript;
            recognizedText.innerText = `"${transcript}"`;
            
            // Send to backend for parsing
            const res = await fetch('/api/voice/parse', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: transcript})
            });
            const data = await res.json();
            
            if(data.command === 'checkout') {
                confirmBill();
            } else if (data.command === 'clear_cart') {
                clearCart();
                speak("Cart cleared", "en-IN");
            } else if (data.items && data.items.length > 0) {
                for(let item of data.items) {
                    addToCart(item);
                    
                    // Voice feedback
                    const lang = document.querySelector('input[name="lang"]:checked').value;
                    if(lang === 'ta-IN') {
                        speak(`${item.quantity} ${item.unit} ${item.name} சேர்க்கப்பட்டது`);
                    } else {
                        speak(`${item.quantity} ${item.unit} of ${item.name} added`);
                    }
                }
            } else {
                speak("Sorry, I didn't catch that", "en-IN");
            }
        };

        recognition.onspeechend = () => {
            recognition.stop();
        };

        recognition.onend = () => {
            isListening = false;
            micBtn.classList.remove('listening');
            statusText.innerText = 'Ready';
        };

        recognition.onerror = (event) => {
            statusText.innerText = 'Error occurred in recognition: ' + event.error;
            isListening = false;
            micBtn.classList.remove('listening');
        };
    }
});
