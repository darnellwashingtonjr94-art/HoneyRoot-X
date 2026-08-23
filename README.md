IMG_1402.jpeg
## HoneyRoot-X

HoneyRoot-X is a containerized SSH honeypot designed to bait attackers seeking root access, capture their brute-force credentials, and log their post-exploitation commands within an isolated fake bash shell.

## Setup & Deployment

1. **Clone the repository:**
   \`\`\`bash
   git clone https://github.com/yourusername/HoneyRoot-X.git
   cd HoneyRoot-X
   \`\`\`

2. **Start the honeypot using Docker Compose:**
   \`\`\`bash
   docker-compose up -d
   \`\`\`
   *(Note: This binds to port 22 on your host machine. Ensure your actual SSH daemon is moved to another port like 2222 before starting).*

3. **View the Logs:**
   All attacker activity is logged in structured JSON format.
   \`\`\`bash
   cat logs/honeypot.json
   \`\`\`

## Security Warning
Do not run this on a production system without fully understanding Docker networking and isolation. Always change your primary SSH port before binding a honeypot to port 22.
