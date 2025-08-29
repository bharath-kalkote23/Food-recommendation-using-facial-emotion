// Face Emotion Detection + Menu Recommendation
const FaceAPI = {
  modelsLoaded: false,
  video: null,
  stream: null,
  currentEmotion: "neutral",

  async load() {
    if (this.modelsLoaded) return;
    const MODEL_URL = "/static/models";
    await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
    await faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL);
    this.modelsLoaded = true;
  },

  async start(videoEl) {
    this.video = videoEl;
    await this.load();
    this.stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoEl.srcObject = this.stream;

    // Start detecting when video plays
    videoEl.onloadedmetadata = () => {
      videoEl.play();
      this.detectLoop();
    };
  },

  async detectLoop() {
    if (!this.video) return;

    setInterval(async () => {
      const detection = await faceapi
        .detectSingleFace(this.video, new faceapi.TinyFaceDetectorOptions())
        .withFaceExpressions();

      if (detection && detection.expressions) {
        // Get best emotion
        let best = "neutral", max = 0;
        for (const [k,v] of Object.entries(detection.expressions)) {
          if (v > max) { max = v; best = k; }
        }

        this.currentEmotion = best;
        document.getElementById("emotionDisplay").innerText = `Detected Emotion: ${best}`;

        // Fetch recommendations
        this.fetchRecommendations(best);
      }
    }, 3000); // every 3 seconds
  },

  async fetchRecommendations(emotion) {
    try {
      const res = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ emotion: emotion, top_k: 4 })
      });
      const data = await res.json();
      this.updateRecommendations(data.items || []);
    } catch (err) {
      console.error("Error fetching recommendations:", err);
    }
  },

  updateRecommendations(items) {
    const list = document.getElementById("recommendList");
    if (!list) return;
    list.innerHTML = "";
    items.forEach(item => {
      const li = document.createElement("li");
      li.className = "p-3 bg-white shadow rounded mb-2";
      li.innerHTML = `<strong>${item.name}</strong> - ${item.category || ""} (${item.rating || "⭐?"})`;
      list.appendChild(li);
    });
  },

  stop() {
    if (this.stream) {
      this.stream.getTracks().forEach(t => t.stop());
      this.stream = null;
    }
  }
};
