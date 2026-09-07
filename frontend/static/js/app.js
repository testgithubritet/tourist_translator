import { sendAudioForTranslation } from "./api.js";
import { AudioRecorder } from "./recorder.js";

let currentSpeaker = null; // 'tourist' | 'local'

const touristOutput = document.getElementById("tourist-output");
const touristSubtext = document.getElementById("tourist-subtext");
const localOutput = document.getElementById("local-output");
const localSubtext = document.getElementById("local-subtext");

const btnTourist = document.getElementById("btn-tourist");
const btnLocal = document.getElementById("btn-local");

const selectTouristLang = document.getElementById("tourist-lang");
const selectLocalLang = document.getElementById("local-lang");

function updateUI(speaker, title, subtitle = "") {
  if (speaker === "tourist") {
    // Tourist spoke -> update Local's screen
    localOutput.innerText = title;
    localSubtext.innerText = subtitle;
  } else {
    // Local spoke -> update Tourist's screen
    touristOutput.innerText = title;
    touristSubtext.innerText = subtitle;
  }
}

async function handleAudioComplete(audioBlob) {
  const targetLanguage =
    currentSpeaker === "tourist"
      ? selectLocalLang.value
      : selectTouristLang.value;

  updateUI(currentSpeaker, "Translating speech...", "Running AssemblyAI Universal-1 & LeMUR...");

  try {
    const data = await sendAudioForTranslation(audioBlob, targetLanguage);
    if (data.translated_text) {
      updateUI(currentSpeaker, `"${data.translated_text}"`, `Original: "${data.original_text}" (${data.detected_language})`);
    } else {
      updateUI(currentSpeaker, "(No speech recognized)", "Please try holding the button and speaking clearly.");
    }
  } catch (error) {
    updateUI(currentSpeaker, "Error Processing Speech", error.message);
  }
}

const recorder = new AudioRecorder(handleAudioComplete);

function bindHoldEvents(button, speakerMode) {
  const startRecording = async (e) => {
    e.preventDefault();
    currentSpeaker = speakerMode;
    button.classList.add("recording-active", "ring-4", "ring-white");
    updateUI(speakerMode, "Listening...", "Recording your voice...");
    await recorder.start();
  };

  const stopRecording = (e) => {
    e.preventDefault();
    button.classList.remove("recording-active", "ring-4", "ring-white");
    recorder.stop();
  };

  // Mouse controls
  button.addEventListener("mousedown", startRecording);
  button.addEventListener("mouseup", stopRecording);

  // Mobile touch controls
  button.addEventListener("touchstart", startRecording);
  button.addEventListener("touchend", stopRecording);
}

bindHoldEvents(btnTourist, "tourist");
bindHoldEvents(btnLocal, "local");