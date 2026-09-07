export class AudioRecorder {
  constructor(onRecordingComplete) {
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.onRecordingComplete = onRecordingComplete;
  }

  async init() {
    if (!this.mediaRecorder) {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      };

      this.mediaRecorder.onstop = () => {
        const audioBlob = new Blob(this.audioChunks, { type: "audio/webm" });
        this.audioChunks = [];
        this.onRecordingComplete(audioBlob);
      };
    }
  }

  async start() {
    await this.init();
    this.audioChunks = [];
    this.mediaRecorder.start();
  }

  stop() {
    if (this.mediaRecorder && this.mediaRecorder.state === "recording") {
      this.mediaRecorder.stop();
    }
  }
}