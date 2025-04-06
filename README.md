# Telegram Bot Project

## 🚀 Quick Start

### Requirements

Make sure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Make](https://www.gnu.org/software/make/)
- [Tuna](https://tuna.am/) (optional for https tunnel)
- [uv](https://docs.astral.sh/uv/) (dependency resolver)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/telegram-bot.git
cd telegram-bot
```

### 2. Setup Environment

#### On Unix:
```bash
make uinit
```

#### On Windows:
```powershell
make winit
```

This will:
- Install all Python dependencies
- Create a `.env` file from `example.env`

### 3. Start the Bot

#### Debug Mode (local run):
```bash
make debug
```

#### Production Mode (Docker):
```bash
make prod
```

To stop production containers:
```bash
make down-prod
```

---

## 🧪 Code Quality & Testing

Run all checks:
```bash
make check
```

Lint and auto-fix:
```bash
make lint
```

Format code:
```bash
make format
```

Type checking:
```bash
make type-check
```

---

## 📊 Optional: Enable Tuna

[Tuna](https://tuna.am/) is a lightweight tunnels to your local network.

To use Tuna:
- Sign up at [tuna.am](https://tuna.am/)
- Set the required token/key
```bash
tuna http <port>
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

MIT License. See `LICENSE` file for details.

---

Happy hacking! 🤖
