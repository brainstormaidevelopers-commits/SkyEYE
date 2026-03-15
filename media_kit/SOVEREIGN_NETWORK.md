# [ SOVEREIGN_NETWORK ] // HEADSCALE x SKYEYE

### 1. THE ARCHITECTURE
To keep the **0Core Brain** private while using a public **Netlify Frontend**, we use a sovereign overlay network. 
*   **Headscale**: Your private coordination server (Sovereign alternative to Tailscale).
*   **The Result**: Your backend at `localhost:5050` becomes accessible at a private IP (e.g., `10.0.0.5:5050`) only to authenticated team members.

### 2. DEPLOYING YOUR HEADSCALE NODE (Docker)
Run this on a small VPS or a dedicated local server:

```yaml
version: '3.7'
services:
  headscale:
    image: headscale/headscale:latest
    volumes:
      - ./config:/etc/headscale
      - ./data:/var/lib/headscale
    ports:
      - "8080:8080"
      - "9090:9090"
    command: headscale serve
```

### 3. CONNECTING THE BRAIN
1.  Install the Tailscale client on your local GPU machine.
2.  Point it to your Headscale instance:
    `tailscale up --login-server http://<YOUR_HEADSCALE_IP>:8080`
3.  Note the private IP assigned to your machine (e.g., `100.64.0.5`).

### 4. UPDATING THE UI
Once you have your private IP, update the `API_BASE` in `index.html`.
*   **Localhost**: `http://localhost:5050`
*   **Headscale**: `http://100.64.0.5:5050` (Replace with your actual IP)
