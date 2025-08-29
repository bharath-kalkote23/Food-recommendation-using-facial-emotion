async function fetchJSON(url, opts={}){
  const res = await fetch(url, Object.assign({headers:{'Content-Type':'application/json'}}, opts));
  return await res.json();
}

async function getRecommendations(emotion, diet){
  const payload = { emotion, diet, top_k: 6 };
  const data = await fetchJSON('/api/recommend', { method:'POST', body: JSON.stringify(payload) });
  return data.items || [];
}

function renderMenuCards(container, items){
  container.innerHTML = '';
  items.forEach(item => {
    const el = document.createElement('div');
    el.className = 'card';
    el.innerHTML = `
      <div class="flex items-start justify-between">
        <div>
          <h3 class="text-lg font-semibold">${item.name}</h3>
          <p class="text-sm text-gray-500">${item.category}</p>
          <div class="mt-2 space-x-1">
            ${(item.tags||[]).slice(0,4).map(t=>`<span class="badge">${t}</span>`).join('')}
          </div>
        </div>
        <div class="text-right">
          <div class="text-xl font-bold">₹${item.price}</div>
          <div class="text-sm">⭐ ${item.rating?.toFixed(1) || '4.0'}</div>
        </div>
      </div>
    `;
    container.appendChild(el);
  });
}

async function initIndex(){
  const video = document.getElementById('video');
  const emotionEl = document.getElementById('emotion');
  const dietEl = document.getElementById('diet');
  const captureBtn = document.getElementById('capture');
  const recsDiv = document.getElementById('recs');

  if (navigator.mediaDevices?.getUserMedia) {
    try {
      await FaceAPI.start(video);
    } catch(e) {
      console.warn('Camera blocked; falling back to manual emotion.');
    }
  }

  captureBtn.addEventListener('click', async () => {
    let emotion = 'neutral';
    if (FaceAPI.stream){
      const out = await FaceAPI.detectOnce();
      emotion = out.emotion || 'neutral';
      emotionEl.value = emotion;
    } else {
      emotion = emotionEl.value;
    }
    const items = await getRecommendations(emotion, dietEl.value);
    renderMenuCards(recsDiv, items);
  });
}

window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('video')) initIndex();
});