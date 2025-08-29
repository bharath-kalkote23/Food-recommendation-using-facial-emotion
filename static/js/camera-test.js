document.addEventListener("DOMContentLoaded", async () => {
  const video = document.getElementById("video");
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    console.log("✅ Camera started successfully");
  } catch (err) {
    console.error("❌ Camera error:", err);
    alert("Camera access failed: " + err.message);
  }
});
