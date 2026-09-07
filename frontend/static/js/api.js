export async function sendAudioForTranslation(audioBlob, targetLanguage) {
  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.webm");
  formData.append("target_language", targetLanguage);

  const response = await fetch("/api/translate", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.error || `Server error: ${response.status}`);
  }

  return await response.json();
}